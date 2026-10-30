# Accessibility QA: browser automation + static audit

## Start here: Playwright + TypeScript + axe-core

The runnable browser slice targets `demo/`, an isolated simulated swap flow. It requires no wallet, API key, Python or live network service. The existing `mock_dapp_ui/` intentionally contains defects and remains the target of the independent Python static audit.

From the repository root (Node.js 22+ and npm):

```bash
cd ux_accessibility_testing
npm ci
npx playwright install chromium
npm run typecheck
npm test
```

On Linux CI, install OS browser dependencies using `npx playwright install --with-deps chromium`. Browser installation may need system package permissions. `npm test` starts and stops the loopback demo server automatically on port 4173 (port must be free), runs desktop + mobile-emulated Chromium, and returns a nonzero exit code on automated failure.

```bash
npm run demo          # manual exploration: http://127.0.0.1:4173
npm run test:headed   # local visible browser (desktop display required)
npm run report        # open Playwright HTML report
```

Stop a manually running demo before running tests. No external target/base URL is supported by this first slice; it always tests the local fixture.

### Blueprint and file inventory

```text
ux_accessibility_testing/
├── demo/                          # NEW isolated accessible baseline
│   ├── index.html                 # landmarks, navigation, labeled form, native dialog
│   ├── app.js                     # validation, estimates, dialog and status behavior
│   └── styles.css                 # responsive layout and visible focus
├── tests/
│   ├── accessibility.spec.ts      # NEW six cases × desktop/mobile projects
│   └── evidence-reporter.ts       # NEW JSON + Markdown, including failed runs
├── scripts/serve.mjs              # NEW zero-dependency loopback server
├── playwright.config.ts           # NEW browser, server, artifacts and reporters
├── package.json                   # NEW local commands, pinned dependencies
├── package-lock.json              # NEW reproducible npm ci dependency graph
├── tsconfig.json                  # NEW strict type checking
├── .gitignore                     # NEW ignores dependencies and generated runs
├── test_specifications/
│   └── 03_playwright_slice.md      # NEW acceptance matrix and manual review queue
├── reports/
│   ├── playwright/                # GENERATED on every run, ignored by git
│   │   ├── evidence.json          # selectors, rules, impact, errors, statuses
│   │   ├── summary.md             # automated findings + manual review queue
│   │   ├── html/                  # Playwright HTML report + attached raw axe results
│   │   └── artifacts/             # failure screenshots and traces
│   └── examples/playwright/       # captured example run, not a current audit
└── README.md                      # UPDATED entry point and boundaries
```

Root `README.md` also links this entry point. Existing Python files and fixtures are unchanged.

### What is automated

Default-page structure and axe scan; exact keyboard Tab order and skip link; keyboard-only successful simulation; label association; empty, zero, negative and over-limit validation plus recovery; current values in dialog; initial focus, bidirectional Tab containment, Escape/Cancel and focus return; 320 CSS px overflow smoke with default/dialog scans. A negative-control case injects an unnamed button into a fresh test page and verifies that axe reports `button-name`; expected injected findings are explicitly marked and kept separate from target defects.

The suite uses axe WCAG 2 A/AA, 2.1 A/AA, 2.2 AA and best-practice tags. This is selected-rule/state coverage, **not WCAG certification**. Browser focus assertions do not validate screen-reader experience or visual focus quality.

### Reports and interpretation

- `reports/playwright/evidence.json`: per-test **Pass / Fail / Needs review**, assertion errors, axe version/environment, scan state, violations and incomplete nodes with selector, rule, impact, HTML and failure details.
- `reports/playwright/summary.md`: readable results, detected issues and outstanding manual work.
- `reports/playwright/html/index.html`: test results and attached full raw axe JSON, plus failure artifacts when available.
- Automated gate: zero axe violations in baseline states and all behavioral assertions passing. `axe.incomplete` is **Needs review**. Expected injected negative-control defects are excluded from baseline quality judgments.
- Overall remains **Needs review** until manual checks are executed. Screen-reader semantics/announcements, practical focus visibility/obstruction, zoom/text spacing, real-device responsive usability and full criterion coverage remain manual.

See [acceptance criteria and manual queue](test_specifications/03_playwright_slice.md). Future GitHub Actions can run the same install/typecheck/test commands from this directory and upload `reports/playwright/` using an always-run artifact step; no architecture change is required. This slice does not add a workflow yet.

---

## Legacy Python static audit

The material below describes the pre-existing static fixture and audit. Its example score is a custom heuristic, not a WCAG conformance percentage. Static HTML/attribute checks do not execute keyboard or dialog behavior, and historical compliance wording below must not be treated as certification.

# ♿ Web3 DApp UX & Accessibility (A11y) Quality Engineering Use Case

An enterprise-grade **Accessibility (A11y) & UX Quality Engineering Case Study** for modern Web3 / DApp interfaces (Token Swaps, Staking, and Wallet Connection Modals), aligned with **W3C WCAG 2.1 Level AA** standards and professional QA workflow skills (`07-design-accessibility-testcases`, `19-execute-accessibility-testing`, and `21-ui-ux-testing`).

---

## 📌 Use Case Overview

While Web3 DApps excel at cryptographic security, they frequently suffer from severe **accessibility and usability barriers**:
- **Screen Reader Invisibility:** Token selectors, slippage sliders, and icon buttons without accessible names (`aria-label`).
- **Keyboard Traps:** Modals opening without trapping focus, leaving keyboard-only users stuck behind the backdrop.
- **Low Contrast Warning Banners:** Gray text on dark backgrounds failing the WCAG 4.5:1 contrast requirement.
- **Non-Semantic Controls:** Interactive `div` elements with `onclick` that cannot be navigated via `Tab` or activated with `Enter`/`Space`.

