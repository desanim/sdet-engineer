import type { APIResponse, TestInfo } from '@playwright/test';
// Opt in per application. Do not attach auth headers, tokens or personal data.
export async function attachResponse(info: TestInfo, response: APIResponse) {
  await info.attach('api-evidence', {
    body: JSON.stringify({ path: new URL(response.url()).pathname, status: response.status(), body: await response.json() }),
    contentType: 'application/json'
  });
  return response;
}
