## 2025-05-15 - [Input Validation and CORS Hardening]
**Vulnerability:** Lack of input validation on UserScan and permissive CORS settings (allow_credentials=True with allow_origins=["*"]).
**Learning:** Pydantic models without explicit constraints can process unrealistic or malicious data, leading to downstream issues (e.g., potential long-input attacks on AI). Permissive CORS can lead to security risks if credentials are handled.
**Prevention:** Use Pydantic's `Field` to define constraints for all user-provided data and ensure CORS is configured with the principle of least privilege.
