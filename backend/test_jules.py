import sys
import os
import asyncio
from unittest.mock import MagicMock

# Ensure we can import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock model before importing get_jules_advice
import google.generativeai as genai
genai.GenerativeModel = MagicMock()

import jules_engine
from main import recommend_garment
from models import UserScan

async def run_diagnostic():
    print("--- 🧪 DIVINEO AI: JULES ENGINE DIAGNOSTIC ---")

    # Mock the LLM response
    mock_response = MagicMock()
    mock_response.text = "This is a luxury style advice in French, English, and Spanish."
    jules_engine.model.generate_content.return_value = mock_response

    # Simulate a user scan
    test_scan = UserScan(
        user_id="LAFAYETTE_LEAD_USER",
        token="1740684000.SIMULATED_SIG", # Mock valid-looking token
        waist=75.0,
        event_type="Gala"
    )

    print(f"Testing Scan: {test_scan.event_type}...")

    # Execute the recommendation logic
    try:
        # recommend_garment in main.py expects (scan, garment_id)
        # Note: we need to bypass verify_auth if we don't have the secret key
        # For simplicity, let's mock verify_auth in main
        import main
        main.verify_auth = MagicMock(return_value=True)

        result = await recommend_garment(test_scan, garment_id="BALMAIN_SS26_SLIM")

        print("\n[✔] Backend Response Received:")
        print(f"Status: {result['status']}")
        print("\n--- JULES STYLE ADVICE ---")
        print(result['styling_advice'])

        # Final Validation
        advice = result['styling_advice'].lower()
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
