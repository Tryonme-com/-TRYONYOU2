# Bolt's Performance Journal

## 2025-05-22 - [Optimizing LLM response times]
**Learning:** LLM API calls are a significant source of latency and cost. For a virtual try-on application, users often try the same garments with similar profiles. Caching these responses based on key inputs can drastically improve perceived performance for repeat interactions.
**Action:** Implement an in-memory cache for `get_jules_advice` to prevent redundant API calls.

## 2025-05-22 - [Reducing Browser Overhead with IntersectionObserver]
**Learning:** Observing elements with `IntersectionObserver` that only need to trigger an animation once adds unnecessary overhead as the user continues to scroll. Unobserving elements after they've been revealed frees up browser resources.
**Action:** Call `observer.unobserve(entry.target)` once the section has been revealed in `js/main.js`.
