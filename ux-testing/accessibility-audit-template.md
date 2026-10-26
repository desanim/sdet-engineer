# Accessibility Audit Report Template

> Use this for a scoped portfolio exercise or project review. A limited sample does not support a blanket conformance claim. Use synthetic accounts and remove personal data from evidence.

## 1. Executive summary

- Product / feature: [ ]
- Build / date: [ ]
- Audit owner: [ ]
- Purpose: [User goal or risk]
- Overall summary: [What was examined and the main risks]
- Conformance statement: [Use only a precise, supported statement. If scope is partial, say so.]

## 2. Scope and target

- Standard/version: [e.g., WCAG 2.2]
- Target level: [A / AA / AAA; explain the agreed target]
- Pages, states, and journeys: [ ]
- User groups and task context considered: [ ]
- Out of scope: [ ]
- Sampling rationale: [Why these pages/states represent the selected tasks]
- Known assumptions/dependencies: [ ]

## 3. Environment

| Platform | Browser/version | Viewport/zoom | Input method | Assistive technology/version | Build |
|---|---|---|---|---|---|
| [OS/device] | [ ] | [ ] | [Keyboard/touch/voice] | [NVDA/VoiceOver/etc.] | [ ] |

Include locale, network condition, and test account type where they affect the result.

## 4. Methods and tools

- Automated checks: [Tool and version; pages/states scanned]
- Manual checks: [Keyboard, screen-reader tasks, zoom/reflow, contrast, etc.]
- Review guidance: [WCAG-EM or other method]
- User research: [Participants and method, or state “not performed”]
- Limitations: [Tool coverage, unavailable devices/AT, sample limits]

Automated results are prompts for investigation. Confirm each finding and add manual checks for interaction, context, and assistive-technology behavior.

## 5. Coverage matrix

| Page / state | Task | Keyboard | Screen reader | Zoom/reflow | Automated scan | Result / notes |
|---|---|---|---|---|---|---|
| [URL/state] | [Goal] | [Done/Not done] | [Combination] | [ ] | [Tool/version] | [ ] |

For detailed criterion-level results, add a separate table or link an evidence file. Use statuses such as Pass, Fail, Not applicable (with rationale), and Not tested. Do not convert missing evidence into a pass.

## 6. Findings summary

| ID | Finding | WCAG criterion (if supported) | Impacted user/task | Priority | Status |
|---|---|---|---|---|---|
| A11Y-001 | [Short title] | [SC and level] | [ ] | [P0–P3] | [Open/Fixed/Retest] |

Define priority using impact, likelihood, and exposure. Priority is a triage aid; it is not a WCAG conformance level or legal determination.

## 7. Finding detail

Repeat for each issue:

### A11Y-[ID]: [Specific user-visible problem]

- Criterion: [Exact WCAG version, SC number, and name; omit if this is a UX observation without a confirmed criterion failure]
- Affected page/state: [URL or screen and state]
- Environment: [Browser, OS, viewport, input, AT]
- Preconditions: [ ]
- Steps to reproduce:
  1. [ ]
  2. [ ]
- Expected: [Criterion or user-goal outcome]
- Observed: [Factual result]
- User impact: [Who is blocked or burdened and how]
- Evidence: [Screenshot, recording, accessibility-tree excerpt; no personal data]
- Frequency/scope: [How often and where observed; do not infer beyond evidence]
- Priority and rationale: [Impact × likelihood/exposure]
- Recommendation: [Possible remediation direction, not a legal claim]
- Retest: [Build/date/result/evidence/regression scope]

## 8. Conclusion and next steps

- Highest-risk findings: [IDs]
- Recommended remediation order: [ ]
- Retest scope: [ ]
- Untested criteria/pages/combinations: [ ]
- What this audit does not establish: [e.g., complete conformance, user satisfaction, or coverage of all assistive technologies]
- Next evaluation date/trigger: [ ]

## 9. Evidence handling

- Use stable identifiers and links.
- Keep screenshots or clips focused on the relevant state.
- Redact names, email addresses, tokens, payment data, and other personal information.
- Record exact build and test setup so another tester can reproduce the result.