import { cpSync, mkdirSync, rmSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
export function buildGemini(out = join(root, 'dist', 'gemini')) {
  mkdirSync(out, { recursive: true });
  for (const name of ['scripts', 'audio', 'pets', 'skills', 'hooks']) rmSync(join(out, name), { recursive: true, force: true });
  for (const name of ['audio', 'pets', 'skills', 'gemini-extension.json', 'LICENSE']) cpSync(join(root, name), join(out, name), { recursive: true });
  mkdirSync(join(out, 'scripts'));
  for (const name of ['johnny5.mjs', 'pet.mjs']) cpSync(join(root, 'scripts', name), join(out, 'scripts', name));
  mkdirSync(join(out, 'hooks'));
  cpSync(join(root, 'hooks', 'gemini.json'), join(out, 'hooks', 'hooks.json'));
  return out;
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) console.log(`Built Gemini extension: ${buildGemini()}`);
