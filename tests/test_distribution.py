"""Distribution regressions use only the standard library."""
import json
from pathlib import Path
import shutil
import stat
from types import SimpleNamespace
from unittest.mock import patch
import tempfile
import unittest
import zipfile
from scripts import package_plugin as package


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.root = self.folder / 'svg-vectorizer'
        self.root.mkdir()
        entries = json.loads((package.ROOT / 'distribution-files.json').read_text())
        for name in entries:
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(package.ROOT / name, destination)
        self.output = self.folder / 'plugin.zip'

    def test_archive_is_reproducible_and_excludes_unlisted_files(self):
        (self.root / '.env').write_text('NOT_A_REAL_SECRET=fixture')
        (self.root / 'node_modules').mkdir()
        (self.root / 'node_modules' / 'unexpected.js').write_text('fixture')
        first = package.build_archive(self.output, self.root)
        original = self.output.read_bytes()
        package.build_archive(self.output, self.root)
        self.assertEqual(self.output.read_bytes(), original)
        self.assertFalse(first['published'])
        with zipfile.ZipFile(self.output) as archive:
            names = set(archive.namelist())
            self.assertTrue(package.REQUIRED.issubset(names))
            self.assertNotIn('.env', names)
            self.assertFalse(any('node_modules' in name for name in names))
            self.assertNotIn('examples/smoke-report.json', names)
            self.assertIsNone(archive.testzip())

    def change_list(self, entry):
        path = self.root / 'distribution-files.json'
        entries = json.loads(path.read_text())
        entries.append(entry)
        path.write_text(json.dumps(entries))

    def test_traversal_and_absolute_paths_preserve_destination(self):
        original = (self.root / 'distribution-files.json').read_bytes()
        for path in ['../outside', '/tmp/outside', 'C:/outside', 'scripts/../LICENSE']:
            (self.root / 'distribution-files.json').write_bytes(original)
            self.change_list(path)
            self.output.write_bytes(b'previous archive')
            with self.subTest(path=path), self.assertRaises(ValueError):
                package.build_archive(self.output, self.root)
            self.assertEqual(self.output.read_bytes(), b'previous archive')

    def test_missing_required_file_preserves_destination(self):
        (self.root / 'LICENSE').unlink()
        self.output.write_bytes(b'previous archive')
        with self.assertRaises(ValueError):
            package.build_archive(self.output, self.root)
        self.assertEqual(self.output.read_bytes(), b'previous archive')

    def test_missing_manifest_asset_is_rejected(self):
        path = self.root / 'distribution-files.json'
        entries = json.loads(path.read_text())
        entries.remove('assets/logo.png')
        path.write_text(json.dumps(entries))
        with self.assertRaisesRegex(ValueError, 'manifest logo'):
            package.build_archive(self.output, self.root)

    def test_windows_reparse_directory_preserves_destination(self):
        real_lstat = Path.lstat
        def redirected(path, *args, **kwargs):
            metadata = real_lstat(path, *args, **kwargs)
            if path == self.root / 'assets':
                return SimpleNamespace(st_mode=metadata.st_mode,
                    st_file_attributes=getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400))
            return metadata
        self.output.write_bytes(b'previous archive')
        with patch.object(Path, 'lstat', redirected):
            with self.assertRaisesRegex(ValueError, 'reparse'):
                package.build_archive(self.output, self.root)
        self.assertEqual(self.output.read_bytes(), b'previous archive')

    def test_symlink_rejected(self):
        target = self.root / 'LICENSE'
        target.unlink()
        try:
            target.symlink_to(package.ROOT / 'LICENSE')
        except OSError as error:
            self.skipTest(f'symlink unavailable: {error}')
        with self.assertRaises(ValueError):
            package.build_archive(self.output, self.root)


if __name__ == '__main__':
    unittest.main()
