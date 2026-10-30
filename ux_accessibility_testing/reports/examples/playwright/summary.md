# Accessibility E2E evidence

Run: **passed** · Overall: **Needs review**

Local simulated swap only. Automated pass is not WCAG conformance. Negative controls are isolated detector checks.

## Automated checks

### chromium-desktop / KEY-01 keyboard-only focus order and skip link — Pass

### chromium-desktop / AXE-01 default page and landmark structure — Pass

State: default — Pass

Passed rules: 39; violations: 0; incomplete nodes: 0.

### chromium-desktop / DIALOG-01 scan, bidirectional focus containment, Escape and return — Pass

State: dialog-open — Needs review

Passed rules: 17; violations: 0; incomplete nodes: 1.

```json
{
  "selector": [
    "#dialog-description"
  ],
  "rule": "color-contrast",
  "impact": "serious",
  "status": "Needs review",
  "error": "Fix any of the following:\n  Element's background color could not be determined because it partially overlaps other elements",
  "html": "<p id=\"dialog-description\">Simulate swapping 1.5 ETH for 4686.75 USDC. No funds will move.</p>",
  "help": "Elements must meet minimum color contrast ratio thresholds",
  "helpUrl": "https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=playwright",
  "checks": {
    "any": [
      {
        "id": "color-contrast",
        "data": {
          "contrastRatio": 0,
          "fontSize": "12.0pt (16px)",
          "fontWeight": "normal",
          "messageKey": "elmPartiallyObscuring",
          "expectedContrastRatio": "4.5:1"
        },
        "relatedNodes": [],
        "impact": "serious",
        "message": "Element's background color could not be determined because it partially overlaps other elements"
      }
    ],
    "all": [],
    "none": []
  }
}
```

### chromium-desktop / FORM-01 label association, invalid states and recovery — Pass

State: validation-error — Pass

Passed rules: 39; violations: 0; incomplete nodes: 0.

### chromium-desktop / CONTROL-01 detector catches injected missing label — Pass

State: injected-missing-button-name — Fail (expected injected defect; isolated negative control)

Passed rules: 39; violations: 1; incomplete nodes: 0.

```json
{
  "selector": [
    "#negative-control"
  ],
  "rule": "button-name",
  "impact": "critical",
  "status": "Fail",
  "error": "Fix any of the following:\n  Element does not have inner text that is visible to screen readers\n  aria-label attribute does not exist or is empty\n  aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty\n  Element has no title attribute\n  Element does not have an implicit (wrapped) <label>\n  Element does not have an explicit <label>\n  Element's default semantics were not overridden with role=\"none\" or role=\"presentation\"",
  "html": "<button id=\"negative-control\"></button>",
  "help": "Buttons must have discernible text",
  "helpUrl": "https://dequeuniversity.com/rules/axe/4.10/button-name?application=playwright",
  "checks": {
    "any": [
      {
        "id": "button-has-visible-text",
        "data": null,
        "relatedNodes": [],
        "impact": "critical",
        "message": "Element does not have inner text that is visible to screen readers"
      },
      {
        "id": "aria-label",
        "data": null,
        "relatedNodes": [],
        "impact": "critical",
        "message": "aria-label attribute does not exist or is empty"
      },
      {
        "id": "aria-labelledby",
        "data": null,
        "relatedNodes": [],
        "impact": "critical",
        "message": "aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty"
      },
      {
        "id": "non-empty-title",
        "data": {
          "messageKey": "noAttr"
        },
        "relatedNodes": [],
        "impact": "critical",
        "message": "Element has no title attribute"
      },
      {
        "id": "implicit-label",
        "data": null,
        "relatedNodes": [],
        "impact": "critical",
        "message": "Element does not have an implicit (wrapped) <label>"
      },
      {
        "id": "explicit-label",
        "data": null,
        "relatedNodes": [],
        "impact": "critical",
        "message": "Element does not have an explicit <label>"
      },
      {
        "id": "presentational-role",
        "data": null,
        "relatedNodes": [],
        "impact": "critical",
        "message": "Element's default semantics were not overridden with role=\"none\" or role=\"presentation\""
      }
    ],
    "all": [],
    "none": []
  }
}
```

### chromium-desktop / RESP-01 reflow smoke at 320 CSS px, default and dialog — Pass

State: 320px-default — Pass

Passed rules: 39; violations: 0; incomplete nodes: 0.

State: 320px-dialog — Needs review

Passed rules: 17; violations: 0; incomplete nodes: 2.

