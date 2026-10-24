"""Encryption module: Argon2id key derivation and AES-256-GCM encryption."""
import os

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Argon2id parameters (OWASP baseline). Stored in the vault so they can be raised later.
KDF_PARAMS = {"time_cost": 3, "memory_cost": 65536, "parallelism": 4}
SALT_LEN = 16
NONCE_LEN = 12   # 96-bit nonce
KEY_LEN = 32     # 256-bit key
AAD = b"pman-vault-v1"


def new_salt() -> bytes:
    return os.urandom(SALT_LEN)


def derive_key(master_password: str, salt: bytes, params: dict = KDF_PARAMS) -> bytes:
    return hash_secret_raw(
        secret=master_password.encode("utf-8"),
        salt=salt,
        time_cost=params["time_cost"],
        memory_cost=params["memory_cost"],
        parallelism=params["parallelism"],
        hash_len=KEY_LEN,
        type=Type.ID,
    )


def encrypt(key: bytes, plaintext: bytes) -> tuple[bytes, bytes]:
    nonce = os.urandom(NONCE_LEN)
    return nonce, AESGCM(key).encrypt(nonce, plaintext, AAD)


def decrypt(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    return AESGCM(key).decrypt(nonce, ciphertext, AAD)
