"""
Main entry point for SecuraMind
- Launches the Gradio UI
- Or optionally allows command-line/test execution of agent tools
"""

import sys
from core.agent_engine import SecuraMindAgent
import os

# Optional: Run Gradio UI
def launch_ui():
    print("🔧 Launching Gradio UI...")
    os.system("python ui/gradio_ui.py")

# Optional: CLI test example (can be removed in production)
def run_test():
    agent = SecuraMindAgent()
    print("🔍 Supported tasks:", agent.get_supported_tasks())

    # Example 1: Scan File
    test_file = "/content/sample.txt"
    if os.path.exists(test_file):
        print("🗂️ File Scan Result:")
        print(agent.scan_file(test_file))

    # Example 2: URL Check
    print("🌐 URL Check:")
    print(agent.scan_url("http://example.com"))

    # Example 3: Code Review
    sample_code = '''
import os
password = "1234"
os.system("rm -rf /")
'''
    print("🧑‍💻 Code Review:")
    result = agent.review_code(sample_code)
    print(result)

    # Optional Fix
    if result["issue_count"] > 0:
        print("🛠️ Fixing Code:")
        print(agent.fix_code(sample_code, result["issues"]))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_test()
    else:
        launch_ui()