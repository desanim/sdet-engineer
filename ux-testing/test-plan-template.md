# UX Testing Plan Template

> Copy this file for a project and replace the bracketed prompts. Use synthetic data and a safe environment.

## 1. Overview

- **Product / feature:** [Name and short description]
- **Build / URL:** [Version or test environment]
- **Prepared by / date:** [Name / date]
- **Objective:** [What user risk or question is this test addressing?]
- **Status:** Draft / Ready / Executed / Retest

## 2. User and task context

- **Target user group:** [Relevant characteristics, experience, needs]
- **User goal:** [What the person is trying to accomplish]
- **Use context:** [Device, location, time pressure, assistive technology, etc.]
- **Criticality:** [Impact if task fails]

## 3. Scope

### In scope
- [Journey, screens, states, device/browser combinations]

### Out of scope
- [Explicit exclusions and reason]

### Assumptions and dependencies
- [Test accounts, feature flags, service dependencies, known limitations]

## 4. Methods

Select and explain each method:

- [ ] Exploratory journey testing
- [ ] Heuristic evaluation
- [ ] Moderated usability session
- [ ] Keyboard and accessibility checks
- [ ] Screen-reader checks: [AT/browser combinations]
- [ ] Responsive/zoom checks
- [ ] Other: [Method and reason]

**Why these methods fit the objective:** [Short rationale]

## 5. Environment and data

| Item | Details |
|---|---|
| Build / URL | [ ] |
| Browser and version | [ ] |
| Device / OS | [ ] |
| Viewport / zoom | [ ] |
| Input method | [Mouse / touch / keyboard / voice] |
| Assistive technology | [If applicable] |
| Locale / timezone | [ ] |
| Network conditions | [ ] |
| Test data | [Synthetic data only; document reset process] |

## 6. User journeys and scenarios

| ID | User goal | Scenario (do not give interface instructions) | Success criteria | Stop / safety condition |
|---|---|---|---|---|
| UX-01 | [Goal] | [Neutral realistic scenario] | [Observable outcome] | [When to stop] |
| UX-02 | [Goal] | [Neutral realistic scenario] | [Observable outcome] | [When to stop] |

## 7. Inspection checklist

### Clarity and feedback
- [ ] Labels, instructions, and terminology are understandable.
- [ ] Loading, success, and error states communicate what happened.
- [ ] The user can tell what is required and what is optional.

### Navigation and control
- [ ] Primary action is distinguishable and available at the right point.
- [ ] Back, cancel, undo, and edit behavior are predictable.
- [ ] Focus and navigation order follow the intended journey.

### Forms and error recovery
- [ ] Input format and constraints are explained before failure where feasible.
- [ ] Errors identify the field and give a usable correction.
- [ ] Valid input is preserved after an error.
- [ ] Error summary and inline messages work with keyboard and assistive tech.

### Responsive and accessibility
- [ ] Key tasks work at supported viewport sizes and zoom.
- [ ] Keyboard focus is visible and not trapped.
- [ ] Controls have accessible names, roles, and states.
- [ ] Contrast, target interaction, headings, and reading order were checked.
- [ ] Applicable WCAG 2.2 criteria are recorded with evidence.

### Completion and trust
- [ ] Final cost, choices, and consequences are visible before confirmation.
- [ ] Confirmation clearly states the completed action and next step.
- [ ] Privacy-sensitive information is not unnecessarily exposed.

## 8. Session notes

| Scenario | Outcome | Time | Errors / recovery | Assistance | Observations (facts) | Interpretation (separate) |
|---|---|---:|---|---|---|---|
| UX-01 | [Complete / difficult / fail] | [ ] | [ ] | [ ] | [ ] | [ ] |

## 9. Findings and prioritization

| Finding ID | User goal affected | Impact | Likelihood / exposure | Severity | Evidence | Owner / status |
|---|---|---|---|---|---|---|
| UX-DEF-01 | [ ] | [ ] | [ ] | [P0–P3] | [Link] | [ ] |

Explain severity using the team's scale and actual evidence. Link any accessibility finding to the applicable WCAG criterion when known.

## 10. Exit criteria

- [ ] Every in-scope scenario has a recorded outcome.
- [ ] High-impact findings have an owner or an explicit decision.
- [ ] Evidence contains no personal data or secrets.
- [ ] Limitations and untested combinations are documented.
- [ ] Retest plan and build are recorded.

## 11. Summary

- **What worked:** [Evidence-backed]
- **Most important user risks:** [Finding IDs]
- **Accessibility status:** [What was checked and what remains]
- **Limitations:** [Sample, coverage, environment]
- **Recommendation / next step:** [Action]
