"""
Fixer Tool for SecuraMind
- Uses an LLM to explain and fix security issues in code snippets
- Supports Claude, OpenAI, or Mistral-compatible APIs
"""

import os
import requests

# Choose one: "anthropic", "openai", or "mistral"
LLM_PROVIDER = "anthropic"
API_KEY = "your_api_key_here"

def build_prompt(code, issues):
    issue_summary = "\\n".join(f"- {i['issue']} on line {i['line_number']}: {i['line']}" for i in issues)
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

def call_llm(prompt):
    if LLM_PROVIDER == "anthropic":
        return call_claude(prompt)
    elif LLM_PROVIDER == "openai":
        return call_openai(prompt)
    elif LLM_PROVIDER == "mistral":
        return call_mistral(prompt)
    else:
        return "❌ Invalid LLM provider."

def call_claude(prompt):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 800,
        "temperature": 0.4,
        "messages": [{"role": "user", "content": prompt}]
    }
    r = requests.post(url, json=payload, headers=headers)
    return r.json().get("content", [{"text": "❌ Error or empty response."}])[0]["text"]

def call_openai(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 800
    }
    r = requests.post(url, json=data, headers=headers)
    return r.json()["choices"][0]["message"]["content"]

def call_mistral(prompt):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": "mistral-small",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 800
    }
    r = requests.post(url, json=data, headers=headers)
    return r.json()["choices"][0]["message"]["content"]

def fix_code(code: str, issues: list) -> dict:
    if not issues or not code.strip():
        return {"error": "Code and issues are required."}

    prompt = build_prompt(code, issues)
    try:
        response = call_llm(prompt)
        return {"explanation_and_fix": response}
    except Exception as e:
        return {"error": str(e)}