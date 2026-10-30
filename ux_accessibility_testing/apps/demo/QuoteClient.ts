import type { APIRequestContext, TestInfo } from '@playwright/test';
import { attachResponse } from '../../framework/api.js';
export class QuoteClient {
  constructor(readonly request: APIRequestContext, readonly info: TestInfo) {}
  async quote(amount: unknown) { return attachResponse(this.info, await this.request.post('/api/quote', { data: { amount } })); }
  async health() { return attachResponse(this.info, await this.request.get('/api/health')); }
}
