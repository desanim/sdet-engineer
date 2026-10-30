import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests', fullyParallel: true, forbidOnly: !!process.env.CI,
  retries: 0, timeout: 30000,
  outputDir: 'reports/playwright/artifacts',
  reporter: [['list'], ['html', { outputFolder: 'reports/playwright/html', open: 'never' }], ['./tests/evidence-reporter.ts']],
  use: { baseURL: 'http://127.0.0.1:4173', trace: 'retain-on-failure', screenshot: 'only-on-failure' },
  projects: [
    { name: 'chromium-desktop', use: { browserName: 'chromium', viewport: { width: 1280, height: 800 } } },
    { name: 'chromium-mobile', use: { browserName: 'chromium', viewport: { width: 375, height: 812 }, isMobile: true, hasTouch: true } }
  ],
  webServer: { command: 'npm run demo', url: 'http://127.0.0.1:4173', reuseExistingServer: false }
});
