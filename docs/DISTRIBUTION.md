# Install and package the plugin

SVG Vectorizer is a standalone skills-only plugin. Its source lives at
[Lainterus1/svg-vectorizer](https://github.com/Lainterus1/svg-vectorizer).
Publishing source on GitHub does not mean the plugin is listed in OpenAI's directory.

## Use with ChatGPT/Codex

The plugin uses `.codex-plugin/plugin.json` and `skills/vectorize/SKILL.md`.
The [official packaging guide](https://developers.openai.com/plugins/build/plugins)
continues to support this compatibility layout.

Install the Python/Node dependencies with [USAGE](USAGE.md), then use Plugin Creator
in a supported client to add this existing folder to your personal marketplace.
Give its absolute path and ask it to preserve other marketplace entries. Only authorize
the local installation changes you intend to make. A working CLI does not itself register
a plugin, and local execution/dependency availability differs between clients.

For an unregistered local test, point the agent directly at
`skills/vectorize/SKILL.md` and supply the input image. Test discovery, invocation and
file delivery in your target client before claiming it is supported.

## Build a clean ZIP

From the plugin root:

```bash
python -m unittest discover -s tests -v
python -m tests.smoke --output-dir /path/to/smoke-results
python scripts/package_plugin.py -o dist/svg-vectorizer.zip
```

The ZIP contains only exact paths in `distribution-files.json`: the manifest, skill,
runtime source, dependency pins, license, docs, tests and demo assets. Plugin files sit
at the archive root, with no extra wrapper directory. It excludes virtual environments,
node_modules, Git metadata, private configuration and unlisted files.

The builder rejects path traversal, symlinks, Windows reparse points, missing required
files and missing referenced icons. It checks inputs before atomically replacing the
ZIP. Fixed entry ordering, timestamps and permissions make repeated builds with the
same input bytes reproducible in the same environment. The printed SHA-256 verifies
transfer integrity, not a security audit.

Extract into a new `svg-vectorizer` folder, install dependencies afresh and repeat the
tests. The ZIP is a source package, not a portable virtual environment or a standalone
Python wheel. Do not upload a review bundle in place of this plugin ZIP.

## Submit to OpenAI yourself

1. Open the [plugin portal](https://platform.openai.com/plugins) and choose the owning
   organization/project and verified developer identity
2. Upload `dist/svg-vectorizer.zip`, then resolve the actual Metadata & Skills findings
3. Submit the checked package for review; publication is a separate step after approval

Follow the [submission guide](https://developers.openai.com/plugins/deploy/submission)
and [plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines).
The selected verified identity controls the directory publisher name; the manifest
alone does not verify an identity. This package has no MCP, app reference or hooks.
Skills-only submission does not need invented MCP tool cases. The current submission
guide says MCP cannot later be added to an existing skills-only plugin, so consider
that boundary before the first submission if a server is genuinely planned.

The public [privacy policy](PRIVACY.md) describes local processing and support email
handling. Do not promise platform-wide privacy based solely on the local CLI.
Windows/macOS native tests and end-to-end skill tests in each intended client remain
separate from Linux CLI verification. A local validator cannot promise directory approval.

## License and provenance

The original MIT license and copyright 2026 Lainterus1 are preserved. This standalone
package was extracted from SVG Vectorizer sources previously maintained in HighGrade;
there is no runtime dependency or included HighGrade adapter. Demo artwork is original
project material. The plugin does not grant rights to other people's input images.

Dependencies are installed separately and retain their licenses: VTracer 1.0.0a4 —
MIT OR Apache-2.0; Pillow 12.3.0 — MIT-CMU; SVGO 4.1.0 — MIT; resvg-js 2.6.2 — MPL-2.0.
Bundling binaries or an environment would require a separate dependency-license review.
