from pydantic import BaseModel
from typing import Dict, List

class UserScan(BaseModel):
    height: float
    weight: float
    event_type: str  # e.g., 'Gala', 'Business', 'Cocktail'

class Garment(BaseModel):
    id: str
    name: str
    elasticity: str  # 'High', 'Medium', 'Low'
    drape: str       # 'Fluid', 'Structured', 'Heavy'
    ideal_metrics: Dict[str, float]

# Mock Database for Galeries Lafayette
GARMENT_DB = [
    {
        "id": "GL-001",
        "name": "Evening Silk Gown",
        "elasticity": "Medium",
        "drape": "Fluid",
        "ideal_metrics": {"chest": 90, "waist": 70}
    },
    {
        "id": "GL-002",
        "name": "Tailored Wool Suit",
        "elasticity": "Low",
        "drape": "Structured",
        "ideal_metrics": {"chest": 100, "waist": 85}
    }
]
