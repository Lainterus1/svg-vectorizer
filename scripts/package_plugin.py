#!/usr/bin/env python3
"""Build a deterministic, allowlisted source ZIP. Does not install or publish."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from pathlib import Path, PurePosixPath
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = {'.codex-plugin/plugin.json', 'skills/vectorize/SKILL.md', 'LICENSE',
            'requirements.txt', 'package.json', 'package-lock.json',
            'scripts/vectorize.py', 'scripts/svg_tools.mjs', 'pyproject.toml',
            'distribution-files.json', 'scripts/package_plugin.py'}


def package_files(root):
    root = Path(root).resolve()
    entries = json.loads((root / 'distribution-files.json').read_text(encoding='utf-8'))
    if not isinstance(entries, list) or not all(isinstance(p, str) for p in entries):
        raise ValueError('distribution-files.json must be an array of relative file paths')
    if len(entries) != len(set(entries)) or not REQUIRED.issubset(entries):
        raise ValueError('duplicate or missing required distribution files')
    files = []
    for entry in sorted(entries):
        relative = PurePosixPath(entry)
        if (relative.is_absolute() or '..' in relative.parts or '\\' in entry
                or str(relative) != entry or ':' in entry):
            raise ValueError(f'unsafe distribution path: {entry}')
        path = root
        for part in relative.parts:
            path /= part
            try:
                metadata = path.lstat()
            except FileNotFoundError as error:
                raise ValueError(f'missing distribution file: {entry}') from error
            # Windows directory junctions are reparse points but not symlinks.
            # Reject both before reading a child or following a redirected file.
            if (stat.S_ISLNK(metadata.st_mode)
                    or getattr(metadata, 'st_file_attributes', 0)
                    & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400)):
                raise ValueError(f'symlink/reparse point not allowed in distribution: {entry}')
        if not path.is_file():
            raise ValueError(f'missing distribution file: {entry}')
        files.append((entry, path.read_bytes()))
    manifest = json.loads(dict(files)['.codex-plugin/plugin.json'])
    interface = manifest.get('interface', {})
    for field in ('composerIcon', 'logo', 'logoDark'):
        value = interface.get(field)
        if value is not None and (not isinstance(value, str) or not value.startswith('./')
                                  or value[2:] not in entries):
            raise ValueError(f'manifest {field} is absent from distribution')
    return files


def build_archive(output, root=ROOT):
    files = package_files(root)  # Finish input checks before touching the destination.
    output = Path(output)
    if output.suffix.lower() != '.zip':
        raise ValueError('output must have a .zip extension')
    root = Path(root).resolve()
    if output.resolve() in {(root / name).resolve() for name, _ in files}:
        raise ValueError('output would overwrite an input')
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, prefix='.package-', suffix='.zip', delete=False) as stream:
            temporary = Path(stream.name)
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, data in files:
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        digest = hashlib.sha256(temporary.read_bytes()).hexdigest()
        size = temporary.stat().st_size
        os.replace(temporary, output)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()
    return {'archive': str(output.resolve()), 'sha256': digest, 'bytes': size,
            'files': len(files), 'published': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-o', '--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(build_archive(args.output), ensure_ascii=False, indent=2))
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        parser.exit(1, f'package: {error}\n')


if __name__ == '__main__':
    main()
