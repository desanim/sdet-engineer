# 16-Week Accessibility QA Roadmap

A practical plan for an experienced manual QA engineer moving toward Accessibility QA / Accessibility Test Specialist work. It emphasizes testing, audit evidence, and communication. It does not assume you will become a frontend developer in four months.

## Schedule and outcomes

- Core pace: about 8 hours per week (roughly 128 hours total).
- Stretch pace: add 2–5 hours per week for component coding, extra assistive-technology/browser combinations, or a second audit.
- Starting assumption: general web QA experience; basic browser and HTML familiarity helps. If HTML is new, use the first two weeks to learn enough to inspect elements and understand names, roles, and states.
- Portfolio outcome: one scoped accessibility audit with reproducible findings, manual test evidence, an automated check, retest evidence, and a clear limitations section.
- Not a promise: finishing the plan does not make someone an expert or prove complete WCAG conformance. Competence grows through repeated product work and feedback from disabled users and accessibility specialists.

Each week, spend about 2 hours learning, 4–5 hours practicing, and 1–2 hours documenting. Shift time as needed; hands-on work is the priority.

## Month 1 — Foundations and core web interaction

| Week | Learn and practice | Deliverable |
|---|---|---|
| 1. Users and barriers | WAI Fundamentals; review how vision, hearing, motor, cognitive, and temporary/contextual barriers affect tasks. Watch first-person demonstrations and read user-authored sources where possible. Avoid treating one person as representative of a whole group. | One-page barrier map: user/task/context → barrier → test idea. |
| 2. Semantic HTML and keyboard | Landmarks, heading structure, buttons vs links, labels, focus order, visible focus, skip links. Install NVDA on Windows; practice with a supported browser using Tab, Shift+Tab, Enter, Space, arrows, and Escape. | Keyboard-only walkthrough of one page, with evidence and issues. |
| 3. WCAG 2.2 and POUR | Learn Perceivable, Operable, Understandable, Robust; levels and success criteria. Use the Quick Reference to select common A/AA checks for a page, rather than trying to memorize the full standard. | A criterion-to-test matrix for 12–15 relevant criteria; include method and evidence needed. |
| 4. Forms and errors | Test labels, instructions, required status, format hints, error identification/suggestion, error summary, focus after submit, and preservation of valid data. | Accessible form test plan and findings on a demo form. |

## Month 2 — ARIA and interactive components

| Week | Learn and practice | Deliverable |
|---|---|---|
| 5. ARIA fundamentals | Learn roles, accessible names, states/properties, live regions, and the first rule: use native HTML when it provides the required semantics and behavior. Inspect the accessibility tree. | “Native HTML or ARIA?” decision sheet with examples and test notes. |
| 6. Common patterns I | Use APG to test disclosure/accordion, tabs, and modal dialogs. Check expected keyboard behavior, focus entry/containment/return, name, role, and state. | Component checklist plus reproducible issue examples. |
| 7. Common patterns II | Review menu button and combobox/autocomplete patterns only where applicable. Test arrow keys, selection, Escape, announcements, and focus. Compare behavior to APG; do not assume every visual menu should use the menu role. | Keyboard interaction matrix for one complex widget; note expected vs observed. |
| 8. Dynamic content and SPA flows | Test route changes, headings/title, focus management, toast and validation announcements, loading/results updates, and skip links. | Short SPA or demo-flow test report. Optional stretch: implement one accessible dynamic state and test it. |

## Month 3 — Audit methods and automation

| Week | Learn and practice | Deliverable |
|---|---|---|
| 9. Automated testing | Run axe DevTools or axe-core, WAVE, and Lighthouse on the same page. Verify each result manually; record tool/version. Add axe-core to an existing automated test if practical (e.g., Playwright). | One-page automated scan summary with confirmed, rejected, and manually investigated results. |
| 10. Manual assistive technology | Build a repeatable keyboard checklist. Test key tasks with NVDA + Firefox or Chrome. If available, add VoiceOver + Safari; record exact combinations. Check 200% and 400% zoom/reflow where appropriate. | Manual test procedure and coverage matrix, including platform limits. |
| 11. Scope a real audit | Choose a public demo or your own app. Define target users, key journeys, pages/states, conformance target, supported combinations, and exclusions before testing. Use a repeatable evaluation method such as WCAG-EM as guidance. | Audit scope, page inventory, and sampling rationale. |
| 12. Findings and reporting | Map failures to exact WCAG criteria only when evidence supports the mapping. Separate criterion failure, usability observation, and recommendation. Prioritize impact and exposure; use the report template. | Draft accessibility audit report with evidence and severity rationale. |

## Month 4 — Coverage, market context, and capstone

| Week | Learn and practice | Deliverable |
|---|---|---|
| 13. Zoom, cognition, motion, mobile | Check reflow, text resize, orientation, target behavior, reduced motion, plain language, and mobile screen-reader basics. Select checks that match the app and user goals. | Expanded coverage matrix and at least two documented findings or verified passes. |
| 14. Standards and market context | Compare the specific requirements relevant to the target market: WCAG 2.2, ISO/IEC 40500:2025, EN 301 549/EAA, Section 508, and China GB/T 37668-2019/MIIT guidance. Confirm current editions from primary sources. | One-page standards comparison with scope, source, and caveats; no blanket legal conclusion. |
| 15. Difficult patterns and report review | Select one relevant challenge (data table, chart, media, custom widget, localization/RTL, PDF, or mobile app). Review evidence with a peer or accessibility community if possible. | Revised finding set; one deeper case study explaining method, impact, and fix direction. |
| 16. Capstone and presentation | Re-run the scoped journey after any changes or on a second build. Include automated and manual evidence, retest results, untested combinations, and limits. Present concise executive summary plus technical appendix. | Publishable portfolio case study and linked audit report. |

## Weekly operating checklist

- [ ] State which user goal and product risk the test addresses.
- [ ] Use synthetic data and a safe environment.
- [ ] Test with keyboard and relevant assistive technology; do not rely on a scan alone.
- [ ] Record browser, OS, viewport/zoom, input method, assistive technology, and build.
- [ ] Capture evidence that can reproduce the issue without exposing personal data.
- [ ] Link a WCAG criterion only when the failure is supported by evidence.
- [ ] Separate observed behavior, user impact, interpretation, and proposed fix.
- [ ] Track untested pages, states, and combinations honestly.

## Capstone portfolio structure

1. Overview: product, audience, tested task, objective, date/build.
2. Scope: pages/states, WCAG version and target level, environments, exclusions.
3. Method: automated tools plus manual keyboard and screen-reader checks.
4. Coverage: test matrix and sampling rationale.
5. Findings: concise summary, detailed evidence, criterion mapping, impact, priority.
6. Fix and retest: before/after evidence and regression checks, if changes are made.
7. Limits: sample and tool limitations, untested combinations, and whether user research was performed.
8. Reflection: what you would test next and what the evidence does not establish.

Use the [accessibility reference library](accessibility-reference.md) and [audit report template](accessibility-audit-template.md) alongside this plan.