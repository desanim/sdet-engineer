import { test, expect } from '../../../apps/demo/fixtures.js';
test('RESP-01 @responsive @smoke profile layout and pointer interaction', async ({ swap, page, hasTouch, record }, info) => {
  await record({ rule: 'RESP-01', selector: ['html', 'nav', '#amount', '#review-dialog', '#confirm'], detail: 'Configured viewport is preserved; no horizontal overflow; touch profiles use tap.' });
  await swap.goto();
  const viewport = page.viewportSize()!;
  expect(viewport).toEqual(info.project.use.viewport);
  const noOverflow = async () => expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await noOverflow(); await expect(page.getByRole('navigation')).toBeVisible();
  await swap.amount.fill('1');
  if (hasTouch) await swap.review.tap(); else await swap.review.click();
  await expect(swap.dialog).toBeVisible(); await noOverflow();
  await expect(swap.confirm).toBeInViewport();
  if (hasTouch) await swap.cancel.tap(); else await swap.cancel.click();
  await expect(swap.dialog).not.toBeVisible();
  await info.attach('profile-layout', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
});
