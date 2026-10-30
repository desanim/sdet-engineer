import { test as base } from '../../framework/test.js';
import { SwapPage } from './SwapPage.js';
import { QuoteClient } from './QuoteClient.js';
export const test = base.extend<{ swap: SwapPage; quotes: QuoteClient }>({
  swap: async ({ page }, use) => { await use(new SwapPage(page)); },
  quotes: async ({ request }, use, info) => { await use(new QuoteClient(request, info)); }
});
export { expect } from '../../framework/test.js';
