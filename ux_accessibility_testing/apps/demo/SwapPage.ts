import { expect, type Page } from '@playwright/test';
export class SwapPage {
  constructor(readonly page: Page) {}
  get amount() { return this.page.getByRole('spinbutton', { name: 'Amount in ETH', exact: true }); }
  get review() { return this.page.getByRole('button', { name: 'Review swap', exact: true }); }
  get dialog() { return this.page.getByRole('dialog', { name: 'Confirm simulated swap' }); }
  get cancel() { return this.page.getByRole('button', { name: 'Cancel', exact: true }); }
  get confirm() { return this.page.getByRole('button', { name: 'Confirm simulation', exact: true }); }
  get status() { return this.page.getByRole('status', { name: 'Simulation result' }); }
  async goto() { await this.page.goto('/'); }
  async openReview(amount = '1.5') {
    await this.amount.fill(amount); await this.review.click(); await expect(this.dialog).toBeVisible();
  }
}
