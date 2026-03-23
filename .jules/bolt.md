## 2025-05-15 - [LRU Cache for AI Recommendations]
**Learning:** LLM API calls are a major bottleneck (several seconds per request). Implementing `functools.lru_cache` provides massive performance gains for identical requests. However, Pydantic models and dictionaries are not hashable and cannot be used directly as cache keys.
**Action:** When implementing `lru_cache` for functions involving complex objects, use an internal helper function that accepts primitive, hashable types (strings, ints) to form the cache key.
