"""
URL Checker Tool for SecuraMind
- Performs heuristic analysis of URLs
- Optionally integrates with VirusTotal for external threat reports
"""

import re
import requests

# -----------------------------
# Config: Optional VirusTotal
# -----------------------------
USE_VIRUSTOTAL = False  # Set True to enable VirusTotal scan
VIRUSTOTAL_API_KEY = "your_api_key_here"

# -----------------------------
# Helper Functions
# -----------------------------

def basic_url_heuristics(url: str) -> dict:
    """Applies regex-based heuristic checks on the URL."""
    suspicious_patterns = {
        "IP in URL": r"https?://\d{1,3}(?:\.\d{1,3}){3}",
        "Long URL": r".{75,}",
        "Suspicious TLD": r"\.(tk|ml|ga|cf|gq)(/|$)",
        "Encoded characters": r"%[0-9a-fA-F]{2}",
        "Multiple subdomains": r"https?://([^.]+\.){3,}"
    }

    findings = []
    for reason, pattern in suspicious_patterns.items():
        if re.search(pattern, url):
            findings.append(reason)

    verdict = "Suspicious" if findings else "Clean"
    return {
        "url": url,
        "heuristic_findings": findings,
        "verdict": verdict
    }

def check_with_virustotal(url: str) -> dict:
    if not USE_VIRUSTOTAL or VIRUSTOTAL_API_KEY == "your_api_key_here":
        return {"error": "VirusTotal scan disabled or API key not set."}
    
    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY
    }
    params = {"url": url}
    response = requests.post("https://www.virustotal.com/api/v3/urls", data=params, headers=headers)

    if response.status_code == 200:
        result = response.json()
        data_id = result.get("data", {}).get("id", "")
        analysis_url = f"https://www.virustotal.com/gui/url/{data_id.replace('-', '')}/detection"
        return {
            "message": "URL submitted to VirusTotal.",
            "analysis_url": analysis_url,
            "id": data_id
        }
    else:
        return {
            "error": f"VirusTotal request failed: {response.text}"
        }

# -----------------------------
# Main Scan Function
# -----------------------------

def scan_url(url: str) -> dict:
    if not url.startswith("http"):
        url = "http://" + url  # Normalize for consistency

    result = {}
    result["heuristic_analysis"] = basic_url_heuristics(url)

    if USE_VIRUSTOTAL:
        result["virustotal"] = check_with_virustotal(url)

    return result
