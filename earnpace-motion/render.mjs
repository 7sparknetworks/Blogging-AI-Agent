// Usage: node render.mjs stills <outdir> t1 t2 ...   |   node render.mjs video <out.mp4> [audio.wav]
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const [mode, out, ...rest] = process.argv.slice(2);
const here = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch({ args: ['--disable-gpu-vsync'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
page.on('pageerror', e => { console.error('PAGE ERROR', e); process.exit(1); });
await page.goto('file://' + path.join(here, 'index.html'));
await page.evaluate(() => window.ready);
const grab = t => page.evaluate(t => { renderFrame(t); return document.getElementById('c').toDataURL('image/png').split(',')[1]; }, t);

if (mode === 'stills') {
  for (const t of rest) writeFileSync(path.join(out, `t${(+t).toFixed(2)}.png`), Buffer.from(await grab(+t), 'base64'));
} else {
  const { DUR, FPS } = await page.evaluate(() => ({ DUR, FPS }));
  const n = Math.round(DUR * FPS);
  const audio = rest[0];
  const args = ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    ...(audio ? ['-i', audio, '-c:a', 'aac', '-b:a', '256k', '-shortest'] : []),
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out];
  const ff = spawn('ffmpeg', args, { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) {
    const buf = Buffer.from(await grab(i / FPS), 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 120 === 0) console.log(`frame ${i}/${n}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
}
await browser.close();
