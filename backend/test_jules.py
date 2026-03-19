import sys
import os
import asyncio
import json
import time
from unittest.mock import MagicMock

# Ensure we can import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock the genai model before importing modules that use it
import google.generativeai as genai
genai.configure = MagicMock()
mock_model = MagicMock()
genai.GenerativeModel = MagicMock(return_value=mock_model)

# Set a mock response with simulated latency
def mocked_generate_content(prompt):
    time.sleep(1.5)
    mock_response = MagicMock()
    mock_response.text = "Mocked Jules Advice: This garment is elegant and comfortable."
    return mock_response

mock_model.generate_content.side_effect = mocked_generate_content

from main import recommend_garment
from models import UserScan

async def run_diagnostic():
    print("--- 🧪 DIVINEO AI: JULES ENGINE DIAGNOSTIC ---")

    # Simulate a user scan for a luxury event
    test_scan = UserScan(
        height=175.4, # Should be rounded to 175
        weight=68.2, # Should be rounded to 68
        event_type="Galeries Lafayette Opening Gala"
    )

    print(f"Testing Scan: {test_scan.event_type}...")

    # Execute the recommendation logic multiple times to test caching
    for i in range(3):
        start_time = time.time()
        try:
            print(f"\nRequest {i+1}:")
            if i == 2:
                # Slightly different metrics that round to the same value
                test_scan.height = 174.6 # Also rounds to 175
                print("Testing with slightly different metrics (rounding to same value)...")

            result = await recommend_garment(test_scan)

            # handle JSONResponse from main.py
            if hasattr(result, 'body'):
                data = json.loads(result.body.decode())
            else:
                data = result

            duration = time.time() - start_time
            print(f"Time taken: {duration:.4f} seconds")

            if data.get('status') == 'error':
                 print(f"Error from backend: {data.get('message')}")
                 continue

            print(f"Garment Selected: {data['garment_name']}")
            print("--- JULES STYLE ADVICE ---")
            # print(data['recommendation'])

            # Final Validation
            advice = data['recommendation'].lower()
            forbidden = ["kg", "cm", "lbs", "size", "tall", "weight", "height"]

            if any(word in advice for word in forbidden):
                print("\n[!] WARNING: AI mentioned forbidden metrics.")
            else:
                print("\n[SUCCESS]: Jules followed the privacy and luxury protocol.")

        except Exception as e:
            print(f"\n[X] ERROR: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_diagnostic())
