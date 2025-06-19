"""
Main entry point for SecuraMind
- Launches the Gradio UI
- Or optionally allows command-line/test execution of agent tools
"""

import os
import sys

# ✅ Ensure project root is on Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.agent_engine import SecuraMindAgent


def launch_ui():
    """
    Launch the Gradio-based UI.
    """
    print("🔧 Launching Gradio UI...")
    os.system("python ui/gradio_ui.py")


def run_test():
    """
    Run predefined tests on the agent tools.
    """
    agent = SecuraMindAgent()
    print("✅ SecuraMind Agent Test Started")
    print("🔍 Supported tasks:", agent.get_supported_tasks())

    # Test 1: File scan
    test_file = "sample.txt"
    if not os.path.exists(test_file):
        with open(test_file, "w") as f:
            f.write('eval("2+2")\npassword = "1234"\nos.system("rm -rf /")')
        print("📄 Sample file created for scanning.")
    print("🗂️ File Scan Result:")
    print(agent.scan_file(test_file))

    # Test 2: URL scan
    print("🌐 URL Check:")
    print(agent.scan_url("http://example.com"))

    # Test 3: Static code analysis
    sample_code = '''
import os
password = "1234"
os.system("rm -rf /")
'''
    print("🧑‍💻 Code Review:")
    result = agent.review_code(sample_code)
    print(result)

    # Test 4: Secure fix (Modal or fallback)
    if result.get("issue_count", 0) > 0:
        print("🛠️ Fixing Code:")
        fix_result = agent.fix_code(sample_code, result["issues"])
        print("✅ Fix Result:")
        print(fix_result)
    else:
        print("✅ No issues to fix.")


# ✅ Entry point with CLI flags
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            run_test()
        elif sys.argv[1] == "cloud":
            print("☁️ Launching Modal Cloud Fixer...")
            os.system("modal run -m agent.fixer")
        else:
            print("⚠️ Unknown option. Launching Gradio UI instead...")
            launch_ui()
    else:
        launch_ui()
