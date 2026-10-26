"""
Frontend Error Boundary & Broken Assets Crawler.
Detects unhandled React crashes, blank screen errors, broken images, and missing critical assets.
"""
import re
from typing import Dict, List
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

CRASH_SIGNATURES = [
    (r"Minified React error #[0-9]+", "Minified React Runtime Exception (White Screen of Death)"),
    (r"Cannot read propert(?:y|ies) of (?:undefined|null)", "Null Pointer / Undefined Property Crash"),
    (r"Unhandled Runtime Error", "Next.js / Vite Unhandled Runtime Error Overlay"),
    (r"ChunkLoadError: Loading chunk [0-9]+ failed", "Dynamic Import / Code-Splitting Asset Failure"),
    (r"Application error: a client-side exception has occurred", "Next.js Fatal Client Crash"),
    (r"500 Internal Server Error", "Uncaught Backend Server Crash"),
]


async def crawl_and_audit_errors(base_url: str) -> Dict:
    detected_errors = []
    broken_assets = []
    checked_assets_count = 0

    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        try:
            res = await client.get(base_url)
            html = res.text
            status = res.status_code
        except Exception as e:
            return {"error": f"Cannot connect to target: {str(e)}", "crashes": []}

        # 1. Inspect main page for crash signatures
        for pattern, label in CRASH_SIGNATURES:
            if re.search(pattern, html, re.IGNORECASE):
                detected_errors.append({
                    "type": "FATAL_UI_CRASH",
                    "label": label,
                    "url": base_url,
                    "severity": "CRITICAL",
                    "impact": "User sees a completely blank screen or crash modal upon landing.",
                })

        # 2. Extract and check all images (<img src="...">)
        soup = BeautifulSoup(html, "html.parser")
        images = soup.find_all("img", src=True)

        for img in images[:15]:  # Check first 15 images
            src = img["src"]
            img_url = urljoin(base_url, src)
            checked_assets_count += 1
            try:
                img_res = await client.head(img_url)
                if img_res.status_code >= 400:
                    broken_assets.append({
                        "asset_type": "Image",
                        "url": img_url,
                        "status_code": img_res.status_code,
                        "severity": "MODERATE",
                        "message": f"Broken image source returned HTTP {img_res.status_code}.",
                    })
            except Exception:
                broken_assets.append({
                    "asset_type": "Image",
                    "url": img_url,
                    "status_code": 0,
                    "severity": "MODERATE",
                    "message": "Connection error loading image asset.",
                })

        # 3. Check favicon
        try:
            checked_assets_count += 1
            fav_res = await client.get(urljoin(base_url, "/favicon.ico"))
            if fav_res.status_code >= 400:
                broken_assets.append({
                    "asset_type": "Favicon",
                    "url": urljoin(base_url, "/favicon.ico"),
                    "status_code": fav_res.status_code,
                    "severity": "MINOR",
                    "message": "Missing /favicon.ico (Causes 404 log clutter in production).",
                })
        except Exception:
            pass

    return {
        "status": "COMPLETED",
        "assets_checked": checked_assets_count,
        "ui_crashes_found": len(detected_errors),
        "broken_assets_found": len(broken_assets),
        "crashes": detected_errors,
        "broken_assets": broken_assets,
    }
