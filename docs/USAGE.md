# Setup and technical reference

## Install

Use the pinned dependencies in the plugin directory. Do not copy a virtual environment
between machines or rely on globally installed npm packages.

Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --only-binary=:all: -r requirements.txt
npm ci --ignore-scripts
.venv/bin/python scripts/vectorize.py input.png -o output.svg --preset logo
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: -r requirements.txt
npm.cmd ci --ignore-scripts
.\.venv\Scripts\python.exe scripts/vectorize.py input.png -o output.svg --preset logo
```

For an optional `vectorize` command, install the editable CLI with the environment's
Python: `python -m pip install -e .`. Reinstall it if the source directory moves.
A standalone wheel with bundled Node dependencies is not provided.

Pinned runtime: VTracer **1.0.0a4** (prerelease), Pillow **12.3.0**, SVGO **4.1.0**,
resvg-js **2.6.2**. Python 3.10+ and Node.js 20+ are required. Binary dependency
availability can vary by platform. Current verification covers Linux; earlier Windows
results do not establish support for each new revision.

## Options

| Option | Meaning |
|---|---|
| `input` | PNG, JPG/JPEG or WebP; content must match the extension |
| `-o, --output` | Required `.svg` destination |
| `--preset` | `auto` (default), `logo`, `icon`, `illustration`, `line-art` |
| `--colors` | 2–256 input colors; explicit values also constrain traced color fills |
| `--simplify` | 0–10; higher values simplify curves more |
| `--filter-speckle` | 0–10000 source pixels; 0 keeps small components |
| `--scale` | 1 or 2; changes tracing resolution, not final SVG dimensions |
| `--no-optimize` | Skip SVGO only; XML and render validation still run |
| `--verbose` | Print preset and pipeline stages |

Use quoted absolute paths when paths contain spaces. User options override preset defaults.
`line-art` accepts only 2 colors. Alpha-mask gray levels are separate from the color palette.

## Presets

| Preset | Input colors | Simplify | Speckle | Scale |
|---|---:|---:|---:|---:|
| `logo` | 8 | 7 | 8 | 1 |
| `icon` | 6 | 8 | 4 | 1 |
| `illustration` | 128 | 2 | size-based, 0–4 | 2 |
| `line-art` | 2 | 1 | 2 | 1 |

`auto` uses a bounded pixel sample. Nearly monochrome artwork is classified as line art;
low-color artwork becomes an icon up to 256 px, otherwise a logo; the remainder becomes
an illustration. This is a heuristic, and an explicit preset is often better.

Illustration uses Lanczos upscaling before median-cut quantization, stacked VTracer tracing
and SVGO. Its speckle threshold is `min(4, max(width, height) // 320)` source pixels.
Explicit `--filter-speckle` overrides it. Speckle scales once with the tracing scale.

The simplify scale is not a pixel-error guarantee. Illustration uses a length threshold
of `(2.5 + 0.25 × simplify) × scale` and extra simplification `simplify × scale / 4`;
other presets use `(3.5 + 0.65 × simplify) × scale`.

Line art uses autocontrast and a 180/255 threshold. Its result contains filled contours,
not centerline strokes. An opaque white background stays white.

## Safety and limitations

- EXIF orientation is applied without modifying the input. Animated images are rejected
- Input and upscaled images are limited to 16 megapixels. Illustration at 2× requires
  an input of at most 4 megapixels; choose `--scale 1` explicitly for larger images
- Transparency is represented with a vector luminance mask, never an embedded raster
- Only the generated SVG element/attribute subset is accepted. Active content, external
  references, arbitrary CSS, DTDs, entities and processing instructions are rejected
- Before/after SVGO renders must differ by no more than 2/255 in any channel. An opaque
  input must not gain transparent gaps. An unexpectedly empty output is rejected
- Existing output is replaced atomically after validation. On failure it stays unchanged;
  a successful replacement does not retain a backup of the previous output
- The Node helper has a 120-second timeout. VTracer's Python API has no separate timeout;
  complex or noisy images can still take substantial time and memory
- Alpha masks can retain pixel steps and increase SVG size. There is no OCR, font recovery,
  print-grade ICC/CMYK guarantee or promise of exact brand geometry

A successful render check proves readable SVG and preservation through optimization,
not artistic equivalence to the raster. Inspect important details visually and reduce
speckle filtering/simplification when needed.

## Errors and checks

Exit codes: **0** success, **1** pipeline failure, **2** invalid CLI syntax. Errors are
printed to stderr with dependency/fix guidance. Missing tools are not downloaded during
conversion, and failures are never replaced with hand-drawn paths or embedded PNGs.

From the plugin root, using its Python environment:

```bash
python -m unittest discover -s tests -v
python -m tests.smoke --output-dir /path/to/smoke-results
python scripts/package_plugin.py -o dist/svg-vectorizer.zip
```

The tests exercise actual VTracer, SVGO and resvg, including transparency, palette limits,
EXIF, presets, failures and output preservation. Fast standard-library tests can run without
native dependencies: `python -m unittest tests.test_validation tests.test_distribution -v`.

See [distribution](DISTRIBUTION.md), [privacy](PRIVACY.md) and the
[reproducible visual example](../examples/README.md).
