# Bolt's Performance Journal

## 2024-05-15 - [LRU Caching for AI Recommendations]
**Learning:** Redundant LLM calls to Gemini are a major bottleneck (~2-5s latency). Standardizing input data (event type, garment attributes) allows for efficient caching with `functools.lru_cache`, which reduces repeated request latency to <1ms.
**Action:** Use primitive types for cache keys and ensure data consistency before calling the AI engine.
