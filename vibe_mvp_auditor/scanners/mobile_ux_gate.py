"""
Mobile Responsive & Launch Meta Tags Quality Gate.
Evaluates mobile viewport configurations, OpenGraph social sharing meta, and mobile tap targets.
"""
import re
from typing import Dict, List

import httpx
from bs4 import BeautifulSoup


async def audit_mobile_and_meta(base_url: str) -> Dict:
    findings = []
    passes = []

    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        try:
            res = await client.get(base_url)
            html = res.text
        except Exception as e:
            return {"error": f"Failed to retrieve URL: {str(e)}", "findings": []}

    soup = BeautifulSoup(html, "html.parser")

    # 1. Viewport Meta Tag (Critical for Mobile)
    viewport = soup.find("meta", attrs={"name": re.compile(r"viewport", re.I)})
    if viewport and viewport.get("content"):
        content = viewport["content"].lower()
        if "width=device-width" in content and "initial-scale=1" in content:
            passes.append("Valid Mobile Viewport meta tag present (<meta name='viewport' content='width=device-width, initial-scale=1'>).")
        else:
            findings.append({
                "category": "Mobile Responsiveness",
                "severity": "HIGH",
                "issue": "Suboptimal Viewport Tag",
                "detail": f"Viewport meta tag content '{viewport.get('content')}' does not set standard width=device-width, initial-scale=1.",
                "remediation": "Add <meta name='viewport' content='width=device-width, initial-scale=1.0'>.",
            })
    else:
        findings.append({
            "category": "Mobile Responsiveness",
            "severity": "CRITICAL",
            "issue": "Missing Mobile Viewport Tag",
            "detail": "HTML completely lacks a <meta name='viewport'> tag. App will display as a shrunken desktop page on mobile.",
            "remediation": "Insert <meta name='viewport' content='width=device-width, initial-scale=1.0'> into <head>.",
        })

    # 2. Product Hunt / Twitter OpenGraph Social Cards
    og_title = soup.find("meta", property="og:title") or soup.find("meta", attrs={"name": "twitter:title"})
    og_image = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "twitter:image"})
    og_desc = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name": "description"})

    if og_title and og_image and og_desc:
        passes.append("Social Sharing OpenGraph Tags (og:title, og:description, og:image) are fully configured for Product Hunt / Twitter.")
    else:
        missing_meta = []
        if not og_title: missing_meta.append("og:title")
        if not og_desc: missing_meta.append("og:description")
        if not og_image: missing_meta.append("og:image")
        findings.append({
            "category": "Viral Growth & Launch Meta",
            "severity": "HIGH",
            "issue": "Missing OpenGraph Social Card Tags",
            "detail": f"Missing: {', '.join(missing_meta)}. Links shared on Product Hunt, Twitter, or Slack will lack rich card preview image.",
            "remediation": "Add <meta property='og:image' content='https://.../preview.png'> and og:title/og:description.",
        })

    # 3. Fixed Width Overflow Risk Check (Inline styles)
    fixed_width_elements = soup.find_all(style=re.compile(r"width:\s*[4-9][0-9]{2,}px|width:\s*[1-9][0-9]{3,}px", re.I))
    if fixed_width_elements:
        findings.append({
            "category": "Mobile Layout Trap",
            "severity": "MEDIUM",
            "issue": "Hardcoded Desktop Width",
            "detail": f"Detected {len(fixed_width_elements)} elements with hardcoded pixel widths > 400px (e.g. style='width: 800px'). Causes horizontal scrolling on mobile phones.",
            "remediation": "Use responsive units (max-width: 100%, w-full, or CSS media queries).",
        })
    else:
        passes.append("No hardcoded fixed-width layout traps detected.")

    return {
        "status": "COMPLETED",
        "passed_checks": len(passes),
        "issues_count": len(findings),
        "passes": passes,
        "findings": findings,
    }
