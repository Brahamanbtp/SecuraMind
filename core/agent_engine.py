"""
SecuraMind Agent Engine
- Central controller that routes inputs to security analysis tools
- Supports optional Modal-based LLM fixer
- Provides a unified API for chaining, memory, and orchestration
"""

# Standard Library
import importlib

# Agent tool imports
from agent.file_scanner import scan_file
from agent.url_checker import scan_url
from agent.log_analyzer import analyze_log
from agent.code_reviewer import review_code
from agent.encryptor import encrypt_file, decrypt_file

# Optional Modal-based fixer support
try:
    from agent.fixer import fix_code_modal, IS_MODAL_FUNCTION
    import modal
except ImportError:
    IS_MODAL_FUNCTION = False
    fix_code_modal = None
    print("⚠️ Modal not available. Code fixing via cloud is disabled.")


class SecuraMindAgent:
    """
    Unified interface for all supported tools in the SecuraMind suite.
    """

    def scan_file(self, filepath: str) -> dict:
        return scan_file(filepath)

    def scan_url(self, url: str) -> dict:
        return scan_url(url)

    def analyze_logs(self, log_text: str) -> dict:
        return analyze_log(log_text)

    def review_code(self, code: str) -> dict:
        return review_code(code)

    def fix_code(self, code: str, issues: list) -> dict:
        if not fix_code_modal:
            return {"error": "❌ No fixer implementation available."}

        if IS_MODAL_FUNCTION:
            print("🛰️ Fixing with Modal cloud function...")
            try:
                if modal.is_local():  # Inside modal run
                    return fix_code_modal.local(code, issues)
                else:  # CLI or Gradio context
                    return fix_code_modal.remote(code, issues)
            except Exception as e:
                return {"error": f"❌ Modal function call failed: {str(e)}"}
        else:
            print("🛠️ Fixing with local fallback...")
            try:
                return fix_code_modal(code, issues)
            except Exception as e:
                return {"error": f"❌ Local fixer failed: {str(e)}"}

    def encrypt_file(self, filepath: str) -> dict:
        return encrypt_file(filepath)

    def decrypt_file(self, enc_file: str, key_file: str, nonce_file: str) -> dict:
        return decrypt_file(enc_file, key_file, nonce_file)

    def get_supported_tasks(self) -> list:
        return [
            "scan_file",
            "scan_url",
            "analyze_logs",
            "review_code",
            "fix_code",
            "encrypt_file",
            "decrypt_file"
        ]
