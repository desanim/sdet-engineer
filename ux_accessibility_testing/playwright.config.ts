import { defineConfig } from '@playwright/test';
import { fileURLToPath } from 'node:url';
import { loadTarget } from './config/targets.js';
import { projectsFor } from './config/devices.js';
const target = loadTarget();
const mode = process.env.TEST_MATRIX ?? 'smoke';
if (!['smoke', 'full'].includes(mode)) throw new Error('TEST_MATRIX must be smoke or full');
const reportDir = fileURLToPath(new URL(`./reports/playwright/${target.app}/${mode}`, import.meta.url));
export default defineConfig({
  testDir: target.testDir, fullyParallel: true, forbidOnly: !!process.env.CI,
  retries: 0, timeout: 30000, workers: process.env.CI ? 2 : undefined,
  grep: mode === 'smoke' ? /@smoke/ : undefined,
  outputDir: `${reportDir}/artifacts`,
  reporter: [['list'], ['html', { outputFolder: `${reportDir}/html`, open: 'never' }],
    ['./framework/reporting/evidence-reporter.ts', { reportDir, target, mode }]],
  metadata: { app: target.app, matrix: mode, execution: 'browser emulation; no physical devices' },
  use: { baseURL: target.baseURL, trace: 'retain-on-failure', screenshot: 'only-on-failure' },
  projects: projectsFor(mode, target.apiBaseURL),
  webServer: target.startDemo ? { command: 'npm run demo', url: 'http://127.0.0.1:4173/api/health', reuseExistingServer: false } : undefined
});
