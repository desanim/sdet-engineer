# Web framework acceptance criteria

Target: registered demo adapter, simulated local quote API. Scope: web only; no native applications or physical device farm.

| ID | Suite | Acceptance | Smoke |
| --- | --- | --- | --- |
| UI-01 | Functional | UI sends real POST quote, uses response values, confirms and restores focus/status | Yes |
| UI-02 | Functional | Empty/zero/negative/over-limit/below-minimum rejected before HTTP; correction clears errors | No |
| UI-03 | Functional | Controlled 503 response shows error, enables retry and then opens dialog | No |
| API-01 | API | Health status and JSON content type | Yes |
| API-02 | API | Exact quote contracts at minimum, normal and maximum amounts | Yes |
| API-03 | API | Invalid numeric ranges, strings, null and object return 422 | No |
| API-04 | API | Raw malformed JSON returns 400; oversized payload returns 413 | No |
| API-05 | API | Wrong method returns 405/Allow; unknown route returns structured 404 | No |
| AXE-01 | A11y | One h1/main/banner/nav/footer and default scan without violations | Yes |
| AXE-02 | A11y | Error and open-dialog scans without violations; incomplete preserved | No |
| CONTROL-01 | A11y | Injected unnamed button caught with matching selector | No |
| KEY-01 | A11y | Tab order, skip link and keyboard-only complete flow | No |
| KEY-02 | A11y | Dialog initial focus, both Tab boundaries, Escape/Cancel and focus return | No |
| RESP-01 | Responsive | Each configured viewport preserved; default/dialog no horizontal overflow; touch profiles use tap | Yes |
| RESP-02 | Responsive | 320/375/768/1024/1440 CSS px, default/dialog layout; 320px axe scan | No; once on desktop Chromium |

Full matrix: 8 UI projects × 9 UI cases + 1 shared breakpoint case + 5 API cases = 78 checks. Smoke: 3 UI projects × 3 smoke cases + 2 API = 11 checks. API cases do not instantiate a browser; shared breakpoint cases are excluded from other projects at discovery, rather than counted as skipped device tests.

## Manual queue

Source: `apps/demo/manual-review.json`. All initial entries are Needs review and unexecuted. Capture reviewer/date/OS/browser/AT versions, steps, expected/actual behavior and evidence before recording manual results.

- Screen-reader heading/landmark/label/description/dialog semantics.
- Error, quote loading/failure and success announcements with NVDA/VoiceOver.
- Visible/unobscured focus, logical order, modal usability and practical keyboard behavior.
- 200%/400% zoom, text spacing, forced colors, landscape and real-device touch/virtual keyboard usability.
- Instructions/error clarity, state-specific contrast and remaining applicable WCAG 2.2 A/AA criteria.

`axe.incomplete` adds a separate per-node review queue. Do not silently convert it to Pass, suppress it or count expected negative-control defects as baseline defects. These cases provide partial coverage of WCAG 1.3.1, 1.4.10, 2.1.1, 2.1.2, 2.4.1, 2.4.3, 3.3.1, 3.3.2 and 4.1.2; they are not full criterion/conformance verification.
