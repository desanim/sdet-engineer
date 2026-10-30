# Web Quality Automation Framework

Playwright + TypeScript + axe-core for **Functional UI, API, Accessibility and Responsive** testing of websites/web apps on desktop, tablet and mobile profiles. The runnable application adapter is a local simulated DApp; framework utilities and device configuration are independent of its selectors.

## Quick start

Node.js 22+ and npm, from the repository root:

```bash
cd ux_accessibility_testing
npm ci
npx playwright install chromium firefox webkit
npm run typecheck
npm test                 # smoke: API once + desktop/tablet/mobile
npm run test:full        # full browser/device matrix
```

Linux/CI: `npx playwright install --with-deps chromium firefox webkit` also installs OS libraries and can require system package permissions. A missing browser/library is an infrastructure failure, never a passing test. The local server starts/stops automatically; port 4173 must be free. No wallet, RPC, account or API key is required.

| Command | Scope |
| --- | --- |
| `npm test` | 11 smoke checks: 2 API + 3 UI cases on 3 profiles |
| `npm run test:full` | 78 checks: 5 API, 9 UI cases on 8 profiles, 1 shared breakpoint sweep |
| `npm run test:ui` | Functional UI suite across full device matrix |
| `npm run test:api` | API contract/boundary/error cases, once without browser launch |
| `npm run test:a11y` | axe scans, keyboard/focus and detector controls |
| `npm run test:responsive` | Profile layout/tap checks and one breakpoint sweep |
| `npm run test:headed` | Smoke in visible browsers, requires a desktop display |
| `npm run demo` | Manual exploration at http://127.0.0.1:4173; stop before tests |
| `npm run report` / `npm run report:full` | Open demo smoke/full HTML report |

Narrow a run with CLI options: `npm run test:full -- --project desktop-firefox --workers=2`. Smoke intentionally includes only `@smoke` tests, even when a project filter is provided. Use `test:full` to remove that tag filter.

## Browser and device matrix

| Project | Engine | Profile | Orientation | Smoke |
| --- | --- | --- | --- | --- |
| desktop-chromium | Chromium | 1440 × 900 | Landscape | Yes |
| desktop-firefox | Firefox | 1440 × 900 | Landscape | No |
| desktop-webkit | WebKit | 1440 × 900 | Landscape | No |
| tablet-ipad-portrait | WebKit | Playwright iPad (gen 7), touch + DPR + UA | Portrait | Yes |
| tablet-ipad-landscape | WebKit | Playwright iPad (gen 7) landscape | Landscape | No |
| mobile-android-portrait | Chromium | Playwright Pixel 7, touch + DPR + UA | Portrait | Yes |
| mobile-iphone-portrait | WebKit | Playwright iPhone 13, touch + DPR + UA | Portrait | No |
| mobile-iphone-landscape | WebKit | Playwright iPhone 13 landscape | Landscape | No |
| api | None | HTTP client, one execution | N/A | Yes |

These are **browser/device emulations**, not real iPhone/iPad/Android or branded Safari/Chrome certification. Keyboard tests on touch profiles exercise synthetic hardware-keyboard input, not the on-screen mobile keyboard. The separate 320/375/768/1024/1440 CSS px sweep runs once on desktop Chromium; profile tests preserve each device's configured viewport. Landscape profiles are separate contexts, not a live rotation sensor test.

Add profiles in `config/devices.ts`. Choose representative profiles based on the target app's users; multiplying every browser × every device is deliberately avoided.

## Structure and responsibilities

```text
ux_accessibility_testing/
├── config/
│   ├── devices.ts                 # browser/device matrix, smoke selection, API isolation
│   └── targets.ts                 # registered apps, UI/API URLs, local-server decision
├── framework/
│   ├── test.ts                    # shared fixtures, browser runtime evidence, axe scanner
│   ├── api.ts                     # opt-in JSON response evidence
│   └── reporting/evidence-reporter.ts
├── apps/demo/
│   ├── SwapPage.ts                # demo-specific semantic locators and actions
│   ├── QuoteClient.ts             # demo quote/health API client
│   ├── fixtures.ts                # adapter fixtures composed from shared test fixture
│   └── manual-review.json         # unexecuted manual accessibility queue
├── tests/demo/
│   ├── functional/swap.spec.ts
│   ├── api/quotes.spec.ts
│   ├── accessibility/{scan,keyboard}.spec.ts
│   └── responsive/{layout,breakpoints}.spec.ts
├── demo/{index.html,app.js,styles.css}
├── scripts/{serve,run-tests}.mjs
├── playwright.config.ts
├── package.json / package-lock.json / tsconfig.json
├── reports/playwright/demo/{smoke,full}/  # generated, ignored
├── reports/examples/                    # captured snapshots, not current results
├── test_specifications/04_web_framework.md
├── mock_dapp_ui/                         # legacy intentionally defective fixture
├── a11y_engine/                          # legacy static Python engine
└── run_a11y_audit.py                     # independent legacy entry point
```

