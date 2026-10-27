"""pman: local password manager (CLI / user-management module)."""
import argparse
import getpass
import json
import sys
import time

import pyperclip
from cryptography.exceptions import InvalidTag

import crypto
import storage

MIN_MASTER_LEN = 12
CLIPBOARD_SECONDS = 15


def save_vault(key: bytes, salt: bytes, params: dict, entries: dict) -> None:
    nonce, ciphertext = crypto.encrypt(key, json.dumps(entries).encode("utf-8"))
    storage.save(salt, params, nonce, ciphertext)


def unlock():
    if not storage.exists():
        sys.exit("No vault found. Run: python pman.py init")
    salt, params, nonce, ciphertext = storage.load()
    key = crypto.derive_key(getpass.getpass("Master password: "), salt, params)
    try:
        entries = json.loads(crypto.decrypt(key, nonce, ciphertext))
    except InvalidTag:
        sys.exit("Access denied: wrong master password or corrupted vault.")
    return key, salt, params, entries


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


def cmd_add(args):
    key, salt, params, entries = unlock()
    if args.service in entries:
        sys.exit(f"'{args.service}' already exists. Remove it first.")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    if not password:
        sys.exit("Password cannot be empty.")
    entries[args.service] = {"username": username, "password": password}
    save_vault(key, salt, params, entries)
    print(f"Saved '{args.service}'.")


def cmd_list(args):
    _, _, _, entries = unlock()
    if not entries:
        print("Vault is empty.")
        return
    print(f"{'SERVICE':<20} USERNAME")
    for service in sorted(entries):
        print(f"{service:<20} {entries[service]['username']}")


def cmd_get(args):
    _, _, _, entries = unlock()
    entry = entries.get(args.service)
    if entry is None:
        sys.exit(f"No entry named '{args.service}'.")
    print(f"Service:  {args.service}")
    print(f"Username: {entry['username']}")
    print("Password: ********")
    try:
        pyperclip.copy(entry["password"])
    except pyperclip.PyperclipException:
        sys.exit("Clipboard unavailable.")
    print(f"Password copied to clipboard. Clearing in {CLIPBOARD_SECONDS}s")
    try:
        time.sleep(CLIPBOARD_SECONDS)
    except KeyboardInterrupt:
        pass
    finally:
        pyperclip.copy("")
    print("Clipboard cleared.")


def cmd_rm(args):
    key, salt, params, entries = unlock()
    if args.service not in entries:
        sys.exit(f"No entry named '{args.service}'.")
    if input(f"Type '{args.service}' to confirm deletion: ") != args.service:
        sys.exit("Cancelled.")
    del entries[args.service]
    save_vault(key, salt, params, entries)
    print(f"Removed '{args.service}'.")


def main():
    parser = argparse.ArgumentParser(prog="pman", description="Local password manager")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="create a new vault").set_defaults(func=cmd_init)
    p = sub.add_parser("add", help="add a credential")
    p.add_argument("service")
    p.set_defaults(func=cmd_add)
    sub.add_parser("list", help="list services (no passwords)").set_defaults(func=cmd_list)
    p = sub.add_parser("get", help="copy a password to the clipboard")
    p.add_argument("service")
    p.set_defaults(func=cmd_get)
    p = sub.add_parser("rm", help="delete a credential")
    p.add_argument("service")
    p.set_defaults(func=cmd_rm)

    args = parser.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        sys.exit("\nAborted.")


if __name__ == "__main__":
    main()
