# agent/fixer.py — Modal 1.0.2 compatible with local test + remote fixing + dotenv

import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env for local testing
load_dotenv()

try:
    import modal

    # ✅ Define Modal App and image (correct API)
    app = modal.App("securamind-fixer")
    image = modal.Image.debian_slim().pip_install("requests")

    # ✅ Modal cloud function with secret for remote access
    @app.function(
        image=image,
        secrets=[modal.Secret.from_name("securamind-api-keys")]
    )
    def fix_code_modal(code: str, issues: list) -> dict:
        import requests

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
            try:
                api_key = os.environ["MISTRAL_API_KEY"]
                print("🔑 API_KEY loaded: ✅ Yes")
            except KeyError:
                print("🔑 API_KEY loaded: ❌ No (MISTRAL_API_KEY not found)")
                return "❌ API Key not loaded from Modal secret (missing MISTRAL_API_KEY)"

            url = "https://api.mistral.ai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}"}
            data = {
                "model": "mistral-small",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.4,
                "max_tokens": 800
            }

            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

        try:
            result = call_mistral(prompt)
            return {"explanation_and_fix": result}
        except Exception as e:
            return {"error": str(e)}

    IS_MODAL_FUNCTION = True

except ImportError:
    # Fallback: Modal not available
    def fix_code_modal(code: str, issues: list) -> dict:
        return {
            "error": "Modal is not available in this environment. Cloud fixing disabled."
        }

    IS_MODAL_FUNCTION = False

# ✅ Local test entrypoint (used via: `modal run -m agent.fixer`)
if IS_MODAL_FUNCTION:
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
        result = fix_code_modal.remote(test_code, test_issues)
        print("🧪 Fix result:\n", result)
