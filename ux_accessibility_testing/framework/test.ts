import { test as base, expect, type Page, type TestInfo } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
export type Coverage = { rule: string; selector: string[]; detail: string };
export async function scan(page: Page, info: TestInfo, state: string, negativeControl = false) {
  const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice']).analyze();
  await info.attach('axe-evidence', { body: JSON.stringify({ state, negativeControl, results }), contentType: 'application/json' });
  return results;
}
export const test = base.extend<{ record: (coverage: Coverage) => Promise<void> }>({
  page: async ({ page, browser, browserName, isMobile, hasTouch }, use, info) => {
    await info.attach('runtime-environment', { body: JSON.stringify({ browserName, browserVersion: browser.version(), viewport: page.viewportSize(), isMobile: !!isMobile, hasTouch: !!hasTouch, userAgent: await page.evaluate(() => navigator.userAgent), devicePixelRatio: await page.evaluate(() => devicePixelRatio), physicalDevice: false }), contentType: 'application/json' });
    await use(page);
  },
  record: async ({}, use, info) => {
    await use(async coverage => { await info.attach('coverage', { body: JSON.stringify(coverage), contentType: 'application/json' }); });
  }
});
export { expect };
