# Checkpoint 2 - Progress

The core password manager is implemented as a Python CLI (`pman.py`) following the architecture from Checkpoint 1: a user-management/CLI module (`pman.py`), an encryption module (`crypto.py`) and a storage layer (`storage.py`). Build and run instructions are in the main [README](../../README.md).

## Requirements

| Requirement                                   | Explanation                                                                                                                                                  |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Basic vault storage working                   | `storage.py`: `save()` / `load()` write and read `vault.json`                                                                                        |
| Credentials encrypted at rest                 | `crypto.py`: Argon2id key derivation + AES-256-GCM; `pman.py`: `save_vault()` encrypts the whole credential list before it reaches storage             |
| Master password authentication                | `pman.py`: `unlock()` derives the key and decrypts; a wrong password fails the GCM check and the program exits with "Access denied"                      |
| Interface never prints passwords in cleartext | `getpass` for all password input; `list` shows only service and username; `get` masks the password and copies it to the clipboard (cleared after 15 s) |

The master password is never stored, not even as a hash. On unlock, Argon2id derives the key from the entered password and the stored salt, and that key is used to decrypt the vault. If the password is wrong, the AES-GCM authentication tag does not verify and the vault stays locked.

## Known Limitations

* Python strings cannot be reliably wiped from memory, so secrets may stay in RAM.
* The clipboard can be read by other local programs during the 15-second window.
