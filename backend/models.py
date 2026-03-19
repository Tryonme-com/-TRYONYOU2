from pydantic import BaseModel, Field
from typing import Dict, List

class UserScan(BaseModel):
    height: float = Field(..., ge=50, le=300)
    weight: float = Field(..., ge=20, le=500)
    event_type: str = Field(..., max_length=100)  # e.g., 'Gala', 'Business', 'Cocktail'

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
