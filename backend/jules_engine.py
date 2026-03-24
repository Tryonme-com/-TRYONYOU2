import os
import google.generativeai as genai
from dotenv import load_dotenv
from functools import lru_cache

# Load .env from the same directory or current directory
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Try loading from specific path if not found (e.g. running from root)
    load_dotenv("backend/.env")
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Warning: GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@lru_cache(maxsize=128)
def _get_cached_jules_advice(event_type: str, garment_name: str, drape: str, elasticity: str):
    """
    Internal helper to cache LLM recommendations using primitive types.
    """
    prompt = f"""
    You are 'Jules', a high-end fashion consultant at Galeries Lafayette.
    A client is interested in the '{garment_name}' for a {event_type}.

    Technical Context:
    - Fabric Drape: {drape}
    - Fabric Elasticity: {elasticity}

    Task:
    Explain why this garment is the perfect choice for their silhouette based
    strictly on how the fabric moves and adapts.

    STRICT RULES:
    1. NEVER mention weight, height, or numeric measurements.
    2. NEVER mention sizes (S, M, L, or numbers like 40, 42).
    3. Focus on elegance, comfort, and the fall of the fabric.
    4. Provide the response in French, followed by English and Spanish.
    """
    response = model.generate_content(prompt)
    return response.text

def get_jules_advice(user_data, garment):
    """
    Generates an emotional styling tip without mentioning body numbers or sizes.
    Uses LRU cache to reduce LLM latency for repeated garment/event combinations.
    """
    # Handle both dict and Pydantic model
    if hasattr(garment, 'dict'):
        garment_data = garment.dict()
    elif isinstance(garment, dict):
        garment_data = garment
    else:
        # Fallback for other potential types
        garment_data = {
            'name': getattr(garment, 'name', 'Unknown'),
            'drape': getattr(garment, 'drape', 'Standard'),
            'elasticity': getattr(garment, 'elasticity', 'Standard')
        }

    return _get_cached_jules_advice(
        user_data.event_type,
        garment_data.get('name', 'Unknown Garment'),
        garment_data.get('drape', 'Standard'),
        garment_data.get('elasticity', 'Standard')
    )
