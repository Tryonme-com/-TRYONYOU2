## 2024-03-17 - LLM Latency & Caching
**Learning:** LLM API calls (Gemini 1.5 Flash) introduce significant latency (avg 1.5s) which can degrade UX for repetitive requests. In-memory caching with a composite key (garment, event, body shape, fit preference) can reduce subsequent response times to near-zero.
**Action:** Always implement a size-limited cache for expensive AI-generated content when the input space has high overlap. Use `async` calls to avoid blocking the backend event loop during API I/O.