This use case provides a **complete automated + manual testing framework** to audit, score, and remediate DApp interfaces.

---

## 📂 Directory Structure

```text
ux_accessibility_testing/
├── mock_dapp_ui/
│   ├── index.html                         # Interactive Web3 Swap UI with realistic accessible patterns & defect scenarios
│   ├── app.js                             # Focus trap, Escape key listener, modal & theme toggle handlers
│   └── styles.css                         # Dark/Light theme styles, skip links, and touch target rules
├── a11y_engine/
│   ├── __init__.py
│   ├── wcag_validator.py                  # Automated DOM auditor for WCAG 2.1 Level A & AA rules
│   └── contrast_calculator.py             # W3C relative luminance & contrast ratio math engine
├── test_specifications/
│   ├── 01_wcag_accessibility_matrix.md   # Test condition & case matrix conforming to Skill 07 & 19
│   └── 02_web3_ux_heuristics.md          # 10 Nielsen Usability Heuristics adapted for Web3 DeFi
├── config/
│   └── a11y_rules.json                    # Conformance thresholds and quality gate rules
├── run_a11y_audit.py                      # One-click CLI runner producing JSON & Markdown reports
└── README.md                              # Use case documentation
```

---

## 🚀 How to Execute the Automated A11y Audit

Run the audit engine with 1 command:
```bash
python ux_accessibility_testing/run_a11y_audit.py
```

### Sample Audit Console Output

```text
=====================================================================================
 ♿ SDET ACCESSIBILITY & UX AUDITOR: WCAG 2.1 LEVEL AA CONFORMANCE SCAN 
=====================================================================================
 • Target Interface: mock_dapp_ui/index.html
 • Target Standard : WCAG 2.1 (Level A & Level AA)
 • Methodologies   : Automated Static Analysis + Rule Invariants
=====================================================================================

CRITERION                           | SEVERITY   | STATUS   | DETAIL                   
-------------------------------------------------------------------------------------
2.4.1 Bypass Blocks (Level A)       | None       | PASS     | Skip-to-content link f...
1.1.1 Non-text Content (Level A)    | None       | PASS     | Image <img src="usdc-l...
1.3.1 Info and Relationships (Le    | None       | PASS     | Input #pay-amount-inpu...
1.3.1 Landmarks Structure (Level    | None       | PASS     | Document correctly use...
4.1.2 Dialog Pattern (Level A)      | None       | PASS     | Modal dialog correctly...
1.1.1 Non-text Content (Level A)    | Critical   | FAIL     | Image element complete...
4.1.2 Name, Role, Value (Level A)   | Critical   | FAIL     | Button contains only a...
2.1.1 Keyboard Accessible (Level    | Critical   | FAIL     | Custom interactive con...
1.4.3 Contrast (Minimum) (Level     | Serious    | FAIL     | Color contrast ratio 2...
-------------------------------------------------------------------------------------
SUMMARY: Compliance Score: 60.0% | Passed: 6 | Violations: 4
=====================================================================================

[⚠️] DETECTED ACCESSIBILITY VIOLATIONS & REMEDIATION GUIDANCE:

 1. [CRITICAL] 1.1.1 Non-text Content (Level A)
    • Offending Element: <img src="eth-logo.png">
    • Problem          : Image element completely missing 'alt' attribute.
    • How to Fix       : Add meaningful alt="Ethereum Logo" or alt="" if decorative.

 2. [CRITICAL] 4.1.2 Name, Role, Value (Level A)
    • Offending Element: <button id="settings-btn">
    • Problem          : Button contains only an icon with no accessible text.
    • How to Fix       : Add aria-label="Transaction Settings" to the icon button.

 3. [CRITICAL] 2.1.1 Keyboard Accessible (Level A)
    • Offending Element: <div class="slippage-badge" onclick="...">
    • Problem          : Custom interactive control built with non-semantic element.
    • How to Fix       : Replace with native <button> or add role='button' and tabindex='0'.

 4. [SERIOUS] 1.4.3 Contrast (Minimum) (Level AA)
    • Offending Element: <div class="low-contrast-warning">
    • Problem          : Color contrast ratio 2.6:1 fails WCAG Level AA (min 4.5:1).
    • How to Fix       : Increase text brightness to at least #9da3b4 for ratio >= 4.5:1.

[❌] QUALITY GATE FAILED: Found 3 Critical A11y violations blocking release.
```

---

## 🎯 Key Standards & Specifications Tracked

| Standard | Conformance Rule | Verification Method |
| :--- | :--- | :--- |
| **WCAG 1.1.1** | Non-text Content (`alt` attributes on tokens & badges) | Automated DOM Check |
| **WCAG 1.4.3** | Color Contrast (Minimum 4.5:1 for normal text) | Mathematical Relative Luminance |
| **WCAG 2.1.1** | Keyboard Operability (All interactive controls reachable via `Tab`) | DOM Semantic & Attribute Audit |
| **WCAG 2.4.1** | Bypass Blocks (Skip to main content link) | Anchor Target Verification |
| **WCAG 2.4.3** | Focus Order & Dialog Trapping (Modal focus management) | JavaScript Keyboard Trap |
| **WCAG 4.1.2** | Name, Role, Value (`aria-label`, `aria-modal`, `role="dialog"`) | ARIA Attribute Conformance |
