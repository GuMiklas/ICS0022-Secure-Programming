# Password Manager

## Description

A local, CLI based password manager written in Python. It securely derives encryption keys from a master password using Argon2id and encrypts all stored credentials using AES-256-GCM. The vault is stored locally as a JSON file.

## Planned Commands

* `init` - Initialize a new secure vault and set the master password.
* `add ` - Add a new credential to the vault.
* `get ` - Retrieve and decrypt a credential.
* `list` - Show all saved services (without revealing passwords).
* `rm ` - Delete a credential from the vault.

## Build and Run Instructions

### Prerequisites

* Python 3.10+
* Virtual environment

### Setup

1. Clone the repository:

   ```
   git clone
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
   * Linux:
     ```
     source venv/bin/activate
     ```
5. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

   (Requires `cryptography` and `argon2-cffi`)

### Usage

Run the application via:

```
python pman.py [command]
```
