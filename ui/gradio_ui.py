"""
Gradio UI for SecuraMind
- Provides a web-based interface for all agent tools
"""

import sys
import os
import gradio as gr
import json

# Fix path so Python can find `core.agent_engine`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.agent_engine import SecuraMindAgent, IS_MODAL_FUNCTION

agent = SecuraMindAgent()

def handle_file_scan(file):
    return agent.scan_file(file.name)

def handle_url_scan(url):
    return agent.scan_url(url)

def handle_log_analysis(log_text):
    return agent.analyze_logs(log_text)

def handle_code_review(code):
    return agent.review_code(code)

def handle_code_fix(code, issues_json):
    try:
        issues = json.loads(issues_json)
        return agent.fix_code(code, issues).get("explanation_and_fix", "⚠️ No result.")
    except Exception as e:
        return f"❌ Error: {str(e)}"

def handle_review_and_fix(code):
    review = agent.review_code(code)
    if review.get("issue_count", 0) == 0:
        return review, "✅ No issues found."
    fix = agent.fix_code(code, review["issues"])
    return review, fix.get("explanation_and_fix", "⚠️ No fix output.")

def handle_encryption(file):
    return agent.encrypt_file(file.name)

def handle_decryption(enc_file, key_file, nonce_file):
    return agent.decrypt_file(enc_file.name, key_file.name, nonce_file.name)

with gr.Blocks(title="SecuraMind – AI Cybersecurity Copilot") as demo:
    gr.Markdown("## 🛡️ SecuraMind – AI Cybersecurity Copilot")

    with gr.Tab("🗂️ File Scanner"):
        file_input = gr.File(label="Upload File")
        file_btn = gr.Button("Scan File")
        file_output = gr.JSON()
        file_btn.click(handle_file_scan, inputs=file_input, outputs=file_output)

    with gr.Tab("🌐 URL Checker"):
        url_input = gr.Textbox(label="Enter URL")
        url_btn = gr.Button("Scan URL")
        url_output = gr.JSON()
        url_btn.click(handle_url_scan, inputs=url_input, outputs=url_output)

    with gr.Tab("📜 Log Analyzer"):
        log_input = gr.Textbox(lines=10, label="Paste Log Text")
        log_btn = gr.Button("Analyze Logs")
        log_output = gr.JSON()
        log_btn.click(handle_log_analysis, inputs=log_input, outputs=log_output)

    with gr.Tab("🧑‍💻 Code Reviewer"):
        code_input = gr.Code(label="Paste Code", language="python", lines=12)
        code_btn = gr.Button("Review Code")
        code_output = gr.JSON()
        code_btn.click(handle_code_review, inputs=code_input, outputs=code_output)

    with gr.Tab("🛠️ Code Fixer (Manual)"):
        gr.Markdown(
            "🌐 Using **Modal Cloud** for secure code fixing (🔒 secrets managed securely)"
            if IS_MODAL_FUNCTION else
            "⚠️ Using **Local fallback fixer** – cloud code fixing is not active."
        )
        fixer_code_input = gr.Code(label="Paste Code", language="python", lines=12)
        fixer_issues_input = gr.Textbox(
            label="Paste Issues as JSON",
            lines=6,
            placeholder='[{"line": "os.system(\'rm -rf /\')", "issue": "Use of os.system()", "line_number": 3}]'
        )
        fixer_btn = gr.Button("Fix Code")
        fixer_output = gr.Textbox(label="Explanation + Fixed Code", lines=20)
        fixer_btn.click(handle_code_fix, inputs=[fixer_code_input, fixer_issues_input], outputs=fixer_output)

    with gr.Tab("🤖 Review + Auto Fix"):
        gr.Markdown(
            "🌐 Using **Modal Cloud** for review + fix (powered by Mistral)"
            if IS_MODAL_FUNCTION else
            "⚠️ Local-only analysis active – cloud fixer is disabled."
        )
        ai_code_input = gr.Code(label="Paste Code", language="python", lines=12)
        ai_review_output = gr.JSON(label="🧪 Review Output")
        ai_fix_output = gr.Textbox(label="🛠️ AI Fix", lines=20)
        ai_btn = gr.Button("🔍 Review & Fix")
        ai_btn.click(handle_review_and_fix, inputs=ai_code_input, outputs=[ai_review_output, ai_fix_output])

    with gr.Tab("🔐 Encrypt / Decrypt Files"):
        gr.Markdown("### 🔒 Encrypt File")
        enc_file_input = gr.File(label="Select File to Encrypt")
        enc_btn = gr.Button("Encrypt")
        enc_output = gr.JSON()
        enc_btn.click(handle_encryption, inputs=enc_file_input, outputs=enc_output)

        gr.Markdown("### 🔁 Decrypt File")
        dec_file_input = gr.File(label="Encrypted .enc File")
        dec_key_input = gr.File(label=".key File")
        dec_nonce_input = gr.File(label=".nonce File")
        dec_btn = gr.Button("Decrypt")
        dec_output = gr.JSON()
        dec_btn.click(handle_decryption, inputs=[dec_file_input, dec_key_input, dec_nonce_input], outputs=dec_output)

demo.launch()
