import sys
import os
import asyncio
import json

# Ensure we can import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import recommend_garment
from models import UserScan

async def run_diagnostic():
    print("--- 🧪 DIVINEO AI: JULES ENGINE DIAGNOSTIC ---")

    # Simulate a user scan for a luxury event
    test_scan = UserScan(
        height=175.0,
        weight=68.0,
        event_type="Galeries Lafayette Opening Gala"
    )

    print(f"Testing Scan: {test_scan.event_type}...")

    # Execute the recommendation logic
    try:
        result = await recommend_garment(test_scan)

        print("\n[✔] Backend Response Received:")
        print(f"Garment Selected: {result['garment_name']}")
        print("\n--- JULES STYLE ADVICE ---")
        print(result['recommendation'])

        # Final Validation
        advice = result['recommendation'].lower()
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
