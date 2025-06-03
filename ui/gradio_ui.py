"""
Gradio UI for SecuraMind
- Provides a web-based interface for all agent tools
"""

import gradio as gr

from agent.file_scanner import scan_file
from agent.url_checker import scan_url
from agent.log_analyzer import analyze_log
from agent.code_reviewer import review_code
from agent.fixer import fix_code
from agent.encryptor import encrypt_file, decrypt_file

def handle_file_scan(file):
    return scan_file(file.name)

def handle_url_scan(url):
    return scan_url(url)

def handle_log_analysis(log_text):
    return analyze_log(log_text)

def handle_code_review(code):
    return review_code(code)

def handle_code_fix(code, issues_json):
    try:
        import json
        issues = json.loads(issues_json)
        return fix_code(code, issues)
    except Exception as e:
        return {"error": str(e)}

def handle_encryption(file):
    return encrypt_file(file.name)

def handle_decryption(enc_file, key_file, nonce_file):
    return decrypt_file(enc_file.name, key_file.name, nonce_file.name)

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
        code_input = gr.Code(label="Paste Code")
        code_btn = gr.Button("Review Code")
        code_output = gr.JSON()
        code_btn.click(handle_code_review, inputs=code_input, outputs=code_output)

    with gr.Tab("🛠️ Code Fixer (LLM)"):
        fixer_code_input = gr.Code(label="Paste Code")
        fixer_issues_input = gr.Textbox(label="Paste issues as JSON")
        fixer_btn = gr.Button("Fix Code")
        fixer_output = gr.Textbox(label="Explanation + Fixed Code", lines=20)
        fixer_btn.click(handle_code_fix, inputs=[fixer_code_input, fixer_issues_input], outputs=fixer_output)

    with gr.Tab("🔐 Encrypt/Decrypt Files"):
        enc_file_input = gr.File(label="Select File to Encrypt")
        enc_btn = gr.Button("Encrypt")
        enc_output = gr.JSON()
        enc_btn.click(handle_encryption, inputs=enc_file_input, outputs=enc_output)

        gr.Markdown("### 🔁 Decrypt Encrypted File:")
        dec_file_input = gr.File(label="Encrypted .enc File")
        dec_key_input = gr.File(label=".key File")
        dec_nonce_input = gr.File(label=".nonce File")
        dec_btn = gr.Button("Decrypt")
        dec_output = gr.JSON()
        dec_btn.click(handle_decryption, inputs=[dec_file_input, dec_key_input, dec_nonce_input], outputs=dec_output)

demo.launch()