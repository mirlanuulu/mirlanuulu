// Кадры вращающегося ASCII-глобуса. Кыргызстан помечается классом "kg".
import fs from 'fs';
import { geoOrthographic, geoContains } from 'd3-geo';
import { feature } from 'topojson-client';

const topo = JSON.parse(fs.readFileSync('node_modules/world-atlas/countries-50m.json', 'utf8'));
const land = feature(topo, topo.objects.land);
const countries = feature(topo, topo.objects.countries);
const kg = countries.features.find((f) => f.id === '417');

const COLS = 46, ROWS = 23, FRAMES = 48, TILT = -22;
const RAMP = '.:-=+*#%@';
const L = (() => { const v = [-0.45, -0.5, 0.74]; const n = Math.hypot(...v); return v.map((x) => x / n); })();

const frames = [];
for (let f = 0; f < FRAMES; f++) {
  // старт так, чтобы Кыргызстан (≈74.5° в.д.) был в центре на первом кадре
  const lambda = -74.5 + (360 * f) / FRAMES;
  const proj = geoOrthographic().scale(1).translate([0, 0]).rotate([lambda, TILT]).clipAngle(90);
  const rows = [];
  for (let i = 0; i < ROWS; i++) {
    const runs = [];
    const push = (cls, ch) => {
      const last = runs[runs.length - 1];
      if (last && last[0] === cls) last[1] += ch; else runs.push([cls, ch]);
    };
    for (let j = 0; j < COLS; j++) {
      const x = (j + 0.5 - COLS / 2) / (COLS / 2);
      const y = (i + 0.5 - ROWS / 2) / (ROWS / 2);
      const r2 = x * x + y * y;
      if (r2 >= 1) { push('a', ' '); continue; }
      const z = Math.sqrt(1 - r2);
      const ll = proj.invert([x, y]);
      const lit = Math.max(0, x * L[0] + y * L[1] + z * L[2]);
      if (ll && geoContains(land, ll)) {
        const ch = RAMP[Math.min(RAMP.length - 1, Math.floor((0.25 + 0.75 * lit) * RAMP.length))];
        push(kg && geoContains(kg, ll) ? 'kg' : 'a', ch);
      } else {
        // океан: редкие точки, гуще к краю — чтобы читалась сфера
        const rim = r2 > 0.86;
        const dot = rim || ((i * 7 + j * 3 + f) % 11 === 0 && lit > 0.35);
        push('o', dot ? (rim ? '.' : '·') : ' ');
      }
    }
    rows.push(runs);
  }
  frames.push(rows);
}
fs.writeFileSync(process.argv[2] || 'frames.json', JSON.stringify({ cols: COLS, rows: ROWS, frames }));
console.log('frames', frames.length);
