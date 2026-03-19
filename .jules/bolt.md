## 2026-03-19 - [LLM Response Caching with Metric Normalization]
**Learning:** LLM API calls are a major bottleneck for response time. Implementing an LRU cache significantly reduces latency for repeat requests. Normalizing input metrics (e.g., rounding float values for height and weight) increases the cache hit rate by treating slightly different sensor readings as identical profiles.
**Action:** Always use bounded caches (like `functools.lru_cache`) for backend services to prevent memory leaks, and consider if input normalization can improve cache efficiency.
