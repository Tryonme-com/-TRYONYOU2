# 🛡️ Sentinel Security Journal

## 2026-03-19 - [API Hardening: CORS and Input Validation]
**Vulnerability:** Overly permissive CORS policy and lack of strict input validation on biometric data endpoints.
**Learning:** The initial implementation allowed all methods and credentials in CORS, which could be exploited for CSRF or other cross-origin attacks if expanded. Lack of input validation on `height` and `weight` could lead to unrealistic data processing or potentially be used as a vector for prompt injection if these values were directly embedded in LLM prompts without sanitization.
**Prevention:** Always implement the Principle of Least Privilege for CORS. Use Pydantic's `Field` constraints to enforce realistic bounds on all numeric and string inputs to provide defense-in-depth and improve system reliability.
