"""
Secrets & Sensitive Credentials Scanner for Vibe-Coded Web Apps.
Extracts HTML and downloads linked JavaScript bundles to detect leaked API keys:
- OpenAI, Anthropic, Stripe Secret Keys, Supabase Service Role, AWS Keys, Private Keys.
"""
import base64
import json
import re
from typing import Dict, List
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

# Production-grade Regex Signatures for Leaked Secrets
SECRET_PATTERNS = {
    "Stripe Secret Key": {
        "regex": r"(?:sk_(?:live|test)_[0-9a-zA-Z]{24,})",
        "severity": "CRITICAL",
        "impact": "Full access to Stripe billing account. Attackers can create charges or drain balances.",
        "remediation": "Move Stripe secret key to backend environment variables. Never expose in client code.",
    },
    "Stripe Restricted Key": {
        "regex": r"(?:rk_live_[0-9a-zA-Z]{24,})",
        "severity": "HIGH",
        "impact": "Restricted access to Stripe account operations.",
        "remediation": "Keep restricted keys on backend servers only.",
    },
    "OpenAI API Key": {
        "regex": r"(?:sk-[a-zA-Z0-9]{48}|sk-proj-[a-zA-Z0-9_-]{80,})",
        "severity": "CRITICAL",
        "impact": "Allows attackers to drain OpenAI credits and access organization fine-tuned models.",
        "remediation": "Proxy all LLM requests through a backend server (e.g. Next.js Route Handler / FastAPI).",
    },
    "Anthropic API Key": {
        "regex": r"(?:sk-ant-[a-zA-Z0-9_-]{80,})",
        "severity": "CRITICAL",
        "impact": "Direct access to Anthropic Claude quota and billable API calls.",
        "remediation": "Store ANTHROPIC_API_KEY in server-only secrets (.env).",
    },
    "AWS Access Key ID": {
        "regex": r"(?:AKIA[0-9A-Z]{16})",
        "severity": "HIGH",
        "impact": "Potential compromise of AWS infrastructure and cloud services.",
        "remediation": "Rotate AWS IAM key immediately and use IAM roles.",
    },
    "GitHub Personal Token": {
        "regex": r"(?:ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{82})",
        "severity": "CRITICAL",
        "impact": "Access to private GitHub repositories, commits, and workflows.",
        "remediation": "Revoke token on GitHub and migrate to GitHub Apps.",
    },
    "Ethereum / Web3 Private Key": {
        "regex": r"(?:0x[a-fA-F0-9]{64})",
        "severity": "CRITICAL",
        "impact": "Full custody loss of crypto wallet funds and smart contract admin rights.",
        "remediation": "Never hardcode private keys in frontend bundles.",
    },
}


def mask_secret(secret: str) -> str:
    """Masks secret keeping only prefix and last 4 characters for evidence."""
    if len(secret) <= 12:
        return secret[:3] + "..." + secret[-2:]
    return secret[:8] + "..." + secret[-4:]


def check_supabase_service_role(text: str) -> List[Dict]:
    """Detects leaked Supabase Service Role JWTs which bypass Row Level Security (RLS)."""
    findings = []
    jwt_pattern = r"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+"
    matches = re.findall(jwt_pattern, text)
    for m in matches:
        try:
            payload_b64 = m.split(".")[1]
            padded = payload_b64 + "=" * (-len(payload_b64) % 4)
            payload_json = json.loads(base64.urlsafe_b64decode(padded))
            if payload_json.get("role") == "service_role":
                findings.append({
                    "secret_type": "Supabase Service Role Key (Bypasses RLS)",
                    "severity": "CRITICAL",
                    "masked_value": mask_secret(m),
                    "impact": "Allows ANY user to bypass Supabase Row Level Security and read/write the entire database.",
                    "remediation": "Use SUPABASE_ANON_KEY on the client. Keep SERVICE_ROLE_KEY exclusively on backend.",
                })
        except Exception:
            continue
    return findings


async def scan_url_for_secrets(base_url: str) -> Dict:
    """Scans target landing page HTML and all internal JavaScript bundles for exposed secrets."""
    findings = []
    scanned_assets = []

    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        try:
            res = await client.get(base_url)
            scanned_assets.append(base_url)
            html_content = res.text
        except Exception as e:
            return {"error": f"Failed to connect to target URL: {str(e)}", "findings": []}

        # 1. Scan root HTML
        for name, meta in SECRET_PATTERNS.items():
            for match in re.findall(meta["regex"], html_content):
                findings.append({
                    "secret_type": name,
                    "severity": meta["severity"],
                    "source": "HTML Document",
                    "masked_value": mask_secret(match),
                    "impact": meta["impact"],
                    "remediation": meta["remediation"],
                })

        findings.extend(check_supabase_service_role(html_content))

        # 2. Extract script tags and scan external JS bundles
        soup = BeautifulSoup(html_content, "html.parser")
        scripts = soup.find_all("script", src=True)
        base_domain = urlparse(base_url).netloc

        for s in scripts:
            src = s["src"]
            full_js_url = urljoin(base_url, src)

            # Focus on same-origin or local bundle scripts
            js_domain = urlparse(full_js_url).netloc
            if js_domain and js_domain != base_domain and not ("localhost" in js_domain or "127.0.0.1" in js_domain):
                continue

            try:
                js_res = await client.get(full_js_url)
                scanned_assets.append(full_js_url)
                js_text = js_res.text

                for name, meta in SECRET_PATTERNS.items():
                    for match in re.findall(meta["regex"], js_text):
                        findings.append({
                            "secret_type": name,
                            "severity": meta["severity"],
                            "source": f"JS Bundle: {src}",
                            "masked_value": mask_secret(match),
                            "impact": meta["impact"],
                            "remediation": meta["remediation"],
                        })

                findings.extend(check_supabase_service_role(js_text))
            except Exception:
                continue

    return {
        "status": "COMPLETED",
        "assets_scanned": len(scanned_assets),
        "scanned_urls": scanned_assets,
        "leak_count": len(findings),
        "critical_leaks": sum(1 for f in findings if f["severity"] == "CRITICAL"),
        "findings": findings,
    }