## Add another website/web app

1. Create `apps/<name>/` with its Page Objects, API client, fixtures and manual review queue. Compose its fixtures from `framework/test.ts`; selectors/business rules stay in the adapter.
2. Create `tests/<name>/{functional,api,accessibility,responsive}/` using those fixtures. Use tags `@functional`, `@api`, `@a11y`, `@responsive`; mark fast representative checks with `@smoke`.
3. Add a registry entry in `config/targets.ts`, following `demo`, with the app's test directory and manual-review JSON. The registry is explicit: merely changing BASE_URL does not make DApp business tests valid for an unrelated site.
4. Set `TEST_APP`, `BASE_URL` and optionally `API_BASE_URL` for the target you are authorized to test. BASE_URL disables the local fixture server. API_BASE_URL defaults to BASE_URL; when overriding API_BASE_URL, set BASE_URL explicitly too. APIs can have a separate host; the app adapter must reflect how its UI actually calls that API.
5. Reuse the matrix, scan helper, fixtures and reporter. Extend suites for authentication/data cleanup as the target requires; this starter does not provide a universal login flow.

Example for a registered `storefront` adapter, bash:

```bash
TEST_APP=storefront BASE_URL=https://staging.example.com API_BASE_URL=https://api-staging.example.com npm run test:full
```

PowerShell equivalent:

```powershell
$env:TEST_APP="storefront"
$env:BASE_URL="https://staging.example.com"
$env:API_BASE_URL="https://api-staging.example.com"
npm run test:full
```

There is no `.env` autoload or secret requirement. Never place credentials in URLs or attach private payloads. The demo client's response evidence is safe synthetic data; new adapters should explicitly select/redact evidence fields. The current demo uses root-relative routes; an application hosted at a subpath needs an adapter that models those paths.

## Test coverage

- **Functional:** real localhost quote request → server validation → current values in dialog → simulated confirmation; invalid input prevents HTTP requests; API failure presents recovery and a successful retry.
- **API:** health/JSON contract, valid lower/normal/upper boundaries, wrong types and invalid ranges, malformed JSON, payload limit, method/Allow header and unknown route.
- **Accessibility:** heading/landmarks, labels/error descriptions, default/error/dialog axe scans, Tab order, skip link, dialog entry/containment/Escape/Cancel/focus return; isolated unnamed-button detector control.
- **Responsive:** no horizontal overflow in default/dialog states; visible confirmation control; tap interaction on touch profiles; screenshots per profile; shared breakpoint sweep and 320px axe scans.

See [acceptance criteria](test_specifications/04_web_framework.md). The earlier [slice specification](test_specifications/03_playwright_slice.md) and `reports/examples/playwright/` are historical V1 material; current commands and paths are in this README.

## Evidence, gates and manual review

Each run writes `reports/playwright/<app>/<smoke|full>/`:

- `evidence.json`: test status/errors, suite, declared coverage, actual browser version/UA/viewport/DPR/touch mode, API responses, state-specific axe nodes with selector/rule/impact/failure details, matrix and counts.
- `summary.md`: readable outcomes, findings and manual queue.
- `html/index.html`: Playwright report with raw axe JSON, response/coverage/runtime attachments and profile screenshots.
- `artifacts/`: failure screenshots and traces.

Smoke and full outputs are separate. A later filtered run in the same mode replaces that mode's previous report; use the recorded test/project counts to understand its scope. Simultaneous runs for the same app/mode are unsupported. Reports reset to a running marker at start; abrupt termination can leave that marker.

`npm test`/`test:full` exits nonzero on assertion, baseline axe violation or infrastructure failure. `axe.incomplete` is **Needs review**. Negative-control findings are isolated and excluded from baseline counts; the detector test passes only when its injected defect is detected. API cases run once rather than being repeated for each device.

Automated **Pass** is limited to executed assertions. Skipped/interrupted cases are **Needs review**, not Pass. Accessibility overall remains **Needs review** until manual work is executed: screen-reader semantics and announcements; practical focus visibility/obstruction; zoom/text spacing/forced colors; real-device usability and full applicable WCAG 2.2 A/AA coverage. Browser emulation, an overflow smoke or zero axe violations cannot establish WCAG conformance.

## GitHub Actions

`.github/workflows/web-quality.yml` runs smoke for module changes in PRs and pushes to main, and offers manual smoke/full dispatch. It installs all browser dependencies, typechecks, runs the same tests and uploads reports even after failures. No account secrets or scheduled automation are configured. CI execution status must be checked in GitHub separately from local validation.

## Legacy Python audit

```bash
python ux_accessibility_testing/run_a11y_audit.py
```

Run that command from the repository root with the repository's Python dependencies installed. It still targets `mock_dapp_ui/`, which intentionally contains defects. Its custom score and historical compliance wording do not establish WCAG conformance; static attribute checks do not execute browser keyboard/focus behavior. The Python engine and original fixture remain independent of this browser framework.
