import { test, expect } from '../../../apps/demo/fixtures.js';
test('API-01 @api @smoke health contract', async ({ quotes, record }) => {
  await record({ rule: 'API-01', selector: ['GET /api/health'], detail: 'Service readiness and JSON content type.' });
  const response = await quotes.health();
  expect(response.status()).toBe(200);
  expect(response.headers()['content-type']).toContain('application/json');
  expect(await response.json()).toEqual({ status: 'ok', service: 'simulated-quotes' });
});
test('API-02 @api @smoke valid quotes and boundaries', async ({ quotes, record }) => {
  await record({ rule: 'API-02', selector: ['POST /api/quote'], detail: 'Minimum, normal and maximum amounts return the exact quote contract.' });
  for (const [amount, receive] of [[0.000001, 0], [1.5, 4686.75], [5, 15622.5]]) {
    const response = await quotes.quote(amount);
    expect(response.status()).toBe(200);
    expect(await response.json()).toEqual({ amount, rate: 3124.5, receive, from: 'ETH', to: 'USDC', simulated: true });
  }
});
test('API-03 @api invalid types and amounts rejected', async ({ quotes, record }) => {
  await record({ rule: 'API-03', selector: ['POST /api/quote'], detail: 'Zero, negative, over-limit, below-minimum, string, null and object are rejected.' });
  for (const amount of [0, -1, 6, 0.0000001, '1', null, {}]) {
    const response = await quotes.quote(amount);
    expect(response.status()).toBe(422);
    expect(await response.json()).toMatchObject({ error: 'invalid_amount' });
  }
});
test('API-04 @api malformed and oversized payloads', async ({ request, record }) => {
  await record({ rule: 'API-04', selector: ['POST /api/quote'], detail: 'Malformed JSON returns 400; over 4 KiB returns 413.' });
  const bad = await request.post('/api/quote', { data: Buffer.from('{'), headers: { 'Content-Type': 'application/json' } });
  expect(bad.status()).toBe(400); expect(await bad.json()).toEqual({ error: 'invalid_json' });
  const large = await request.post('/api/quote', { data: { amount: 1, padding: 'x'.repeat(5000) } });
  expect(large.status()).toBe(413); expect(await large.json()).toEqual({ error: 'payload_too_large' });
});
test('API-05 @api method and route boundaries', async ({ request, record }) => {
  await record({ rule: 'API-05', selector: ['GET /api/quote', 'GET /api/missing'], detail: '405 Allow header and structured 404; no HTML fallback for API errors.' });
  const wrong = await request.get('/api/quote');
  expect(wrong.status()).toBe(405); expect(wrong.headers()['allow']).toBe('POST');
  const missing = await request.get('/api/missing');
  expect(missing.status()).toBe(404); expect(await missing.json()).toEqual({ error: 'not_found' });
});
