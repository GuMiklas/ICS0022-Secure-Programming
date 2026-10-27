# Password Manager

## Description

A local, CLI based password manager written in Python. It securely derives encryption keys from a master password using Argon2id and encrypts all stored credentials using AES-256-GCM. The vault is stored locally as a JSON file.

## Commands

* `init` - Initialize a new secure vault and set the master password.
* `add <service>` - Add a new credential to the vault.
* `get <service>` - Show the username and copy the password to the clipboard (cleared after 15 s).
* `list` - Show all saved services (without revealing passwords).
* `rm <service>` - Delete a credential from the vault.

## Build and Run Instructions

### Prerequisites

* Python 3.10+
* Virtual environment

### Setup

1. Clone the repository:

   ```
   git clone https://github.com/GuMiklas/ICS0022-Secure-Programming.git
   ```
2. Navigate to the directory:

   ```
   cd ICS0022-Secure-Programming
   ```
3. Create a virtual environment:

   ```
   python -m venv venv
   ```
4. Activate the environment:

   * Windows:
     ```
     venv\Scripts\activate
     ```

     (If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.)
   * Linux:
     ```
     source venv/bin/activate
     ```
5. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

   (Installs `cryptography`, `argon2-cffi` and `pyperclip`)

   On Linux, the clipboard also needs a system tool: `sudo apt install xclip` (or `wl-clipboard` on Wayland).

### Usage

Run the application via:

```
python pman.py [command]
```



The vault is stored in `vault.json` in the current directory. Set the `PMAN_VAULT` environment variable to use a different path.

## Notes

* **Key derivation:** Argon2id (time cost 3, 64 MiB memory, parallelism 4, 16-byte random salt) turns the master password into a 256-bit key.
* **Encryption at rest:** the whole credential list is encrypted with AES-256-GCM and a fresh 12-byte nonce on every save. The vault file only contains the salt, the KDF parameters, the nonce and the ciphertext.
* **Master password check:** no password hash is stored.
* **No cleartext output:** passwords are typed with `getpass`, `list` never shows them, and `get` only copies them to the clipboard, which is cleared after 15 seconds.
* **Safe writes:** the vault is written to a temporary file and then atomically replaced, so a crash cannot leave a half-written vault.
* **Known limitations:** Python cannot reliably wipe secrets from memory, and other local programs can read the clipboard while the password is on it.
