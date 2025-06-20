# modal_env_test.py
import os
import modal

app = modal.App("env-check")

@app.function(secrets=[modal.Secret.from_name("securamind-api-keys")])
def check_env():
    print("🔍 MISTRAL_API_KEY:", os.getenv("MISTRAL_API_KEY"))

@app.local_entrypoint()
def main():
    check_env.remote()
