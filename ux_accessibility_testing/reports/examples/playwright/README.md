# Captured browser evidence

This is a snapshot from the implementation validation, not a live audit or WCAG certification. Regenerate current results using `npm test` in `ux_accessibility_testing/`.

Validation environment: Linux, Node.js 24.22.1, Playwright 1.56.1, bundled Chromium 141, axe-core 4.10.3.

- Clean `npm ci`: passed.
- `npm run typecheck`: passed.
- `npm test -- --workers=2`: 12 passed (six cases × two projects).
- Baseline state scans: ten; zero violations.
- Detector controls: two; each caught the expected `button-name` violation at `#negative-control`. These are isolated injected defects, not baseline failures.
- Seven incomplete contrast nodes across four dialog scans: preserved as Needs review; no automatic conformance conclusion.
- Five manual review items: not executed, Needs review.
- Assertion failure paths were also exercised during implementation: JSON/Markdown retained error details and the test command exited nonzero.

`evidence.json` includes selectors, rule IDs, impacts, failure messages, engine/environment metadata, behavior outcomes and the manual queue. `summary.md` is its human-readable companion. Per-scan full raw axe JSON and the HTML report are generated locally under `reports/playwright/` and intentionally excluded from git.
