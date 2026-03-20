import os
import functools
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

@functools.lru_cache(maxsize=128)
def _get_cached_jules_advice(event_type, garment_name, drape, elasticity):
    """
    Internal cached function to generate LLM advice.
    Using primitive types as arguments ensures they are hashable.
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
    ⚡ Bolt: Added LRU cache to reduce expensive LLM calls for repeated parameters.
    """
    # garment is a dict (from GARMENT_DB) or Garment object.
    # The prompt usage implies dict access: garment['name']

    # Handle both dict and Pydantic model
    if hasattr(garment, 'dict'):
        garment_data = garment.dict()
    else:
        garment_data = garment

    # Extract stable fields for the cache key
    # We round numeric values to increase cache hits for similar silhouettes
    return _get_cached_jules_advice(
        user_data.event_type,
        garment_data['name'],
        garment_data.get('drape', 'Natural Fall'),
        garment_data.get('elasticity', 'Standard')
    )
