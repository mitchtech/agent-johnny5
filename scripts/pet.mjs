import { createHash } from 'node:crypto';
import { existsSync, lstatSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, renameSync, rmSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

const ID = 'johnny5';
const BUNDLE = resolve(dirname(fileURLToPath(import.meta.url)), '..', 'pets', ID);
const FILES = ['pet.json', 'spritesheet.webp', 'LICENSE.txt', 'NOTICE.md'];
const MARKER = '.agent-johnny5.json';
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
export const NOT_BUNDLED = "Johnny 5 pet art is not bundled yet. Create one with Codex's native pet feature, or watch the repo for a release that includes it.";

export function petPath(env = process.env) {
  return resolve(env.CODEX_HOME || join(homedir(), '.codex'), 'pets', ID);
}

function regular(path) {
  try { return lstatSync(path).isFile(); } catch (error) {
    if (error.code === 'ENOENT') return false;
    throw error;
  }
}

// Missing art is the expected state until a pet ships; it is not an error.
const HEALTHY = ['matching', 'not-installed', 'not-bundled'];

function bundled() {
  return regular(join(BUNDLE, 'pet.json')) && regular(join(BUNDLE, 'spritesheet.webp'));
}

function hashes(directory) {
  return Object.fromEntries(FILES.map(name => [name, regular(join(directory, name)) ? hash(readFileSync(join(directory, name))) : null]));
}

function owned(directory) {
  if (!regular(join(directory, MARKER))) return false;
  try {
    const marker = JSON.parse(readFileSync(join(directory, MARKER), 'utf8'));
    const actual = hashes(directory);
    return marker.owner === 'agent-johnny5' && FILES.every(name => actual[name] && marker.files?.[name] === actual[name])
      && readdirSync(directory).every(name => FILES.includes(name) || name === MARKER);
  } catch { return false; }
}

export function petStatus(env = process.env) {
  const path = petPath(env);
  let entry;
  try { entry = lstatSync(path); } catch (error) {
    if (error.code !== 'ENOENT') throw error;
    return { id: ID, path, state: bundled() ? 'not-installed' : 'not-bundled', managed: false };
  }
  if (!entry.isDirectory() || entry.isSymbolicLink()) return { id: ID, path, state: 'conflict', managed: false };
  // Without bundled art there is nothing to compare, but a managed copy from a release can still be removed.
  if (!bundled()) return { id: ID, path, state: 'not-bundled', managed: owned(path) };
  const actual = hashes(path);
  const expected = hashes(BUNDLE);
  // A manually extracted bundle may have only the two host files. Notices are optional for matching it.
  const matching = FILES.every(name => actual[name] === expected[name] || (!actual[name] && !['pet.json', 'spritesheet.webp'].includes(name)));
  const version = matching ? JSON.parse(readFileSync(join(BUNDLE, 'pet.json'), 'utf8')).spriteVersionNumber ?? null : null;
  return { id: ID, path, state: matching ? 'matching' : 'modified', managed: owned(path), spriteVersionNumber: version };
}

export function installPet(env = process.env, replace = false) {
  const status = petStatus(env);
  if (status.state === 'not-bundled') throw new Error(NOT_BUNDLED);
  if (status.state === 'matching') return { ...status, changed: false };
  if (status.state === 'conflict') throw new Error(`Pet path is not a regular directory: ${status.path}`);
  if (status.state !== 'not-installed' && !replace) throw new Error(`Different pet files at ${status.path}; use --replace to keep a backup and install Johnny 5`);
  const parent = dirname(status.path);
  mkdirSync(parent, { recursive: true });
  const temporary = mkdtempSync(join(parent, '.agent-johnny5-'));
  let backup;
  try {
    for (const name of FILES) writeFileSync(join(temporary, name), readFileSync(join(BUNDLE, name)));
    writeFileSync(join(temporary, MARKER), `${JSON.stringify({ owner: 'agent-johnny5', files: hashes(temporary) }, null, 2)}\n`);
    if (status.state !== 'not-installed') {
      backup = `${status.path}.backup-${temporary.split('.agent-johnny5-').at(-1)}`;
      renameSync(status.path, backup);
    }
    renameSync(temporary, status.path);
  } catch (error) {
    if (backup && !existsSync(status.path)) renameSync(backup, status.path);
    throw error;
  } finally { rmSync(temporary, { recursive: true, force: true }); }
  return { ...petStatus(env), changed: true, ...(backup ? { backup } : {}) };
}

export function uninstallPet(env = process.env) {
  const status = petStatus(env);
  if (status.state === 'not-installed' || (status.state === 'not-bundled' && !existsSync(status.path))) return { ...status, changed: false };
  if (!status.managed) throw new Error(`Refusing to remove unmanaged or changed files at ${status.path}; inspect and remove them manually`);
  // Move out of the live pet directory before removing only the verified owned bundle.
  const temporary = mkdtempSync(join(dirname(status.path), '.agent-johnny5-remove-'));
  try {
    const retired = join(temporary, ID);
    renameSync(status.path, retired);
    if (!owned(retired)) {
      renameSync(retired, status.path);
      throw new Error('Pet files changed during removal; nothing was deleted');
    }
    rmSync(retired, { recursive: true });
  } finally {
    // A failed restoration must preserve the retired directory for manual recovery.
    if (readdirSync(temporary).length === 0) rmSync(temporary, { recursive: true });
  }
  return { ...petStatus(env), changed: true };
}

export function printPetStatus(status = petStatus()) {
  console.log(`Pet: ${status.state} (${status.path})`);
  console.log(`Pet ownership: ${status.managed ? 'managed by agent-johnny5' : 'unmanaged'}`);
  console.log(status.state === 'matching'
    ? 'Select: refresh the desktop pet picker, or enter /pets Johnny 5 in a supported Codex CLI terminal'
    : status.state === 'not-bundled' ? NOT_BUNDLED : 'Install: agent-johnny5 pet install (optional; independent of sounds)');
  return HEALTHY.includes(status.state) ? 0 : 1;
}

export function petMain(argv) {
  const [command, ...args] = argv;
  if (!command || ['--help', '-h'].includes(command)) {
    console.log('agent-johnny5 pet install [--replace]\nagent-johnny5 pet status [--json]\nagent-johnny5 pet uninstall');
    return 0;
  }
  const options = command === 'install' ? { replace: { type: 'boolean', default: false } }
    : command === 'status' ? { json: { type: 'boolean', default: false } } : {};
  const { values } = parseArgs({ args, options });
  let status;
  if (command === 'install') status = installPet(process.env, values.replace);
  else if (command === 'status') status = petStatus();
  else if (command === 'uninstall') status = uninstallPet();
  else throw new Error(`Unknown pet command: ${command}`);
  if (values.json) console.log(JSON.stringify(status, null, 2));
  else {
    if (status.changed !== undefined) console.log(status.changed ? 'Pet files updated.' : 'No pet files changed.');
    if (status.backup) console.log(`Previous pet preserved: ${status.backup}`);
    return printPetStatus(status);
  }
  return HEALTHY.includes(status.state) ? 0 : 1;
}
