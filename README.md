# SVG Vectorizer

**Turn PNG, JPG and WebP artwork into scalable SVG files.**

Have a logo or drawing but only a raster image? SVG Vectorizer traces it into real
vector paths you can resize, recolor and edit in design tools. It runs locally and
fits into ChatGPT/Codex as a skills-only plugin.

![A real PNG-to-SVG conversion with SVG Vectorizer](examples/before-after.png)

*Left: the 512 × 512 PNG input. Right: the SVG produced by this plugin, with no manual
path editing. [View the SVG](examples/demo-output.svg) · [Reproduce the example](examples/README.md)*

## When it helps

- Prepare a raster logo or icon for a website or app
- Convert flat-color artwork into editable vector shapes
- Trace line drawings while retaining transparent areas

Best for clear shapes and limited colors. Photos, gradients and tiny text may produce
large or simplified results. Tracing is an approximation, not recovery of the original design file.

## Quick start

Requires **Python 3.10+** and **Node.js 20+**. From the plugin folder on Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --only-binary=:all: -r requirements.txt
npm ci --ignore-scripts
.venv/bin/python scripts/vectorize.py input.png -o output.svg --preset logo
```

Choose `logo`, `icon`, `illustration` or `line-art`; omit the preset for automatic selection.
[Windows setup, options and tests →](docs/USAGE.md)

## How it works

**VTracer** builds paths → **SVGO** optimizes them → **XML checks and resvg** validate the result.
The output replaces its destination only after validation succeeds. Conversion makes no network
requests after dependencies are installed. No API key, MCP server or background service is needed.

This repository is the standalone source package. Installing its dependencies does not register
it in ChatGPT/Codex; follow the [plugin packaging guide](docs/DISTRIBUTION.md).

**Version:** 0.1.1 · **License:** [MIT](LICENSE) · **Publisher:** Daniil
**Support:** gonchardaniil1998@gmail.com · [Privacy policy](docs/PRIVACY.md)
