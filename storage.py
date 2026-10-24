"""Storage layer: reads/writes the vault file. Only handles ciphertext and public parameters."""
import base64
import json
import os

VAULT_PATH = os.environ.get("PMAN_VAULT", "vault.json")


def _b64encode(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


def _b64decode(s: str) -> bytes:
    return base64.b64decode(s)


def exists(path: str = VAULT_PATH) -> bool:
    return os.path.exists(path)


def save(salt: bytes, kdf_params: dict, nonce: bytes, ciphertext: bytes, path: str = VAULT_PATH) -> None:
    data = {
        "version": 1,
        "kdf": {"name": "argon2id", "salt": _b64encode(salt), **kdf_params},
        "nonce": _b64encode(nonce),
        "ciphertext": _b64encode(ciphertext),
    }
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)
    try:
        os.chmod(path, 0o600)  # owner-only on POSIX; limited effect on Windows
    except OSError:
        pass


def load(path: str = VAULT_PATH) -> tuple[bytes, dict, bytes, bytes]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    kdf = data["kdf"]
    params = {k: kdf[k] for k in ("time_cost", "memory_cost", "parallelism")}
    return _b64decode(kdf["salt"]), params, _b64decode(data["nonce"]), _b64decode(data["ciphertext"])
