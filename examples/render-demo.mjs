// Own code-native logo artwork -> raster fixture, then a truthful before/after plate.
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {Resvg} from '@resvg/resvg-js';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(here);
const render=svg=>new Resvg(svg,{font:{loadSystemFonts:true,defaultFontFamily:'DejaVu Sans'}}).render().asPng();
if(process.argv[2]==='input'){
  fs.writeFileSync(path.join(here,'demo-input.png'),new Resvg(fs.readFileSync(path.join(root,'assets/logo.svg'),'utf8'),{background:'#ffffff',font:{loadSystemFonts:false}}).render().asPng());
}else if(process.argv[2]==='preview'){
  const png=fs.readFileSync(path.join(here,'demo-input.png')).toString('base64');
  const actual=fs.readFileSync(path.join(here,'demo-output.svg'),'utf8');
  const vector=actual.replace(/<svg\b/, '<svg x="865" y="287"').replace('width="512"','width="390"').replace('height="512"','height="390"');
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="960" viewBox="0 0 1440 960">
<rect width="1440" height="960" fill="#eef3ef"/>
<g font-family="DejaVu Sans, sans-serif" fill="#183e34">
<circle cx="73" cy="66" r="7" fill="#56876a"/><text x="93" y="72" font-size="17" font-weight="bold" letter-spacing="2">SVG VECTORIZER</text>
<text x="64" y="159" font-size="66" font-weight="bold" letter-spacing="-2">Pixels in. Paths out.</text>
<text x="66" y="205" font-size="23" fill="#547064">Turn raster artwork into SVG paths for websites, apps and design tools.</text>
<rect x="64" y="250" width="640" height="554" rx="27" fill="white" stroke="#dae5dc"/>
<rect x="736" y="250" width="640" height="554" rx="27" fill="white" stroke="#bacebe"/>
<text x="96" y="294" font-size="16" font-weight="bold" letter-spacing="2" fill="#718477">BEFORE</text>
<text x="768" y="294" font-size="16" font-weight="bold" letter-spacing="2" fill="#416750">AFTER</text>
<text x="672" y="294" text-anchor="end" font-size="15" fill="#547064">PNG · 512 × 512</text>
<text x="1344" y="294" text-anchor="end" font-size="15" fill="#416750">SVG · actual traced output</text>
<image x="193" y="317" width="390" height="390" href="data:image/png;base64,${png}"/>
<g transform="translate(0 30)">${vector}</g>
<text x="96" y="750" font-size="28" font-weight="bold">The raster image</text>
<text x="768" y="750" font-size="28" font-weight="bold">Editable vector paths</text>
<text x="96" y="782" font-size="17" fill="#668073">A fixed-resolution PNG is the only input.</text>
<text x="768" y="782" font-size="17" fill="#668073">Traced, optimized and render-checked locally.</text>
<text x="68" y="846" font-size="18" fill="#416750">✓ Local conversion     ✓ Real SVG geometry     ✓ No manual path editing</text>
<line x1="64" y1="875" x2="1376" y2="875" stroke="#d6e1d8"/>
<text x="66" y="902" font-size="14" fill="#708276">Actual plugin run · logo preset · simplify 1 · speckle filter 0 · self-created demonstration artwork</text>
<text x="66" y="927" font-size="14" fill="#708276">Tracing approximates the raster. It does not recover the original design file.</text>
</g></svg>`;
  fs.writeFileSync(path.join(here,'before-after.svg'),svg);
  fs.writeFileSync(path.join(here,'before-after.png'),render(svg));
}else{throw new Error('Usage: node examples/render-demo.mjs input|preview');}
