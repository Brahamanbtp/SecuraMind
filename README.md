---
title: SecuraMind
emoji: 🛡️
colorFrom: gray
colorTo: blue
sdk: gradio
sdk_version: 4.18.0
app_file: ui/app.py
license: apache-2.0
---

# 🔐 SecuraMind — AI-Powered Secure Code Assistant

SecuraMind is a secure coding assistant that helps developers identify and fix code vulnerabilities using powerful LLMs. Designed for performance, scalability, and integration into CI pipelines, it empowers developers to write secure code — fast.

> 🧠 Powered by **LLM inference** via [Modal Labs](https://modal.com)  
> 🛡️ Use Cases: Code Fixing, Log Analysis, Threat Summaries, Developer Assistance

---

## 🔥 Key Features

| Feature                         | Description |
|--------------------------------|-------------|
| ✅ LLM-Powered Fixes            | Automatically detects and fixes insecure code via OpenAI/Claude |
| ✅ Modal Integration            | Serverless deployment of heavy LLM workloads with zero infra setup |
| ✅ Fast, Secure Execution       | Modal runs in containers — isolated, fast, and scalable |
| ✅ CLI + API Support            | Use from terminal, web app, or call via REST API |
| ✅ Role-Based Workflow (planned) | Integrate different security roles in analysis pipeline |

---

## ⚙️ Tech Stack

- **Python 3.10+**
- **Modal Labs** (LLM inference)
- **OpenAI / Claude / Mistral API**
- **Gradio** (for frontend interface)
- **FastAPI** (for public API layer)
- **Tailwind UI** (planned frontend styling)
- **GitHub Actions** (planned CI integration)

---

## 🧪 Quickstart (Using Modal)

### 1. Clone the Repo

```bash
git clone https://huggingface.co/spaces/Brahamanbtp/SecuraMind
cd SecuraMind
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Authenticate with Modal

```bash
modal token new
```

> Follow the link shown in terminal to authenticate via browser.  
> 💡 This stores your auth token locally so Modal functions can run.

---

## 🧠 Example: LLM-Based Code Fix (via Modal)

```python
# fixer_modal.py
from modal import App, Image

image = Image.debian_slim().pip_install("requests")
app = App("securamind-fixer", image=image)

@app.function()
def fix_code_modal(code: str, issues: list):
    # Secure call to LLM (e.g., Mistral/OpenAI) with prompt formatting
    ...
```

#### Calling the Fixer Function

```python
from agent.fixer import fix_code_modal
fixed = fix_code_modal.remote(code, issues)
```

---

## 🌐 Deploy Public API (Optional)

```python
@app.function()
@asgi_app()
def web_api():
    from fastapi import FastAPI, Request
    app = FastAPI()

    @app.post("/fix")
    async def fix(request: Request):
        data = await request.json()
        result = fix_code_modal.remote(data["code"], data["issues"])
        return {"fixed_code": result}
```

```bash
modal deploy fixer_modal.py
```

Access it at:

```
https://<your-username>--securamind-fixer.modal.run/fix
```

---

## 🧰 Roadmap (Planned Features)

- 🔄 GitHub CI/CD Secure PRs
- 🧩 VSCode plugin for inline scans
- 📊 Dashboards for org-wide security posture
- 🔐 Role-based analyst workflows

---

## 💡 Why Modal?

| Reason               | Benefit                         |
|----------------------|----------------------------------|
| ✅ Serverless LLMs    | No GPU setup required           |
| ✅ Infinite scale      | Handles high user load         |
| ✅ Secure containers   | Runs in isolated environments  |
| ✅ Simple API design   | Easy to test + deploy          |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss improvements or feature requests.

---

## 📄 License

This project is licensed under the [Apache 2.0 License](LICENSE).

---

## 📬 Contact

- **Author:** Pranay Sharma  
- **Email:** pranaysharma5626@gmail.com
