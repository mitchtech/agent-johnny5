import { cpSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const out = join(root, 'dist', 'site');
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
cpSync(join(root, 'site'), out, { recursive: true });
const { version } = JSON.parse(readFileSync(join(root, 'package.json'), 'utf8'));
const html = readFileSync(join(out, 'index.html'), 'utf8').replaceAll('__VERSION__', version);
writeFileSync(join(out, 'index.html'), html);
cpSync(join(root, 'audio'), join(out, 'audio'), { recursive: true });
cpSync(join(root, 'assets', 'previews'), join(out, 'previews'), { recursive: true });
if (existsSync(join(root, 'assets', 'exports'))) cpSync(join(root, 'assets', 'exports'), join(out, 'exports'), { recursive: true });
console.log(`Built site: ${out}`);
