import os
import google.generativeai as genai
from dotenv import load_dotenv

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

# Performance Optimization: Bounded in-memory cache for LLM recommendations
# Reduces latency and API costs for identical user/garment combinations
# Bounded to 128 entries to prevent unbounded memory growth (memory leak)
from functools import lru_cache

@lru_cache(maxsize=128)
def _get_cached_advice(event_type, height, weight, garment_id, drape, elasticity, garment_name):
    """
    Internal helper to use functools.lru_cache for memoization.
    Arguments must be hashable.
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
    Uses an LRU cache to store and reuse recommendations.
    """
    # Handle both dict and Pydantic model
    if hasattr(garment, 'dict'):
        garment_data = garment.dict()
    else:
        garment_data = garment

    # Normalization: Round metrics to nearest integer to improve cache hit rate
    # slightly different sensor readings shouldn't trigger new LLM calls
    rounded_height = round(user_data.height)
    rounded_weight = round(user_data.weight)
    garment_id = garment_data.get('id', garment_data.get('name'))

    # Delegate to the cached function
    return _get_cached_advice(
        user_data.event_type,
        rounded_height,
        rounded_weight,
        garment_id,
        garment_data['drape'],
        garment_data['elasticity'],
        garment_data['name']
    )
