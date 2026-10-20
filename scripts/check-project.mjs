import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const json = name => JSON.parse(readFileSync(join(root, name), 'utf8'));
const version = json('package.json').version;
for (const name of ['plugin.json', '.claude-plugin/plugin.json', 'gemini-extension.json']) assert.equal(json(name).version, version, `${name}: version mismatch`);
assert.ok(!existsSync(join(root, 'hooks', 'hooks.json')), 'The source package must not double-register default hooks');
for (const name of readdirSync(join(root, 'skills'))) {
  const skill = readFileSync(join(root, 'skills', name, 'SKILL.md'), 'utf8');
  assert.match(skill, /disable-model-invocation: false/);
  assert.match(skill, /TRIGGER when:/);
  assert.match(skill, /DO NOT TRIGGER when:/);
}
if (process.env.GITHUB_REF_TYPE === 'tag') assert.equal(process.env.GITHUB_REF_NAME, `v${version}`, 'Release tag must match package version');
console.log(`Project metadata and skills verified: v${version}`);
