"""
SecuraMind Agent Engine
- Central controller that routes inputs to security analysis tools
- Supports optional Modal-based LLM fixer
- Provides a unified API for chaining, memory, and orchestration
"""

# Standard Library
import importlib

# Agent tool imports (relative to project root)
from agent.file_scanner import scan_file
from agent.url_checker import scan_url
from agent.log_analyzer import analyze_log
from agent.code_reviewer import review_code
from agent.encryptor import encrypt_file, decrypt_file

# Optional Modal-based fixer support
try:
    from agent.fixer import fix_code_modal  # Modal cloud-based function
    import modal
    IS_MODAL_FUNCTION = True
except ImportError:
    try:
        from agent.fixer import fix_code as fix_code_modal  # Local fallback
        IS_MODAL_FUNCTION = False
    except ImportError:
        raise ImportError("❌ Neither Modal-based nor local fixer could be loaded. Check module paths.")


class SecuraMindAgent:
    """
    Unified interface for all supported tools in the SecuraMind suite.
    """

    def scan_file(self, filepath: str) -> dict:
        """Scan a file for threats or suspicious content."""
        return scan_file(filepath)

    def scan_url(self, url: str) -> dict:
        """Check a URL against security databases or heuristic rules."""
        return scan_url(url)

    def analyze_logs(self, log_text: str) -> dict:
        """Analyze logs for patterns and anomalies."""
        return analyze_log(log_text)

    def review_code(self, code: str) -> dict:
        """Perform static code analysis for OWASP and common risks."""
        return review_code(code)

    def fix_code(self, code: str, issues: list) -> dict:
        """Use an LLM (Modal or Local) to fix code based on detected issues."""
        if IS_MODAL_FUNCTION:
            print("🛰️ Fixing with Modal cloud function...")

            # Determine environment: modal run or external script
            if modal.is_local():
                return fix_code_modal.call(code, issues)
            else:
                return fix_code_modal.spawn(code, issues).get()
        else:
            print("🛠️ Fixing with local fallback...")
            return fix_code_modal(code, issues)

    def encrypt_file(self, filepath: str) -> dict:
        """Encrypt a file using symmetric key cryptography."""
        return encrypt_file(filepath)

    def decrypt_file(self, enc_file: str, key_file: str, nonce_file: str) -> dict:
        """Decrypt a previously encrypted file using stored key/nonce."""
        return decrypt_file(enc_file, key_file, nonce_file)

    def get_supported_tasks(self) -> list:
        """Return a list of all supported agent tools/tasks."""
        return [
            "scan_file",
            "scan_url",
            "analyze_logs",
            "review_code",
            "fix_code",
            "encrypt_file",
            "decrypt_file"
        ]
