"""
Encryptor Tool for SecuraMind
- AES-GCM file encryption and decryption using secure random keys
- Output: .enc file + key + nonce (base64 encoded)
"""

import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_key():
    return AESGCM.generate_key(bit_length=256)

def encrypt_file(input_path, output_path=None):
    if not os.path.isfile(input_path):
        return {"error": "File does not exist."}

    key = generate_key()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)

    with open(input_path, "rb") as f:
        data = f.read()

    encrypted = aesgcm.encrypt(nonce, data, None)

    if not output_path:
        output_path = input_path + ".enc"

    with open(output_path, "wb") as f:
        f.write(encrypted)

    base = os.path.splitext(output_path)[0]
    with open(base + ".key", "wb") as f:
        f.write(base64.b64encode(key))
    with open(base + ".nonce", "wb") as f:
        f.write(base64.b64encode(nonce))

    return {
        "message": "Encryption successful",
        "encrypted_file": output_path,
        "key_file": base + ".key",
        "nonce_file": base + ".nonce"
    }

def decrypt_file(encrypted_path, key_path, nonce_path, output_path=None):
    try:
        with open(encrypted_path, "rb") as f:
            ciphertext = f.read()
        with open(key_path, "rb") as f:
            key = base64.b64decode(f.read())
        with open(nonce_path, "rb") as f:
            nonce = base64.b64decode(f.read())

        aesgcm = AESGCM(key)
        decrypted = aesgcm.decrypt(nonce, ciphertext, None)

        if not output_path:
            output_path = encrypted_path.replace(".enc", ".dec")

        with open(output_path, "wb") as f:
            f.write(decrypted)

        return {
            "message": "Decryption successful",
            "output_file": output_path
        }

    except Exception as e:
        return {"error": f"Decryption failed: {str(e)}"}