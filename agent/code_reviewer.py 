"""
Code Reviewer Tool for SecuraMind
- Scans code snippets to identify common security issues
- Uses rule-based heuristics inspired by OWASP Top 10
"""

import re

# Define risky patterns to scan for
SECURITY_PATTERNS = [
    {"issue": "Use of eval()", "pattern": r"\beval\s*\(", "severity": "high"},
    {"issue": "Use of exec()", "pattern": r"\bexec\s*\(", "severity": "high"},
    {"issue": "Use of os.system()", "pattern": r"os\.system\s*\(", "severity": "medium"},
    {"issue": "Use of subprocess", "pattern": r"subprocess\.(Popen|call|run)", "severity": "medium"},
    {"issue": "Hardcoded password/API key", "pattern": r"(password|passwd|api[_-]?key)\s*=\s*[\"'].*[\"']", "severity": "high"},
    {"issue": "Raw SQL query", "pattern": r"(SELECT|INSERT|UPDATE|DELETE)\s+.*\s+FROM\s+", "severity": "medium"},
    {"issue": "Input used in query directly", "pattern": r"input\(.*\).*['\"]\s*(SELECT|INSERT|UPDATE|DELETE)", "severity": "high"},
]

def review_code(code: str) -> dict:
    lines = code.strip().splitlines()
    issues_found = []

    for i, line in enumerate(lines, 1):
        for rule in SECURITY_PATTERNS:
            if re.search(rule["pattern"], line, re.IGNORECASE):
                issues_found.append({
                    "line_number": i,
                    "line": line.strip(),
                    "issue": rule["issue"],
                    "severity": rule["severity"]
                })

    verdict = "Issues Found" if issues_found else "No major issues detected"
    return {
        "verdict": verdict,
        "issue_count": len(issues_found),
        "issues": issues_found
    }