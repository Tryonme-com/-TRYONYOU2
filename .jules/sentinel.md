## 2025-05-15 - [Securing HMAC Secrets and CORS]
**Vulnerability:** Hardcoded HMAC secret key and overly permissive CORS policy.
**Learning:** Hardcoding production-level secrets in multiple files (`main.py` and `DivineoBunker.py`) creates a high risk of exposure. Permissive CORS (`"*"`) is acceptable for rapid prototyping but should be configurable for deployment to prevent unauthorized cross-origin access.
**Prevention:** Use environment variables (via `os.getenv` and `python-dotenv`) for all sensitive credentials. Implement configurable CORS origins through environment variables, defaulting to specific origins in production.
