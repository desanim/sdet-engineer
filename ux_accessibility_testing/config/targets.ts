import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
const moduleRoot = fileURLToPath(new URL('../', import.meta.url));

// Register application adapters here; shared framework code has no app selectors.
const registry = {
  demo: { testDir: './tests/demo', manualReview: './apps/demo/manual-review.json' }
};
export function loadTarget() {
  const app = process.env.TEST_APP ?? 'demo';
  if (!(app in registry)) throw new Error(`Unknown TEST_APP: ${app}. Register an adapter in config/targets.ts.`);
  const adapter = registry[app as keyof typeof registry];
  if (!process.env.BASE_URL && (app !== 'demo' || process.env.API_BASE_URL)) {
    throw new Error('Set BASE_URL for a remote adapter or when overriding API_BASE_URL. Omit both URLs to run the local demo.');
  }
  const baseURL = process.env.BASE_URL ?? 'http://127.0.0.1:4173';
  const apiBaseURL = process.env.API_BASE_URL ?? baseURL;
  for (const value of [baseURL, apiBaseURL]) {
    const url = new URL(value);
    if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.search || url.hash) {
      throw new Error('BASE_URL/API_BASE_URL must be HTTP(S) URLs without credentials, query or fragment.');
    }
  }
  return { app, baseURL, apiBaseURL,
    startDemo: !process.env.BASE_URL && !process.env.API_BASE_URL && app === 'demo',
    testDir: resolve(moduleRoot, adapter.testDir), manualReview: resolve(moduleRoot, adapter.manualReview) };
}
