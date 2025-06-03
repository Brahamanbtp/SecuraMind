"""
File Scanner Tool for SecuraMind
- Detects potentially malicious or suspicious files
- Supports local heuristic checks and optional VirusTotal scan
"""

import os
import mimetypes
import hashlib
import requests

# -----------------------------
# Config: Optional VirusTotal
# -----------------------------
USE_VIRUSTOTAL = False  # Set to True if you have an API key
VIRUSTOTAL_API_KEY = "your_api_key_here"  # Replace if needed

# -----------------------------
# Helper Functions
# -----------------------------

def get_file_info(filepath):
    size = os.path.getsize(filepath)
    mime_type, _ = mimetypes.guess_type(filepath)
    with open(filepath, "rb") as f:
        content = f.read()
        sha256 = hashlib.sha256(content).hexdigest()
    return {
        "name": os.path.basename(filepath),
        "size_bytes": size,
        "mime_type": mime_type,
        "sha256": sha256
    }

def local_heuristic_analysis(filepath):
    """Very basic detection of suspicious content."""
    suspicious_keywords = [b"powershell", b"eval(", b"base64_decode", b"exec(", b"<script>", b"import os", b"subprocess"]
    findings = []
    try:
        with open(filepath, "rb") as f:
            content = f.read()
            for keyword in suspicious_keywords:
                if keyword in content:
                    findings.append(keyword.decode("utf-8", errors="ignore"))
    except Exception as e:
        return {"error": str(e)}

    return {
        "suspicious_keywords_found": findings,
        "verdict": "Suspicious" if findings else "Clean"
    }

def scan_with_virustotal(filepath):
    if not USE_VIRUSTOTAL or VIRUSTOTAL_API_KEY == "your_api_key_here":
        return {"error": "VirusTotal scanning is disabled or API key not set."}

    with open(filepath, "rb") as f:
        files = {"file": (os.path.basename(filepath), f)}
        headers = {"x-apikey": VIRUSTOTAL_API_KEY}
        response = requests.post("https://www.virustotal.com/api/v3/files", files=files, headers=headers)
        if response.status_code == 200:
            result = response.json()
            analysis_id = result.get("data", {}).get("id")
            return {"message": "Uploaded to VirusTotal", "analysis_id": analysis_id}
        else:
            return {"error": f"Upload failed: {response.text}"}

# -----------------------------
# Main Scan Function
# -----------------------------

def scan_file(filepath):
    if not os.path.isfile(filepath):
        return {"error": "Invalid file path"}

    result = {}
    result["file_info"] = get_file_info(filepath)
    result["local_analysis"] = local_heuristic_analysis(filepath)

    if USE_VIRUSTOTAL:
        result["virustotal"] = scan_with_virustotal(filepath)

    return result