## 2025-03-05 - Hardcoded Secrets in Authentication Handshake
**Vulnerability:** Critical authentication secrets were hardcoded in multiple backend files (`main.py`, `DivineoBunker.py`), exposing the system to credential theft if the source code were compromised.
**Learning:** Hardcoding secrets often occurs during "rapid prototyping" phases and persists into production if not audited. Centralized environment variable management is essential for multi-component systems.
**Prevention:** Use `python-dotenv` and `os.getenv` for all sensitive keys. Implement mandatory pre-commit hooks or CI scans to detect plaintext secrets (e.g., `git-secrets`).
