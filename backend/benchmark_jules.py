import time
import asyncio
from unittest.mock import MagicMock
import backend.jules_engine as jules_engine
from backend.models import UserScan, SHOPIFY_INVENTORY

async def benchmark_cache():
    print("--- ⚡ BOLT PERFORMANCE BENCHMARK: JULES AI CACHE ---")

    # Mock the LLM call to simulate latency
    original_model = jules_engine.model
    jules_engine.model = MagicMock()

    def mock_generate_content(prompt):
        time.sleep(1.5) # Simulate 1.5s LLM latency
        mock_response = MagicMock()
        mock_response.text = "This is a cached recommendation."
        return mock_response

    jules_engine.model.generate_content = mock_generate_content

    test_scan = UserScan(
        user_id="BENCHMARK_USER",
        token="SIMULATED",
        waist=75.0,
        event_type="Gala"
    )
    garment = SHOPIFY_INVENTORY["BALMAIN_SS26_SLIM"]

    print(f"Targeting: {garment['name']} for {test_scan.event_type}")

    # 1. First Call (Cache Miss)
    print("\n[1] Executing First Call (Cache Miss)...")
    start_miss = time.perf_counter()
    jules_engine.get_jules_advice(test_scan, garment)
    end_miss = time.perf_counter()
    miss_duration = end_miss - start_miss
    print(f"Miss Duration: {miss_duration:.4f}s")

    # 2. Second Call (Cache Hit)
    print("\n[2] Executing Second Call (Cache Hit)...")
    start_hit = time.perf_counter()
    jules_engine.get_jules_advice(test_scan, garment)
    end_hit = time.perf_counter()
    hit_duration = end_hit - start_hit
    print(f"Hit Duration: {hit_duration:.6f}s")

    # 3. Results
    improvement = (miss_duration - hit_duration) / miss_duration * 100
    print(f"\n--- RESULTS ---")
    print(f"Latency Reduction: {improvement:.2f}%")
    print(f"Speedup: {miss_duration / hit_duration:.2f}x")

    # Restore original model
    jules_engine.model = original_model

if __name__ == "__main__":
    asyncio.run(benchmark_cache())
