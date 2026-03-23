import time
import sys
import os
from unittest.mock import MagicMock

# Ensure we can import from the backend directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import jules_engine
from models import UserScan, SHOPIFY_INVENTORY

def benchmark():
    print("--- ⚡ JULES ENGINE PERFORMANCE BENCHMARK ---")

    # Mock the generative model to avoid real API calls and simulate latency
    original_model = jules_engine.model
    mock_model = MagicMock()

    def mock_generate_content(prompt):
        time.sleep(0.5) # Simulate 500ms LLM latency
        mock_response = MagicMock()
        mock_response.text = "Mocked Luxury Advice: Elegant and Fluid."
        return mock_response

    mock_model.generate_content.side_effect = mock_generate_content
    jules_engine.model = mock_model

    # Prepare test data
    user_data = UserScan(
        user_id="test_user",
        token="test_token",
        waist=70.0,
        event_type="Gala"
    )

    # Ensure garment has required keys (temporarily for this test if not fixed yet)
    garment = SHOPIFY_INVENTORY["BALMAIN_SS26_SLIM"].copy()
    if 'drape' not in garment:
        garment['drape'] = "Architectural"
    if 'elasticity' not in garment:
        garment['elasticity'] = "High-Recovery"

    print("\n1. Initial call (Cold Cache):")
    start = time.perf_counter()
    advice1 = jules_engine.get_jules_advice(user_data, garment)
    end = time.perf_counter()
    print(f"Time: {(end - start) * 1000:.2f}ms")

    print("\n2. Second call with same data (Should be cached if implemented):")
    start = time.perf_counter()
    advice2 = jules_engine.get_jules_advice(user_data, garment)
    end = time.perf_counter()
    print(f"Time: {(end - start) * 1000:.2f}ms")

    # Restore original model
    jules_engine.model = original_model

    if advice1 == advice2:
        print("\n[SUCCESS] Responses match.")
    else:
        print("\n[ERROR] Responses do not match.")

if __name__ == "__main__":
    benchmark()
