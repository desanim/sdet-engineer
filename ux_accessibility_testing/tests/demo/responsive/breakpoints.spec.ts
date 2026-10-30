import { test, expect } from '../../../apps/demo/fixtures.js';
import { scan } from '../../../framework/test.js';
test('RESP-02 @responsive breakpoint sweep and 320px scans', async ({ page, swap, record }, info) => {
  // One desktop project owns CSS breakpoint sweeps; device projects keep their own viewport.
  await record({ rule: 'RESP-02', selector: ['html', '#amount', '#review-dialog', '#confirm'], detail: '320/375/768/1024/1440 CSS px in default and dialog states; 320px axe scan.' });
  for (const width of [320, 375, 768, 1024, 1440]) {
    await page.setViewportSize({ width, height: 900 }); await swap.goto();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    if (width === 320) expect((await scan(page, info, '320px-default')).violations).toEqual([]);
    await swap.openReview();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    await expect(swap.confirm).toBeInViewport();
    if (width === 320) expect((await scan(page, info, '320px-dialog')).violations).toEqual([]);
    await swap.cancel.click();
  }
});
