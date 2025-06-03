# main.py
"""
Main entry point for SecuraMind
- Launches the Gradio UI
- Or optionally allows command-line/test execution of agent tools
"""

import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.agent_engine import SecuraMindAgent


# Optional: Run Gradio UI
def launch_ui():
    print("🔧 Launching Gradio UI...")
    os.system("python ui/gradio_ui.py")


# Optional: CLI test example
def run_test():
    agent = SecuraMindAgent()
    print("🔍 Supported tasks:", agent.get_supported_tasks())

    # Example 1: Scan File
    test_file = "sample.txt"
    if os.path.exists(test_file):
        print("🗂️ File Scan Result:")
        print(agent.scan_file(test_file))
    else:
        with open(test_file, "w") as f:
            f.write('eval("2+2")\npassword = "1234"\nos.system("rm -rf /")')
        print("📄 Sample file created for scanning.")
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

    # Example 4: Code Fixing
    if result["issue_count"] > 0:
        print("🛠️ Fixing Code:")
        fix_result = agent.fix_code(sample_code, result["issues"])
        print(fix_result)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_test()
    else:
        launch_ui()
