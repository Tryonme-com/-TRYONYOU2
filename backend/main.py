from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import UserScan, GARMENT_DB
from jules_engine import get_jules_advice

app = FastAPI(title="Divineo AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for the pilot
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/recommend")
async def recommend_garment(scan: UserScan):
    # Logic: For the pilot, we pick the first garment or match by event_type
    selected_garment = GARMENT_DB[0]

    try:
        recommendation = get_jules_advice(scan, selected_garment)
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "code": 503,
                "message": "Jules AI Engine is currently recalibrating or unavailable. Please try again."
            }
        )

    return {
        "garment_name": selected_garment["name"],
        "recommendation": recommendation,
        "status": "success"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
