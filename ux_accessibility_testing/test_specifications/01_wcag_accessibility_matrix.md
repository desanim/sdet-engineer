# ♿ WCAG 2.1 Level AA Accessibility Test Specification & Case Matrix

*Designed according to QA Workflow Skill `07-design-accessibility-testcases` and `19-execute-accessibility-testing`.*

---

## 1. Conformance Scope & Environment Matrix

- **Application:** VibeDEX Web3 Token Swap Interface
- **Target Standard:** **W3C WCAG 2.1 (Conformant to Level A & Level AA)**
- **Supported Assistive Technologies (AT):**
  - **Screen Readers:** NVDA 2026.1 (Windows / Chrome), VoiceOver (macOS / Safari, iOS / Mobile Safari)
  - **Navigation Devices:** Physical Keyboard-only, Switch Control
  - **Display Modes:** 200% - 400% Zoom / Reflow, Windows High Contrast Mode, Dark & Light Themes

---

## 2. Detailed Accessibility Condition & Case Matrix

| Case ID | Journey / Component | WCAG Criterion | Method | Device / AT | Steps to Execute | Expected Accessible Behavior | Severity Guidance | Automation Suitability |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A11Y-TC-01** | Global Navigation / Header | **2.4.1 Bypass Blocks (Level A)** | Manual + Automated | Keyboard | 1. Open DApp.<br>2. Press `Tab` once. | Skip to main content button becomes visible, focused; pressing `Enter` moves focus straight to `#main-content`. | **Serious** | Automated |
| **A11Y-TC-02** | Swap Card / Settings Button | **4.1.2 Name, Role, Value (Level A)** | Automated | NVDA / Screen Reader | 1. Navigate to Settings gear icon using `Tab`. | Screen reader announces "Transaction Settings, Button". Icon button must not be announced as unlabelled or just "Button". | **Critical** | Automated |
| **A11Y-TC-03** | Token Select / Logos | **1.1.1 Non-text Content (Level A)** | Automated | Screen Reader | 1. Inspect token icons in pay/receive selectors. | Every informative `<img>` has descriptive `alt` (e.g. `alt="USDC Logo"`). Purely decorative icons use `aria-hidden="true"`. | **Critical** | Automated |
| **A11Y-TC-04** | Form Controls / Amount Inputs | **1.3.1 Info and Relationships (Level A)** | Automated | Screen Reader | 1. Tab into Pay and Receive input fields. | Screen reader announces "You Pay, Edit, 0.0" and associated label via `<label for="...">` or `aria-labelledby`. | **Critical** | Automated |
| **A11Y-TC-05** | Trade Info / Price Impact Warning | **1.4.3 Contrast (Minimum) (Level AA)** | Automated + Color Picker | CCA (Colour Contrast Analyser) | 1. Inspect text color and background color of Warning element. | Text contrast ratio is at least **4.5:1** against surface background. Low contrast text (#707080 on #0f111a is 2.6:1 $\rightarrow$ Violation). | **Serious** | Automated |
| **A11Y-TC-06** | Slippage Selector Badges | **2.1.1 Keyboard (Level A)** | Manual | Keyboard-only | 1. Attempt to reach and select 0.5% and 1.0% slippage options using `Tab` and `Enter`/`Space`. | Slippage options receive visible focus ring, can be activated via `Enter` or `Space`, and expose `role="radio"` or `role="button"`. | **Critical** | Manual / Custom AST |
| **A11Y-TC-07** | Live Gas & Exchange Rate Updates | **4.1.3 Status Messages (Level AA)** | Manual | Screen Reader | 1. Wait for live price fluctuation or gas fee adjustment. | Screen reader politely announces updated price without interrupting user input (`aria-live="polite"`). | **Moderate** | Manual |
| **A11Y-TC-08** | Swap Confirmation Modal | **2.4.3 Focus Order & 4.1.2 Dialog (Level A)** | Manual | Keyboard + VoiceOver | 1. Click Swap button.<br>2. Observe modal opening.<br>3. Press `Tab` repeatedly.<br>4. Press `Escape`. | Focus shifts into the dialog (`aria-modal="true"`), focus is trapped inside while open, `Escape` closes the modal, and focus restores to trigger. | **Critical** | Semi-Automated |
| **A11Y-TC-09** | Responsive Display / Mobile | **1.4.10 Reflow (Level AA)** | Manual | Browser Zoom 400% (1280px width) | 1. Set zoom to 400% (equivalent to 320 CSS px width). | Content reflows vertically without two-dimensional scrolling (no horizontal scrollbar needed to complete a swap). | **Serious** | Manual |
| **A11Y-TC-10** | Touch Targets | **2.5.5 / 2.5.8 Target Size (Level AA)** | Automated + Manual | Mobile Device / Touch | 1. Measure clickable dimensions of buttons, selectors, and badges. | Clickable interactive controls have a minimum bounding box of **44x44 CSS pixels** or adequate spacing. | **Moderate** | Automated |

---

## 3. Untested User Impact Assessment

If accessibility testing is omitted before deploying the DApp:
1. **Blind / Low-Vision Users:** Cannot complete token swaps because form inputs and settings buttons lack accessible names.
2. **Motor-Impaired Keyboard Users:** Cannot change slippage tolerance or close confirmation modals because custom interactive elements cannot be focused.
3. **Legal & Compliance Exposure:** In many jurisdictions (European Accessibility Act - EAA 2025, US ADA Title III), public web applications face direct legal penalties for non-conformance to WCAG 2.1 AA.
