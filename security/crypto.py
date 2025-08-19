import os
import hashlib
from cryptography.fernet import Fernet

_KEY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "secret.key")

def _get_or_create_key() -> bytes:
    if not os.path.exists(_KEY_PATH):
        key = Fernet.generate_key()
        with open(_KEY_PATH, "wb") as f:
            f.write(key)
        return key
    with open(_KEY_PATH, "rb") as f:
        return f.read()

_fernet = Fernet(_get_or_create_key())


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def encrypt_str(text: str) -> bytes:
    return _fernet.encrypt(text.encode("utf-8"))


def decrypt_str(token: bytes) -> str:
    return _fernet.decrypt(token).decode("utf-8")

