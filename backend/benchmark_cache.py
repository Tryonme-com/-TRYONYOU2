import time
from unittest.mock import MagicMock
import jules_engine

def benchmark():
    print("--- ⚡ BOLT CACHE BENCHMARK (MOCKED LLM) ---")

    # Mock the LLM call to simulate a real, slow API response
    original_model = jules_engine.model
    jules_engine.model = MagicMock()

    def slow_generate_content(prompt):
        time.sleep(1.0) # Simulate 1s network latency
        mock_response = MagicMock()
        mock_response.text = f"Mocked advice for: {prompt[:50]}..."
        return mock_response

    jules_engine.model.generate_content.side_effect = slow_generate_content

    # Clear cache for a clean run
    jules_engine._get_cached_advice.cache_clear()

    test_args = ("Gala", "Balmain Slim-Fit Jeans", "Architectural and structured", "Minimal with memory retention")

    print(f"Executing first call (uncached)...")
    start_time = time.time()
    advice1 = jules_engine._get_cached_advice(*test_args)
    end_time = time.time()
    uncached_duration = end_time - start_time
    print(f"Uncached duration: {uncached_duration:.4f} seconds")

    print(f"\nExecuting second call (cached)...")
    start_time = time.time()
    advice2 = jules_engine._get_cached_advice(*test_args)
    end_time = time.time()
    cached_duration = end_time - start_time
    print(f"Cached duration: {cached_duration:.4f} seconds")

    # Restore original model
    jules_engine.model = original_model

    if advice1 == advice2:
        print("\n[SUCCESS] Cache returned identical result.")
        speedup = uncached_duration / cached_duration if cached_duration > 0 else float('inf')
        print(f"Performance Gain: {speedup:.1f}x faster")
    else:
        print("\n[ERROR] Cache mismatch!")

if __name__ == "__main__":
    benchmark()
