"""pman: local password manager (CLI / user-management module)."""
import argparse
import getpass
import json
import sys

import crypto
import storage

MIN_MASTER_LEN = 12


def save_vault(key: bytes, salt: bytes, params: dict, entries: dict) -> None:
    nonce, ciphertext = crypto.encrypt(key, json.dumps(entries).encode("utf-8"))
    storage.save(salt, params, nonce, ciphertext)


def cmd_init(args):
    if storage.exists():
        sys.exit("A vault already exists.")
    password = getpass.getpass("New master password: ")
    if len(password) < MIN_MASTER_LEN:
        sys.exit(f"Master password must be at least {MIN_MASTER_LEN} characters.")
    if password != getpass.getpass("Confirm master password: "):
        sys.exit("Passwords do not match.")
    salt = crypto.new_salt()
    save_vault(crypto.derive_key(password, salt), salt, crypto.KDF_PARAMS, {})
    print("Vault created.")


def main():
    parser = argparse.ArgumentParser(prog="pman", description="Local password manager")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="create a new vault").set_defaults(func=cmd_init)

    args = parser.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        sys.exit("\nAborted.")


if __name__ == "__main__":
    main()