```json
{
  "selector": [
    "#dialog-title"
  ],
  "rule": "color-contrast",
  "impact": "serious",
  "status": "Needs review",
  "error": "Fix any of the following:\n  Element's background color could not be determined because it partially overlaps other elements",
  "html": "<h2 id=\"dialog-title\">Confirm simulated swap</h2>",
  "help": "Elements must meet minimum color contrast ratio thresholds",
  "helpUrl": "https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=playwright",
  "checks": {
    "any": [
      {
        "id": "color-contrast",
        "data": {
          "contrastRatio": 0,
          "fontSize": "18.0pt (24px)",
          "fontWeight": "bold",
          "messageKey": "elmPartiallyObscuring",
          "expectedContrastRatio": "3:1"
        },
        "relatedNodes": [],
        "impact": "serious",
        "message": "Element's background color could not be determined because it partially overlaps other elements"
      }
    ],
    "all": [],
    "none": []
  }
}
```

```json
{
  "selector": [
    "#dialog-description"
  ],
  "rule": "color-contrast",
  "impact": "serious",
  "status": "Needs review",
  "error": "Fix any of the following:\n  Element's background color could not be determined because it partially overlaps other elements",
  "html": "<p id=\"dialog-description\">Simulate swapping 1.5 ETH for 4686.75 USDC. No funds will move.</p>",
  "help": "Elements must meet minimum color contrast ratio thresholds",
  "helpUrl": "https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=playwright",
  "checks": {
    "any": [
      {
        "id": "color-contrast",
        "data": {
          "contrastRatio": 0,
          "fontSize": "12.0pt (16px)",
          "fontWeight": "normal",
          "messageKey": "elmPartiallyObscuring",
          "expectedContrastRatio": "4.5:1"
        },
        "relatedNodes": [],
        "impact": "serious",
        "message": "Element's background color could not be determined because it partially overlaps other elements"
      }
    ],
    "all": [],
    "none": []
  }
}
```

### chromium-mobile / AXE-01 default page and landmark structure — Pass

State: default — Pass

Passed rules: 39; violations: 0; incomplete nodes: 0.

### chromium-mobile / KEY-01 keyboard-only focus order and skip link — Pass

### chromium-mobile / DIALOG-01 scan, bidirectional focus containment, Escape and return — Pass

State: dialog-open — Needs review

Passed rules: 17; violations: 0; incomplete nodes: 2.

```json
{
  "selector": [
    "#dialog-title"
  ],
  "rule": "color-contrast",
  "impact": "serious",
  "status": "Needs review",
  "error": "Fix any of the following:\n  Element's background color could not be determined because it partially overlaps other elements",
  "html": "<h2 id=\"dialog-title\">Confirm simulated swap</h2>",
  "help": "Elements must meet minimum color contrast ratio thresholds",
  "helpUrl": "https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=playwright",
  "checks": {
    "any": [
      {
        "id": "color-contrast",
        "data": {
          "contrastRatio": 0,
          "fontSize": "18.0pt (24px)",
          "fontWeight": "bold",
          "messageKey": "elmPartiallyObscuring",
          "expectedContrastRatio": "3:1"
        },
        "relatedNodes": [],
        "impact": "serious",
        "message": "Element's background color could not be determined because it partially overlaps other elements"
      }
    ],
    "all": [],
    "none": []
  }
}
```

```json
{
  "selector": [
    "#dialog-description"
  ],
  "rule": "color-contrast",
  "impact": "serious",
  "status": "Needs review",
  "error": "Fix any of the following:\n  Element's background color could not be determined because it partially overlaps other elements",
  "html": "<p id=\"dialog-description\">Simulate swapping 1.5 ETH for 4686.75 USDC. No funds will move.</p>",
  "help": "Elements must meet minimum color contrast ratio thresholds",
  "helpUrl": "https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=playwright",
  "checks": {
    "any": [
      {
        "id": "color-contrast",
        "data": {
          "contrastRatio": 0,
          "fontSize": "12.0pt (16px)",
          "fontWeight": "normal",
          "messageKey": "elmPartiallyObscuring",
          "expectedContrastRatio": "4.5:1"
        },
        "relatedNodes": [],
        "impact": "serious",
        "message": "Element's background color could not be determined because it partially overlaps other elements"
      }
    ],
    "all": [],
    "none": []
  }
}
```

### chromium-mobile / FORM-01 label association, invalid states and recovery — Pass

State: validation-error — Pass

Passed rules: 39; violations: 0; incomplete nodes: 0.

### chromium-mobile / CONTROL-01 detector catches injected missing label — Pass

State: injected-missing-button-name — Fail (expected injected defect; isolated negative control)

Passed rules: 39; violations: 1; incomplete nodes: 0.

