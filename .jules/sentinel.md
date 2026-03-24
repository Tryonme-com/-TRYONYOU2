## 2025-05-15 - [security improvement] Remove Hardcoded Secrets
**Vulnerability:** Hardcoded `SECRET_KEY` for HMAC authentication in `backend/main.py` and `backend/DivineoBunker.py`.
**Learning:** Hardcoding secrets simplifies development but creates a critical security risk as anyone with access to the source code can forge authentication tokens.
**Prevention:** Always use environment variables for sensitive configuration like API keys, secrets, and passwords. Use a `.env.example` file to document required environment variables without exposing their actual values.
