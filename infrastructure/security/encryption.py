from cryptography.fernet import Fernet
import os

KEY_FILE = "clave.key"


def get_key():
    """
    Retrieve encryption key or generate it if it doesn't exist.
    """
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key


def encrypt(text: str) -> bytes:
    """
    Encrypt plain text using Fernet symmetric encryption.
    """
    fernet = Fernet(get_key())
    return fernet.encrypt(text.encode())


def decrypt(encrypted_text: bytes) -> str:
    """
    Decrypt encrypted text and return plain string.
    """
    fernet = Fernet(get_key())
    return fernet.decrypt(encrypted_text).decode()
