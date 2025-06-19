# modal_main.py

import modal
from agent.fixer import fix_code_modal

# Optional: mock data for testing
test_code = '''
import os
password = "1234"
os.system("rm -rf /")
'''
test_issues = [
    {"line_number": 2, "line": 'password = "1234"', "issue": "Hardcoded password"},
    {"line_number": 3, "line": 'os.system("rm -rf /")', "issue": "Use of os.system()"},
]

@modal.local_entrypoint()
def main():
    result = fix_code_modal.call(test_code, test_issues)
    print("✅ Cloud Fix Result:\n", result)
