# Architecture and Data Flow

---

The architecture isolates plaintext data handling from the storage layer.

1. **User-Management Module:** Handles terminal I/O. It accepts the master password using a prompt`getpass`, generates or retrieves a cryptographic salt, and runs the Argon2id key derivation function to produce the Master Encryption Key (MEK).
2. **Encryption Module:** The cryptographic core. It receives the MEK and handles the AES-256-GCM encryption and decryption of the vault.
3. **Storage Layer:** Handles file read/write operations. It only interacts with the JSON containing the non-secret cryptographic parameters (salt, nonce) and the ciphertext part. It never processes plaintext credentials.

---

## Data flow

1. **Encryption**

   - User-Management Module: Accepts the user's master password from the CLI and derives the Master Encryption Key.
   - Encryption Module: Receives the MEK. It takes the plaintext credentials currently sitting in memory and encrypts them into a secure ciphertext part.
   - Storage Layer: Receives the ciphertext part and safe cryptographic parameters (like the salt and nonce) from the Encryption Module. It formats this into a JSON file and writes it to disk.
2. **Decryption**

- Storage Layer: Reads the JSON vault file from disk and passes the encrypted blob and parameters up to the Encryption Module.
- User-Management Module: Takes the user's inputted master password, processes it, and hands the regenerated MEK to the Encryption Module.
- Encryption Module: Combines the MEK and the encrypted part to unlock the vault. The plaintext credentials are held strictly in temporary memory for the user to access via the CLI.

---

![flow](/.images/1789583464193.png)
