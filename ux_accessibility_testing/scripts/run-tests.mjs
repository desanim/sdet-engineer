// Cross-platform env selection without shell-specific VAR=value syntax.
import { spawnSync } from 'node:child_process';
const [mode = 'smoke', ...args] = process.argv.slice(2);
if (!['smoke', 'full'].includes(mode)) throw new Error('Expected smoke or full');
const result = spawnSync(process.execPath, ['node_modules/@playwright/test/cli.js', 'test', ...args], {
  stdio: 'inherit', env: { ...process.env, TEST_MATRIX: mode }
});
if (result.error) throw result.error;
process.exit(result.status ?? 1);
