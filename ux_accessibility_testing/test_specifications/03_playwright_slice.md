# Browser slice: scope and acceptance criteria

Target: `demo/`, a local-only simulated DApp. Original `mock_dapp_ui/` remains an intentionally defective static-audit fixture. No wallet connection or RPC calls.

| Test | Evidence / acceptance | Related WCAG criteria (partial coverage) |
| --- | --- | --- |
| AXE-01 | One h1 and main/banner/nav/footer; axe has zero violations in default state | 1.3.1, 2.4.2, 4.1.2 |
| KEY-01 | Exact Tab sequence skip → Swap → About → amount → Review; skip transfers focus to main; keyboard-only successful simulation and focus return | 2.1.1, 2.4.1, 2.4.3 |
| FORM-01 | Native label focuses input; empty/0/negative/over-limit input rejected; description includes error; correction clears invalid state; current amount appears in dialog | 1.3.1, 3.3.1, 3.3.2 |
| DIALOG-01 | Accessible dialog name; initial focus on Cancel, Tab/Shift+Tab wrap, Escape/Cancel close and restore focus; axe open-state scan | 2.1.2, 2.4.3, 4.1.2 |
| RESP-01 | At 320 CSS px, no document horizontal overflow; controls in viewport; axe default/dialog scans | 1.4.10 (smoke only) |
| CONTROL-01 | Test-local unnamed button is detected by button-name with matching selector; expected defect isolated from target findings | Detector verification, not a conformance test |

All six tests run on desktop Chromium and mobile-emulated Chromium. Emulation is not real-device, Safari or screen-reader evidence.

## Manual review queue

All start as **Needs review**; never infer Pass from an automated run.

1. MAN-01: NVDA + Firefox/Chrome, VoiceOver + Safari: heading/landmark navigation, label/description reading, dialog name and modal boundary.
2. MAN-02: Error and success announcement timing, duplicate announcements and recovery with screen reader active.
3. MAN-03: Focus visibility and obstruction, logical order and dialog usability at zoom and with assistive technology.
4. MAN-04: 200%/400% zoom, text spacing, landscape, forced colors, touch targets and real mobile usability.
5. MAN-05: Content clarity, state-specific contrast and remaining applicable WCAG 2.2 A/AA criteria.

Record reviewer, date, browser/OS/AT versions, steps, actual result and evidence per item. `axe.incomplete` adds a separate Needs review queue; it is neither Pass nor an automatic Fail.

## Evidence contract and gate

`reports/playwright/evidence.json` contains run status, per-test/project status/errors, state-specific axe version/environment, passed rule IDs, violation/incomplete nodes (selector, rule, impact, HTML, failure summary, checks and help URL), and manual items.

- **Pass**: executed assertion passed, or a scan found no violations within its scope.
- **Fail**: assertion/timeout failed or axe violation found. Expected negative-control violations remain labeled Fail at finding level, while detector test passes if detected.
- **Needs review**: skipped/interrupted checks, axe incomplete nodes and all unexecuted manual work.
- `npm test` exits nonzero on automated failure. Manual work does not block this first automation gate; overall accessibility status remains Needs review even when the run passes.
- Reports are reset at run start. JSON/Markdown are generated at run end even for failed assertions; abrupt process termination can leave a running marker. A browser/server setup failure is not accessibility evidence.
