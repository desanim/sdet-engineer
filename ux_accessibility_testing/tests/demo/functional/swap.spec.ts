import { test, expect } from '../../../apps/demo/fixtures.js';
test.beforeEach(async ({ swap }) => { await swap.goto(); });

test('UI-01 @functional @smoke quote API to confirmed simulation', async ({ swap, page, record }) => {
  await record({ rule: 'UI-01', selector: ['#amount', '#review', '#review-dialog', '#status'], detail: 'Real local quote response is used by the dialog, then simulation succeeds.' });
  const quoteResponse = page.waitForResponse(r => r.url().endsWith('/api/quote') && r.request().method() === 'POST');
  await swap.openReview('1.5');
  const response = await quoteResponse;
  expect(response.status()).toBe(200);
  expect(await response.json()).toMatchObject({ amount: 1.5, receive: 4686.75, simulated: true });
  await expect(page.locator('#dialog-description')).toContainText('1.5 ETH for 4686.75 USDC');
  await swap.confirm.click();
  await expect(swap.dialog).not.toBeVisible();
  await expect(swap.review).toBeFocused();
  await expect(swap.status).toHaveText('Simulation complete. No transaction was broadcast.');
});

test('UI-02 @functional rejects invalid boundaries and recovers', async ({ swap, page, record }) => {
  await record({ rule: 'UI-02', selector: ['#amount', '#amount-error', '#review-dialog'], detail: 'Invalid values do not send quote requests; valid correction clears error.' });
  let quoteCalls = 0;
  page.on('request', r => { if (new URL(r.url()).pathname === '/api/quote') quoteCalls++; });
  await page.locator('label[for="amount"]').click();
  await expect(swap.amount).toBeFocused();
  for (const value of ['', '0', '-1', '6', '0.0000001']) {
    await swap.amount.fill(value); await swap.review.click();
    await expect(swap.amount).toBeFocused();
    await expect(swap.amount).toHaveAttribute('aria-invalid', 'true');
    await expect(swap.amount).toHaveAccessibleDescription(/Enter an amount greater than 0 and no more than 5 ETH/);
    await expect(page.locator('#amount-error')).toBeVisible();
    await expect(swap.dialog).not.toBeVisible();
  }
  expect(quoteCalls).toBe(0);
  await swap.openReview('5');
  await expect(swap.amount).not.toHaveAttribute('aria-invalid');
  await expect(page.locator('#amount-error')).toBeHidden();
  await expect(page.locator('#dialog-description')).toContainText('5 ETH for 15622.50 USDC');
});

test('UI-03 @functional quote failure permits retry', async ({ swap, page, record }) => {
  await record({ rule: 'UI-03', selector: ['#status', '#review', '#review-dialog'], detail: '503 response shows error, re-enables controls and retry succeeds.' });
  await page.route('**/api/quote', route => route.fulfill({ status: 503, json: { error: 'unavailable' } }));
  await swap.amount.fill('1'); await swap.review.click();
  await expect(swap.status).toHaveText('Quote unavailable. Please try again.');
  await expect(swap.dialog).not.toBeVisible();
  await expect(swap.review).toBeEnabled();
  await expect(swap.amount).toBeEditable();
  await page.unroute('**/api/quote');
  await swap.review.click(); await expect(swap.dialog).toBeVisible();
});
