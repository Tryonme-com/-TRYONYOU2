# Sentinel Security Journal

## 2025-05-15 - [Hardcoded Secrets and Insecure CORS]
**Vulnerability:** Hardcoded HMAC secret key in backend and unrestricted CORS origins.
**Learning:** Initial prototype code often includes hardcoded secrets for convenience, which must be externalized before deployment. Insecure CORS (*) allows any site to make requests to the API, which can be risky if authentication is weak or if sensitive data is involved.
**Prevention:** Use environment variables for all secrets and specific origin lists for CORS from the start. Use a `.env.example` to document requirements.

## 2025-05-15 - [Hardcoded Password in Frontend]
**Vulnerability:** A staff password was hardcoded in the frontend JavaScript, making it easily discoverable by anyone inspecting the code.
**Learning:** Frontend authentication checks are only for UI guidance and should always be backed by a secure backend verification.
**Prevention:** Always verify sensitive credentials on the backend using constant-time comparison (like `hmac.compare_digest`) and keep passwords in environment variables.