```json
{
  "selector": [
    "#negative-control"
  ],
  "rule": "button-name",
  "impact": "critical",
  "status": "Fail",
  "error": "Fix any of the following:\n  Element does not have inner text that is visible to screen readers\n  aria-label attribute does not exist or is empty\n  aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty\n  Element has no title attribute\n  Element does not have an implicit (wrapped) <label>\n  Element does not have an explicit <label>\n  Element's default semantics were not overridden with role=\"none\" or role=\"presentation\"",
  "html": "<button id=\"negative-control\"></button>",
  "help": "Buttons must have discernible text",
  "helpUrl": "https://dequeuniversity.com/rules/axe/4.10/button-name?application=playwright",
  "checks": {
    "any": [
      {
        "id": "button-has-visible-text",
        "data": null,
        "relatedNodes": [],
        "impact": "critical",
        "message": "Element does not have inner text that is visible to screen readers"
      },
      {
        "id": "aria-label",
        "data": null,
        "relatedNodes": [],
        "impact": "critical",
        "message": "aria-label attribute does not exist or is empty"
      },
      {
        "id": "aria-labelledby",
        "data": null,
        "relatedNodes": [],
        "impact": "critical",
        "message": "aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty"
      },
      {
        "id": "non-empty-title",
        "data": {
          "messageKey": "noAttr"
        },
        "relatedNodes": [],
        "impact": "critical",
        "message": "Element has no title attribute"
      },
      {
        "id": "implicit-label",
        "data": null,
        "relatedNodes": [],
        "impact": "critical",
        "message": "Element does not have an implicit (wrapped) <label>"
      },
      {
        "id": "explicit-label",
        "data": null,
        "relatedNodes": [],
        "impact": "critical",
        "message": "Element does not have an explicit <label>"
      },
      {
        "id": "presentational-role",
        "data": null,
        "relatedNodes": [],
        "impact": "critical",
        "message": "Element's default semantics were not overridden with role=\"none\" or role=\"presentation\""
      }
    ],
    "all": [],
    "none": []
  }
}
```

### chromium-mobile / RESP-01 reflow smoke at 320 CSS px, default and dialog — Pass

State: 320px-default — Pass

Passed rules: 39; violations: 0; incomplete nodes: 0.

State: 320px-dialog — Needs review

Passed rules: 17; violations: 0; incomplete nodes: 2.

```json
{
  "selector": [
    "#dialog-title"
  ],
  "rule": "color-contrast",
  "impact": "serious",
  "status": "Needs review",
  "error": "Fix any of the following:\n  Element's background color could not be determined because it partially overlaps other elements",
  "html": "<h2 id=\"dialog-title\">Confirm simulated swap</h2>",
  "help": "Elements must meet minimum color contrast ratio thresholds",
  "helpUrl": "https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=playwright",
  "checks": {
    "any": [
      {
        "id": "color-contrast",
        "data": {
          "contrastRatio": 0,
          "fontSize": "18.0pt (24px)",
          "fontWeight": "bold",
          "messageKey": "elmPartiallyObscuring",
          "expectedContrastRatio": "3:1"
        },
        "relatedNodes": [],
        "impact": "serious",
        "message": "Element's background color could not be determined because it partially overlaps other elements"
      }
    ],
    "all": [],
    "none": []
  }
}
```

```json
{
  "selector": [
    "#dialog-description"
  ],
  "rule": "color-contrast",
  "impact": "serious",
  "status": "Needs review",
  "error": "Fix any of the following:\n  Element's background color could not be determined because it partially overlaps other elements",
  "html": "<p id=\"dialog-description\">Simulate swapping 1.5 ETH for 4686.75 USDC. No funds will move.</p>",
  "help": "Elements must meet minimum color contrast ratio thresholds",
  "helpUrl": "https://dequeuniversity.com/rules/axe/4.10/color-contrast?application=playwright",
  "checks": {
    "any": [
      {
        "id": "color-contrast",
        "data": {
          "contrastRatio": 0,
          "fontSize": "12.0pt (16px)",
          "fontWeight": "normal",
          "messageKey": "elmPartiallyObscuring",
          "expectedContrastRatio": "4.5:1"
        },
        "relatedNodes": [],
        "impact": "serious",
        "message": "Element's background color could not be determined because it partially overlaps other elements"
      }
    ],
    "all": [],
    "none": []
  }
}
```

## Manual review — not executed

- **MAN-01 / Needs review** — Screen reader semantics (main, nav, dialog): NVDA + Firefox/Chrome and VoiceOver + Safari: read headings/landmarks, labels, description, dialog name and modal boundary.
- **MAN-02 / Needs review** — Announcements and recovery (#amount, #amount-error, #status): With screen reader enabled, submit empty/invalid form, correct it and complete simulation. Verify error and success are announced once at the right time.
- **MAN-03 / Needs review** — Practical focus usability (:focus-visible, #review-dialog): Keyboard through all controls; inspect visible, unobscured focus, sensible reading order and modal entry/exit at zoom and with assistive technology.
- **MAN-04 / Needs review** — Responsive usability and zoom (body): Check 200%/400% browser zoom, text spacing, landscape, touch targets, forced colors and real mobile devices. 320px overflow smoke does not establish conformance.
- **MAN-05 / Needs review** — Content and full WCAG coverage (body): Review instructions, error clarity, contrast in all states and remaining applicable WCAG 2.2 A/AA criteria; record reviewer, browser/AT versions and evidence.
