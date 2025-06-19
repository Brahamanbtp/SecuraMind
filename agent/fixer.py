# agent/fixer.py — Modal 1.0.2 compatible with local test entrypoint

import os
import modal

# Modal App and image setup
app = modal.App("securamind-fixer")

image = modal.Image.debian_slim().pip_install("requests")

# Cloud function to fix insecure code using Mistral
@app.function(
    image=image,
    secrets=[modal.Secret.from_name("securamind-api-keys")]
)
def fix_code_modal(code: str, issues: list) -> dict:
    import requests

    API_KEY = os.environ.get("MISTRAL_API_KEY")

    def build_prompt(code, issues):
        issue_summary = "\n".join(
            f"- {i['issue']} on line {i['line_number']}: {i['line']}" for i in issues
        )
        return f"""
You are a secure code assistant.

Below is a potentially insecure code snippet. Analyze the code, explain the security issues listed, and then rewrite the code securely.

### Insecure Code:
{code}

### Issues Detected:
{issue_summary}

### Your Tasks:
1. Explain each issue in simple terms.
2. Provide a secure and corrected version of the code.
Return only the explanation followed by the fixed code.
"""

    prompt = build_prompt(code, issues)

    def call_mistral(prompt):
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        data = {
            "model": "mistral-small",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,
            "max_tokens": 800
        }
        r = requests.post(url, json=data, headers=headers)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    try:
        output = call_mistral(prompt)
        return {"explanation_and_fix": output}
    except Exception as e:
        return {"error": str(e)}

# ✅ Local test entrypoint (called via `modal run -m agent.fixer`)
# Optional: Local test entrypoint (for modal run)
@app.local_entrypoint()
def main():
    test_code = '''
import os
password = "1234"
os.system("rm -rf /")
'''
    test_issues = [
        {"line_number": 2, "line": 'password = "1234"', "issue": "Hardcoded password/API key"},
        {"line_number": 3, "line": 'os.system("rm -rf /")', "issue": "Use of os.system()"}
    ]

    # ✅ Use .local() to invoke Modal function locally
    result = fix_code_modal.local(test_code, test_issues)
    print("🧪 Fix result:\n", result)

