# 🔐 SecuraMind — AI-Powered Secure Code Assistant

![SecuraMind Logo](./assets/securamind-banner.png)

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

- **Python 3.10**
- **Modal Labs** (LLM inference)
- **OpenAI / Claude / Mistral API**
- **FastAPI** (for public API layer)
- **Colab / Jupyter Notebooks** (demo + dev)
- **Tailwind UI** (planned frontend)
- **GitHub Actions** (planned CI integration)

---

## 🧪 Quickstart (Using Modal)

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/securamind.git
cd securamind
```

### 2. Install Modal

```bash
pip install modal
```

### 3. Authenticate with Modal

**Recommended:** Authenticate via your local terminal:

```bash
modal token new
```

Then follow the link in your browser to log in. This stores your auth token locally.

> 💡 If using Google Colab, run this locally first — then your Colab will work too.

---

## 🧠 Example: LLM-Based Code Fix with Modal

```python
# fixer_modal.py
from modal import Stub, Image

image = Image.debian_slim().pip_install("openai")
stub = Stub("securamind-fixer", image=image)

@stub.function()
def fix_code_modal(code: str, issues: list):
    import openai
    openai.api_key = "sk-..."  # Recommended: use Modal secrets
    # Simulated LLM fix (replace with actual call)
    return f"[MODAL FIX] Fixed {len(issues)} issues in {len(code)} characters."
```

#### Call It in Code

```python
from fixer_modal import fix_code_modal

fixed = fix_code_modal.remote("vulnerable_code_here()", [{"issue": "XSS"}])
```

---

## 🌐 Optional: Public API Endpoint

```python
@stub.function()
@asgi_app()
def web_app():
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

Now accessible at:

```
https://<username>--securamind-fixer.modal.run/fix
```

---

## 🧰 Roadmap (Future Works)

- 🔄 Real-time CI integration
- 🧩 VSCode plugin
- 🔍 Inline code annotations
- 📊 Security trend dashboards
- 🔐 Role-based analysis workflows

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

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📄 License

[MIT](LICENSE)

---

## 📬 Contact

- **Author:** Pranay Sharma  
-**Email:**pranaysharma5626@gmail.com 
---
