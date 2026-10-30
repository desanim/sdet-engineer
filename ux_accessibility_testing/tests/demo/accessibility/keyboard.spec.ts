import { test, expect } from '../../../apps/demo/fixtures.js';
test.beforeEach(async ({ swap }) => { await swap.goto(); });
test('KEY-01 @a11y keyboard-only order, skip and completion', async ({ page, swap, record }) => {
  await record({ rule: 'KEY-01', selector: ['#skip', '#nav-swap', '#nav-about', '#main', '#amount', '#review', '#cancel', '#confirm'], detail: 'Exact Tab sequence, skip link focus transfer and keyboard-only simulation.' });
  for (const selector of ['#skip', '#nav-swap', '#nav-about', '#amount', '#review']) {
    await page.keyboard.press('Tab'); await expect(page.locator(selector)).toBeFocused();
  }
  await page.reload(); await page.keyboard.press('Tab');
  await expect(page.locator('#skip')).toBeInViewport();
  await page.keyboard.press('Enter'); await expect(page.locator('#main')).toBeFocused();
  await page.keyboard.press('Tab'); await expect(swap.amount).toBeFocused();
  await page.keyboard.type('1.5'); await page.keyboard.press('Tab'); await expect(swap.review).toBeFocused();
  await page.keyboard.press('Enter'); await expect(swap.cancel).toBeFocused();
  await page.keyboard.press('Tab'); await expect(swap.confirm).toBeFocused();
  await page.keyboard.press('Enter'); await expect(swap.dialog).not.toBeVisible();
  await expect(swap.review).toBeFocused();
  await expect(swap.status).toHaveText('Simulation complete. No transaction was broadcast.');
});
test('KEY-02 @a11y dialog Tab boundaries, Escape, Cancel and focus return', async ({ page, swap, record }) => {
  await record({ rule: 'KEY-02', selector: ['#review-dialog', '#cancel', '#confirm', '#review'], detail: 'Initial focus, bidirectional containment, Escape and Cancel restore trigger.' });
  await swap.openReview(); await expect(swap.cancel).toBeFocused();
  await page.keyboard.press('Shift+Tab'); await expect(swap.confirm).toBeFocused();
  await page.keyboard.press('Tab'); await expect(swap.cancel).toBeFocused();
  await page.keyboard.press('Tab'); await expect(swap.confirm).toBeFocused();
  await page.keyboard.press('Tab'); await expect(swap.cancel).toBeFocused();
  await page.keyboard.press('Escape'); await expect(swap.dialog).not.toBeVisible(); await expect(swap.review).toBeFocused();
  await page.keyboard.press('Enter'); await expect(swap.cancel).toBeFocused();
  await page.keyboard.press('Enter'); await expect(swap.dialog).not.toBeVisible(); await expect(swap.review).toBeFocused();
});
