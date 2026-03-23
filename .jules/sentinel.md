# Sentinel Security Journal

## 2025-05-15 - [Hardcoded Secrets and Insecure CORS]
**Vulnerability:** Hardcoded HMAC secret key in backend and unrestricted CORS origins.
**Learning:** Initial prototype code often includes hardcoded secrets for convenience, which must be externalized before deployment. Insecure CORS (*) allows any site to make requests to the API, which can be risky if authentication is weak or if sensitive data is involved.
**Prevention:** Use environment variables for all secrets and specific origin lists for CORS from the start. Use a `.env.example` to document requirements.
