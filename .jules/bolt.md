## 2025-05-15 - [Add LRU caching to AI recommendation engine]
**Learning:** LLM API calls are a significant performance bottleneck in the recommendation pipeline. Since fashion advice for specific garment/event combinations is often static, caching these results provides a massive performance boost (from ~1s to <0.1ms). Using primitive, hashable types for cache keys is essential when working with complex objects like Pydantic models.

**Action:** Always wrap expensive, repeatable AI logic with `functools.lru_cache` using primitive keys to maximize hits and minimize latency.
