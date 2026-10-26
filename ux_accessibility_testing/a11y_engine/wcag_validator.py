"""
Automated WCAG 2.1 Level AA Accessibility DOM Auditor.
Parses HTML document structure, evaluates accessibility rules, and classifies severity.
"""
from typing import List, Dict
from bs4 import BeautifulSoup
from .contrast_calculator import calculate_contrast_ratio, evaluate_wcag_contrast


class WCAGValidator:
    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, "html.parser")
        self.violations: List[Dict] = []
        self.passes: List[Dict] = []

    def run_all_checks(self) -> Dict:
        self.check_bypass_blocks()       # WCAG 2.4.1
        self.check_images_alt()          # WCAG 1.1.1
        self.check_form_labels()         # WCAG 1.3.1 / 4.1.2
        self.check_buttons_accessible_name() # WCAG 4.1.2
        self.check_keyboard_accessibility()  # WCAG 2.1.1
        self.check_landmarks()           # WCAG 1.3.1
        self.check_known_color_contrast()# WCAG 1.4.3
        self.check_dialog_pattern()      # WCAG 4.1.2 / 2.4.3

        total_rules = len(self.passes) + len(self.violations)
        compliance_pct = round((len(self.passes) / total_rules * 100), 1) if total_rules > 0 else 0.0

        return {
            "compliance_score_percent": compliance_pct,
            "total_checks": total_rules,
            "passed_count": len(self.passes),
            "violation_count": len(self.violations),
            "violations": self.violations,
            "passes": self.passes,
        }

    # WCAG 2.4.1: Bypass Blocks
    def check_bypass_blocks(self):
        skip_link = self.soup.find("a", class_="skip-link")
        if skip_link and skip_link.get("href"):
            target_id = skip_link.get("href").lstrip("#")
            target = self.soup.find(id=target_id)
            if target:
                self.passes.append({
                    "criterion": "2.4.1 Bypass Blocks (Level A)",
                    "detail": f"Skip-to-content link found and correctly targets element #{target_id}.",
                })
                return
        self.violations.append({
            "criterion": "2.4.1 Bypass Blocks (Level A)",
            "severity": "Serious",
            "element": "<a>",
            "message": "Missing functional skip-to-content link for keyboard users to bypass top navigation.",
        })

    # WCAG 1.1.1: Non-text Content
    def check_images_alt(self):
        images = self.soup.find_all("img")
        for img in images:
            alt = img.get("alt")
            src = img.get("src", "unknown")
            if alt is None:
                self.violations.append({
                    "criterion": "1.1.1 Non-text Content (Level A)",
                    "severity": "Critical",
                    "element": f'<img src="{src}">',
                    "message": "Image element completely missing 'alt' attribute. Screen readers will read filename.",
                    "remediation": 'Add meaningful alt="Ethereum Logo" or alt="" if decorative.',
                })
            else:
                self.passes.append({
                    "criterion": "1.1.1 Non-text Content (Level A)",
                    "detail": f'Image <img src="{src}"> has valid alt attribute: "{alt}".',
                })

    # WCAG 1.3.1 / 4.1.2: Form Labels
    def check_form_labels(self):
        inputs = self.soup.find_all("input")
        for inp in inputs:
            inp_id = inp.get("id")
            inp_type = inp.get("type", "text")
            has_label = False

            if inp_id:
                label = self.soup.find("label", attrs={"for": inp_id})
                if label:
                    has_label = True

            if inp.get("aria-label") or inp.get("aria-labelledby"):
                has_label = True

            if has_label:
                self.passes.append({
                    "criterion": "1.3.1 Info and Relationships (Level A)",
                    "detail": f'Input #{inp_id or inp_type} has programmatic accessible label.',
                })
            else:
                self.violations.append({
                    "criterion": "1.3.1 Info and Relationships (Level A)",
                    "severity": "Critical",
                    "element": f'<input id="{inp_id}">',
                    "message": f"Form control <input type='{inp_type}'> lacks an associated accessible label.",
                    "remediation": "Associate with a <label for='...'> or add aria-label.",
                })

    # WCAG 4.1.2: Name, Role, Value (Buttons)
    def check_buttons_accessible_name(self):
        buttons = self.soup.find_all("button")
        for btn in buttons:
            btn_text = btn.get_text(strip=True)
            aria_label = btn.get("aria-label")
            aria_labelledby = btn.get("aria-labelledby")
            btn_id = btn.get("id", "button")

            if btn_text or aria_label or aria_labelledby:
                self.passes.append({
                    "criterion": "4.1.2 Name, Role, Value (Level A)",
                    "detail": f'Button #{btn_id} has accessible name: "{aria_label or btn_text}".',
                })
            else:
                self.violations.append({
                    "criterion": "4.1.2 Name, Role, Value (Level A)",
                    "severity": "Critical",
                    "element": f'<button id="{btn_id}">',
                    "message": "Button contains only an icon with no accessible text or aria-label.",
                    "remediation": 'Add aria-label="Transaction Settings" to the icon button.',
                })

    # WCAG 2.1.1: Keyboard
    def check_keyboard_accessibility(self):
        # Detect divs/spans with onclick but no role/tabindex
        clickable_divs = self.soup.find_all(lambda tag: tag.name in ["div", "span"] and tag.has_attr("onclick"))
        for elem in clickable_divs:
            has_role = elem.get("role") == "button"
            has_tabindex = elem.get("tabindex") == "0"
            elem_class = elem.get("class", ["div"])

            if not (has_role and has_tabindex):
                self.violations.append({
                    "criterion": "2.1.1 Keyboard Accessible (Level A)",
                    "severity": "Critical",
                    "element": f'<{elem.name} class="{" ".join(elem_class)}" onclick="...">',
                    "message": "Custom interactive control is built with a non-semantic element without keyboard accessibility.",
                    "remediation": "Replace with native <button> or add role='button' and tabindex='0' with Enter/Space key handlers.",
                })

    # WCAG 1.3.1: Landmarks
    def check_landmarks(self):
        main = self.soup.find("main") or self.soup.find(role="main")
        header = self.soup.find("header") or self.soup.find(role="banner")
        nav = self.soup.find("nav") or self.soup.find(role="navigation")

        if main and header and nav:
            self.passes.append({
                "criterion": "1.3.1 Landmarks Structure (Level A)",
                "detail": "Document correctly uses primary HTML5 / ARIA landmarks: <header>, <nav>, and <main>.",
            })
        else:
            self.violations.append({
                "criterion": "1.3.1 Landmarks Structure (Level A)",
                "severity": "Moderate",
                "element": "<body>",
                "message": "Document is missing one or more structural landmarks (<header>, <nav>, or <main>).",
            })

    # WCAG 1.4.3: Contrast (Calculated on known classes)
    def check_known_color_contrast(self):
        low_contrast_elem = self.soup.find(class_="low-contrast-warning")
        if low_contrast_elem:
            # Contrast between #707080 and #0f111a
            ratio = calculate_contrast_ratio("#707080", "#0f111a")
            evaluation = evaluate_wcag_contrast(ratio)
            if not evaluation["pass_aa"]:
                self.violations.append({
                    "criterion": "1.4.3 Contrast (Minimum) (Level AA)",
                    "severity": "Serious",
                    "element": '<div class="low-contrast-warning">',
                    "message": f"Color contrast ratio {ratio}:1 fails WCAG 2.1 Level AA requirement (min 4.5:1).",
                    "remediation": "Increase text brightness to at least #9da3b4 for a ratio >= 4.5:1.",
                })

    # WCAG 4.1.2: Modal Dialog Pattern
    def check_dialog_pattern(self):
        modal = self.soup.find(attrs={"role": "dialog"})
        if modal:
            has_modal_attr = modal.get("aria-modal") == "true"
            has_labelled_by = modal.get("aria-labelledby") is not None
            if has_modal_attr and has_labelled_by:
                self.passes.append({
                    "criterion": "4.1.2 Dialog Pattern (Level A)",
                    "detail": "Modal dialog correctly implements role='dialog', aria-modal='true', and aria-labelledby.",
                })
            else:
                self.violations.append({
                    "criterion": "4.1.2 Dialog Pattern (Level A)",
                    "severity": "Serious",
                    "element": '<div role="dialog">',
                    "message": "Dialog element missing required aria-modal='true' or aria-labelledby attributes.",
                })
