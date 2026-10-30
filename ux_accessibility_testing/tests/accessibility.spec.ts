import { test, expect, type Page, type TestInfo } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

async function scan(page: Page, info: TestInfo, state: string, negativeControl = false) {
  const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice']).analyze();
  await info.attach('axe-evidence', { body: JSON.stringify({ state, negativeControl, results }), contentType: 'application/json' });
  return results;
}
async function tabTo(page: Page, selector: string) {
  await page.keyboard.press('Tab');
  await expect(page.locator(selector)).toBeFocused();
}
async function openReview(page: Page) {
  await page.locator('#amount').fill('1.5');
  await page.locator('#review').click();
  await expect(page.getByRole('dialog')).toBeVisible();
}
test.beforeEach(async ({ page }) => { await page.goto('/'); });

test('AXE-01 default page and landmark structure', async ({ page }, info) => {
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Review a token swap');
  await expect(page.getByRole('banner')).toHaveCount(1);
  await expect(page.getByRole('navigation', { name: 'Main', exact: true })).toHaveCount(1);
  await expect(page.getByRole('main')).toHaveCount(1);
  await expect(page.getByRole('contentinfo')).toHaveCount(1);
  expect((await scan(page, info, 'default')).violations).toEqual([]);
});

test('KEY-01 keyboard-only focus order and skip link', async ({ page }) => {
  for (const selector of ['#skip', '#nav-swap', '#nav-about', '#amount', '#review']) await tabTo(page, selector);
  await page.reload();
  await tabTo(page, '#skip');
  await expect(page.locator('#skip')).toBeInViewport();
  await page.keyboard.press('Enter');
  await expect(page.locator('#main')).toBeFocused();
  await tabTo(page, '#amount');
  await page.keyboard.type('1.5');
  await tabTo(page, '#review');
  await page.keyboard.press('Enter');
  await expect(page.locator('#cancel')).toBeFocused();
  await tabTo(page, '#confirm');
  await page.keyboard.press('Enter');
  await expect(page.getByRole('dialog')).not.toBeVisible();
  await expect(page.locator('#review')).toBeFocused();
  await expect(page.getByRole('status', { name: 'Simulation result' })).toHaveText('Simulation complete. No transaction was broadcast.');
});

test('FORM-01 label association, invalid states and recovery', async ({ page }, info) => {
  const input = page.getByRole('spinbutton', { name: 'Amount in ETH', exact: true });
  await expect(input).toHaveAttribute('id', 'amount');
  await page.locator('label[for="amount"]').click();
  await expect(input).toBeFocused();
  for (const value of ['', '0', '-1', '6']) {
    await input.fill(value);
    await page.locator('#review').click();
    await expect(input).toBeFocused();
    await expect(input).toHaveAttribute('aria-invalid', 'true');
    await expect(input).toHaveAccessibleDescription(/Enter an amount greater than 0 and no more than 5 ETH/);
    await expect(page.locator('#amount-error')).toBeVisible();
    await expect(page.getByRole('dialog')).not.toBeVisible();
  }
  expect((await scan(page, info, 'validation-error')).violations).toEqual([]);
  await input.fill('1.5');
  await expect(input).not.toHaveAttribute('aria-invalid');
  await expect(page.locator('#amount-error')).toBeHidden();
  await expect(page.locator('#estimate')).toHaveText('4686.75');
  await page.locator('#review').click();
  await expect(page.getByRole('dialog')).toHaveAccessibleName('Confirm simulated swap');
  await expect(page.locator('#dialog-description')).toContainText('1.5 ETH for 4686.75 USDC');
});

test('DIALOG-01 scan, bidirectional focus containment, Escape and return', async ({ page }, info) => {
  await openReview(page);
  await expect(page.locator('#cancel')).toBeFocused();
  expect((await scan(page, info, 'dialog-open')).violations).toEqual([]);
  await page.keyboard.press('Shift+Tab');
  await expect(page.locator('#confirm')).toBeFocused();
  await tabTo(page, '#cancel');
  await tabTo(page, '#confirm');
  await tabTo(page, '#cancel');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog')).not.toBeVisible();
  await expect(page.locator('#review')).toBeFocused();
  await page.keyboard.press('Enter');
  await page.keyboard.press('Enter'); // initially focused Cancel
  await expect(page.getByRole('dialog')).not.toBeVisible();
  await expect(page.locator('#review')).toBeFocused();
});

test('RESP-01 reflow smoke at 320 CSS px, default and dialog', async ({ page }, info) => {
  await page.setViewportSize({ width: 320, height: 800 });
  const noOverflow = async () => {
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  };
  await noOverflow();
  await expect(page.locator('#amount')).toBeInViewport();
  expect((await scan(page, info, '320px-default')).violations).toEqual([]);
  await openReview(page);
  await noOverflow();
  await expect(page.locator('#confirm')).toBeInViewport();
  expect((await scan(page, info, '320px-dialog')).violations).toEqual([]);
});

test('CONTROL-01 detector catches injected missing label', async ({ page }, info) => {
  // Test-local mutation only: confirms scanner + evidence path are not silently empty.
  await page.locator('main').evaluate(el => {
    const button = document.createElement('button'); button.id = 'negative-control'; el.append(button);
  });
  const results = await scan(page, info, 'injected-missing-button-name', true);
  expect(results.violations.some(v => v.id === 'button-name' && v.nodes.some(n => n.target.includes('#negative-control')))).toBe(true);
});
