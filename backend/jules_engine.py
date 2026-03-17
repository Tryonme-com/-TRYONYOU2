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

from collections import OrderedDict

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# In-memory cache to store AI recommendations with a simple size limit (LRU-ish)
# Key: (garment_id, event_type, body_shape, fit_preference)
MAX_CACHE_SIZE = 100
_recommendation_cache = OrderedDict()

async def get_jules_advice(user_data, garment):
    """
    Generates an emotional styling tip without mentioning body numbers or sizes.
    Uses caching and asynchronous AI calls for performance.
    """
    # Handle both dict and Pydantic model for garment
    if hasattr(garment, 'get'):
        garment_data = garment
        garment_id = garment.get('id', 'unknown')
    else:
        garment_data = garment.dict()
        garment_id = garment_data.get('id', 'unknown')

    # Create a cache key
    cache_key = (
        garment_id,
        user_data.event_type,
        user_data.body_shape,
        user_data.fit_preference
    )

    # Check cache first (O(1) lookup)
    if cache_key in _recommendation_cache:
        # Move to end to mark as recently used
        _recommendation_cache.move_to_end(cache_key)
        return _recommendation_cache[cache_key]

    prompt = f"""
    You are 'Jules', a high-end fashion consultant at Galeries Lafayette.
    A client is interested in the '{garment_data['name']}' for a {user_data.event_type}.
    The client has a {user_data.body_shape} body shape and prefers a {user_data.fit_preference} fit.

    Technical Context:
    - Fabric Drape: {garment_data['drape']}
    - Fabric Elasticity: {garment_data['elasticity']}

    Task:
    Explain why this garment is the perfect choice for their silhouette based
    strictly on how the fabric moves and adapts.

    STRICT RULES:
    1. NEVER mention weight, height, or numeric measurements.
    2. NEVER mention sizes (S, M, L, or numbers like 40, 42).
    3. Focus on elegance, comfort, and the fall of the fabric.
    4. Provide the response in French, followed by English and Spanish.
    """

    # Use asynchronous generation to avoid blocking the event loop
    response = await model.generate_content_async(prompt)
    advice = response.text

    # Store in cache with size limit enforcement
    if len(_recommendation_cache) >= MAX_CACHE_SIZE:
        _recommendation_cache.popitem(last=False)  # Remove oldest item (FIFO/LRU)

    _recommendation_cache[cache_key] = advice

    return advice
