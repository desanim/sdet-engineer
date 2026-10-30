# Framework validation snapshot

Captured on 2026-10-30, Linux / Node.js 24.22.1. See `validation.json` for the exact matrix, runtime browser versions, case lists, incomplete findings and manual review queue.

| Check | Result |
| --- | --- |
| Clean `npm ci` | Pass |
| Strict TypeScript check | Pass |
| Smoke: API + desktop/tablet/mobile | 11/11 Pass |
| Full: API + eight UI profiles | 78/78 Pass |
| Full baseline axe scans | 26 scans, zero violations |
| Isolated detector controls | 8 scans, all caught the expected missing button name |
| axe incomplete nodes | 9, Needs review |
| Manual accessibility items | 5, not executed / Needs review |

Full run took 46.6 seconds with two workers; smoke took 7.4 seconds. These times describe this run only.

Firefox in this restricted container required local-only `MOZ_DISABLE_CONTENT_SANDBOX`, `MOZ_DISABLE_RDD_SANDBOX` and `MOZ_DISABLE_GMP_SANDBOX` environment settings. The project and GitHub Actions configuration do not disable browser sandboxing. Smoke passed without these environment settings. The initial Firefox launch failures were infrastructure errors, not app failures.

The JSON here is a compact snapshot; regenerate full per-test evidence and raw axe JSON/HTML attachments with `npm test` / `npm run test:full`. Generated reports live under `reports/playwright/demo/{smoke,full}/` and are ignored by git. The older `reports/examples/playwright/` captures the historical V1 slice.

No physical device or screen-reader testing was performed. Accessibility overall remains Needs review. GitHub Actions configuration is included; its remote execution must be checked separately.
