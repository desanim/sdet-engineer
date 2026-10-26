# UX Testing for QA

A practical reference set for testing whether a digital product is understandable, usable, accessible, and reliable across real user journeys. The materials are written for a QA engineer building a portfolio case study.

## What is included

| Document | Use it for |
|---|---|
| [Foundations](foundations.md) | Scope UX testing, choose methods, plan sessions, assess findings, and measure outcomes |
| [Test plan template](test-plan-template.md) | Turn a product flow into a reviewable UX test plan and checklist |
| [Bug report template](bug-report-template.md) | Write evidence-based UX and accessibility defects developers can reproduce |

## Working model

1. **Understand the user goal.** Identify the audience, task, context, and impact of failure.
2. **Map the journey.** Follow the complete path, including entry points, errors, recovery, and completion.
3. **Inspect the interface.** Combine exploratory checks, heuristic review, responsive checks, and accessibility checks.
4. **Validate with users when possible.** Observe representative users attempting realistic tasks. QA can facilitate or support the study, while keeping observations separate from assumptions.
5. **Record evidence.** Capture environment, steps, expected and observed behavior, impact, and supporting evidence.
6. **Prioritize and retest.** Rank by user impact and frequency, confirm fixes, and check nearby flows for regressions.

## Portfolio practice case

Use a fictional or public demo e-commerce product. Examine product discovery, product details, cart, and checkout. Do not submit a real purchase or use real personal or payment data. Record:

- Test objective and scope
- User journeys and task scenarios
- Device, browser, viewport, and test data
- Findings with severity, evidence, and recommendations
- Accessibility checks against WCAG 2.2
- Retest notes and a short reflection on limitations

See [Foundations](foundations.md) for method selection and [Test plan template](test-plan-template.md) to start the case.

## Reference sources

- [Nielsen Norman Group: Usability Testing 101](https://www.nngroup.com/articles/usability-testing-101/)
- [Nielsen Norman Group: 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [Nielsen Norman Group: Task Scenarios for Usability Testing](https://www.nngroup.com/articles/task-scenarios-usability-testing/)
- [W3C: WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [W3C WAI: WCAG 2 at a Glance](https://www.w3.org/WAI/standards-guidelines/wcag/glance/)

The heuristics are inspection principles, not a substitute for usability sessions. WCAG conformance checks are a distinct accessibility activity; automated tools alone cannot establish that a product is accessible.
