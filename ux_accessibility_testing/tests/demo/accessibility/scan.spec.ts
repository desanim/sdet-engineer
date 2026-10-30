import { test, expect } from '../../../apps/demo/fixtures.js';
import { scan } from '../../../framework/test.js';
test.beforeEach(async ({ swap }) => { await swap.goto(); });
test('AXE-01 @a11y @smoke default page structure and scan', async ({ page, record }, info) => {
  await record({ rule: 'AXE-01', selector: ['header', 'nav', 'main', 'h1', 'footer'], detail: 'One main heading and expected landmarks; zero axe violations.' });
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Review a token swap');
  for (const role of ['banner', 'navigation', 'main', 'contentinfo'] as const) await expect(page.getByRole(role)).toHaveCount(1);
  expect((await scan(page, info, 'default')).violations).toEqual([]);
});
test('AXE-02 @a11y validation and open dialog scans', async ({ page, swap, record }, info) => {
  await record({ rule: 'AXE-02', selector: ['#amount-error', '#review-dialog'], detail: 'Error and dialog states scanned independently; incomplete nodes remain Needs review.' });
  await swap.review.click();
  await expect(page.locator('#amount-error')).toBeVisible();
  expect((await scan(page, info, 'validation-error')).violations).toEqual([]);
  await swap.openReview();
  await expect(swap.dialog).toHaveAccessibleName('Confirm simulated swap');
  expect((await scan(page, info, 'dialog-open')).violations).toEqual([]);
});
test('CONTROL-01 @a11y unnamed-button negative control', async ({ page, record }, info) => {
  await record({ rule: 'CONTROL-01', selector: ['#negative-control'], detail: 'Isolated injected defect must be reported by button-name.' });
  await page.locator('main').evaluate(el => { const button = document.createElement('button'); button.id = 'negative-control'; el.append(button); });
  const results = await scan(page, info, 'injected-missing-button-name', true);
  expect(results.violations.some(v => v.id === 'button-name' && v.nodes.some(n => n.target.includes('#negative-control')))).toBe(true);
});
