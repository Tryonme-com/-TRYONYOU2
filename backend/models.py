from pydantic import BaseModel, Field
from typing import Dict, List

class UserScan(BaseModel):
    # Add validation to prevent malformed or malicious input
    height: float = Field(..., gt=50, lt=250, description="Height in cm")
    weight: float = Field(..., gt=20, lt=300, description="Weight in kg")
    event_type: str = Field(..., min_length=1, max_length=100)

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
