# Sentinel Journal

This journal tracks critical security learnings for the TryOnYou project.

## 2025-03-03 - Hardcoded Secrets and Insecure Error Handling
**Vulnerability:** Hardcoded `SECRET_KEY` in `backend/main.py` and `backend/DivineoBunker.py`. Inconsistent error handling when the AI engine failed.
**Learning:** Legacy development often leaves test credentials in code for simplicity, which can leak into production.
**Prevention:** Always load secrets from environment variables and implement centralized, generic error responses that don't leak internal states.
