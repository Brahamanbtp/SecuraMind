"""
SecuraMind Agent Engine
- Routes inputs to the appropriate tools
- Provides a unified API for future multi-agent chaining or memory
"""

from agent.file_scanner import scan_file
from agent.url_checker import scan_url
from agent.log_analyzer import analyze_log
from agent.code_reviewer import review_code
from agent.fixer import fix_code
from agent.encryptor import encrypt_file, decrypt_file


class SecuraMindAgent:

    def scan_file(self, filepath: str) -> dict:
        return scan_file(filepath)

    def scan_url(self, url: str) -> dict:
        return scan_url(url)

    def analyze_logs(self, log_text: str) -> dict:
        return analyze_log(log_text)

    def review_code(self, code: str) -> dict:
        return review_code(code)

    def fix_code(self, code: str, issues: list) -> dict:
        return fix_code(code, issues)

    def encrypt_file(self, filepath: str) -> dict:
        return encrypt_file(filepath)

    def decrypt_file(self, enc_file: str, key_file: str, nonce_file: str) -> dict:
        return decrypt_file(enc_file, key_file, nonce_file)

    def get_supported_tasks(self) -> list:
        return [
            "scan_file", "scan_url", "analyze_logs",
            "review_code", "fix_code",
            "encrypt_file", "decrypt_file"
        ]