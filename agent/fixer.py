# fixer_modal.py (Cloud-based fixer for SecuraMind using Modal and Mistral)

import os
import modal

# Set up Modal stub
stub = modal.Stub("securamind-fixer")

# Use default Modal Python image with requests preinstalled
image = modal.Image.debian_slim().pip_install("requests")

@stub.function(image=image, secret=modal.Secret.from_name("securamind-api-keys"))
def fix_code_modal(code: str, issues: list) -> dict:
    import requests

    API_KEY = os.environ.get("ak-2iQ1O30002OYfnmuBBhbHv")

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
