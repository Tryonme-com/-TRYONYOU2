from pydantic import BaseModel
from typing import Dict, List, Optional

class UserScan(BaseModel):
    user_id: str
    token: str
    waist: float
    event_type: str  # e.g., 'Gala', 'Business', 'Cocktail'

class Garment(BaseModel):
    id: str
    name: str
    waist_flat_cm: float
    stretch_factor: float
    stock: int
    price: str
    variant_id: str

# 👗 Catálogo Shopify (Divineo Bunker)
SHOPIFY_INVENTORY = {
    "BALMAIN_SS26_SLIM": {
        "id": "BALMAIN_SS26_SLIM",
        "name": "Balmain Slim-Fit Jeans",
        "waist_flat_cm": 65,
        "stretch_factor": 1.15,
        "drape": "Architectural",
        "elasticity": "Dynamic",
        "stock": 12,
        "price": "1.290 €",
        "variant_id": "gid://shopify/ProductVariant/445566"
    },
    "LEVIS_510_STRETCH": {
        "id": "LEVIS_510_STRETCH",
        "name": "Levis 510 Skinny",
        "waist_flat_cm": 68,
        "stretch_factor": 1.10,
        "drape": "Fluid",
        "elasticity": "Standard",
        "stock": 45,
        "price": "110 €",
        "variant_id": "gid://shopify/ProductVariant/778899"
    }
}

GARMENT_DB = list(SHOPIFY_INVENTORY.values())
