## 2025-02-27 - [AI Response Caching]
**Learning:** LLM requests for styling advice introduce a consistent 1.5s+ latency. Since the input technical context (drape, elasticity) for a specific garment and event type is static, these responses are highly cacheable.
**Action:** Implement `functools.lru_cache` in the AI engine. Use an internal helper with primitive, hashable types as the cache key to maximize hits across different instance objects with identical data.

## 2025-02-27 - [Environment Hygiene]
**Learning:** Automatic lockfile generation (e.g., `pnpm install`) can introduce massive, out-of-scope diffs.
**Action:** Always verify the proposed file list before submission and ensure the `.gitignore` covers runtime-generated artifacts like `__pycache__` to prevent bloating the PR.

## 2025-05-22 - [FastAPI Event Loop Blocking]
**Learning:** Using `async def` for FastAPI route handlers that perform synchronous blocking I/O (like LLM calls via standard SDKs or HMAC calculations) blocks the main event loop, causing concurrent requests to be processed sequentially.
**Action:** Use standard `def` for route handlers that call synchronous blocking libraries. This allows FastAPI to run them in an external thread pool, enabling true concurrency and significantly reducing total latency for multiple users (observed ~54% reduction).
