## 2025-05-15 - [API Security Hardening]
**Vulnerability:** Overly permissive CORS and missing input validation.
**Learning:** Wildcard CORS with credentials enabled is a significant security risk. Lack of input validation on physical metrics can lead to unexpected API behavior.
**Prevention:** Always restrict CORS origins to trusted domains and use Pydantic `Field` for strict input validation.
