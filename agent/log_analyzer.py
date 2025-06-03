"""
Log Analyzer Tool for SecuraMind
- Scans logs to extract and categorize potential anomalies
- Supports rule-based detection of errors, warnings, login failures, etc.
"""

import re

def parse_log_lines(log_text):
    lines = log_text.strip().splitlines()
    return [line.strip() for line in lines if line.strip()]

def detect_log_anomalies(log_lines):
    patterns = {
        "Error": re.compile(r"\b(error|fail|exception|critical)\b", re.IGNORECASE),
        "Warning": re.compile(r"\b(warn|deprecated|caution)\b", re.IGNORECASE),
        "Authentication Issue": re.compile(r"(unauthorized|access denied|login failed|invalid credentials)", re.IGNORECASE),
        "Network Issue": re.compile(r"(timeout|connection refused|host unreachable|dns failure)", re.IGNORECASE)
    }

    findings = {category: [] for category in patterns}
    findings["Unmatched"] = []

    for line in log_lines:
        matched = False
        for category, pattern in patterns.items():
            if pattern.search(line):
                findings[category].append(line)
                matched = True
                break
        if not matched:
            findings["Unmatched"].append(line)

    summary = {k: len(v) for k, v in findings.items()}
    return {"summary": summary, "matches": findings}

def analyze_log(log_text):
    if not log_text.strip():
        return {"error": "Empty log content provided."}

    lines = parse_log_lines(log_text)
    result = detect_log_anomalies(lines)
    return {
        "line_count": len(lines),
        "analysis": result
    }