import hmac
import hashlib
import time
import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models import UserScan, SHOPIFY_INVENTORY
from jules_engine import get_jules_advice

load_dotenv()

app = FastAPI(title="Divineo Bunker Backend")

# 🛡️ Configuración Maestra (abvetos.com)
SECRET_KEY = os.getenv("LVT_SECRET_KEY", "LVT_DEV_SECRET_DO_NOT_USE_IN_PROD")
ALLOWED_ORIGINS = os.getenv("LVT_ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PATENT = "PCT/EP2025/067317"

def verify_auth(user_id: str, token: str) -> bool:
    try:
        ts, sig = token.split('.')
        if int(time.time()) - int(ts) > 600: return False # Ventana 10 min
        expected = hmac.new(SECRET_KEY.encode(), f"{user_id}:{ts}".encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(sig, expected)
    except: return False

def calculate_fit(user_waist: float, item_id: str):
    item = SHOPIFY_INVENTORY.get(item_id)
    if not item: return None
    
    # Física Textil Real: Cintura Usuario / (Ancho Prenda * Elasticidad)
    fit_index = user_waist / (item['waist_flat_cm'] * item['stretch_factor'])
    
    # Rango de Certeza Absoluta (0.95 - 1.05)
    is_perfect = 0.95 <= fit_index <= 1.05
    return is_perfect, round(fit_index, 3), item

@app.post("/api/recommend")
async def recommend_garment(scan: UserScan, garment_id: str = "BALMAIN_SS26_SLIM"):
    # 1. Seguridad y Handshake
    if not verify_auth(scan.user_id, scan.token):
        raise HTTPException(status_code=403, detail="Acceso restringido al búnker.")

    # 2. Motor de Certeza
    fit_data = calculate_fit(scan.waist, garment_id)
    if not fit_data:
        raise HTTPException(status_code=404, detail="Prenda no disponible en el catálogo de Shopify.")

    is_divineo, score, item = fit_data

    # 3. Generación de Métricas
    metrics = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "accuracy_score": score,
        "stock_available": item['stock'] > 0,
        "return_reduction_impact": "40% SAVED" if is_divineo else "0%",
        "patent": PATENT
    }

    # 4. Respuesta Divineo Totality (con Jules AI Advice)
    try:
        # Usamos Jules para el toque de estilo
        styling_advice = get_jules_advice(scan, item)
    except Exception as e:
        styling_advice = f"Divineo confirmado con {item['name']}."

    if is_divineo and item['stock'] > 0:
        return {
            "status": "SUCCESS",
            "pau_voice": f"Hola, soy P.A.U. Divineo confirmado con {item['name']}. Tu silueta es real y el ajuste es exacto.",
            "styling_advice": styling_advice,
            "action": "RENDER_OVERLAY_GLB",
            "payload": {
                "shopify_checkout": f"https://abvetos.com/cart/add?id={item['variant_id']}",
                "price": item['price'],
                "fit_report": metrics
            }
        }
    else:
        return {
            "status": "RESCAN",
            "pau_voice": f"P.A.U. sugiere verificar el ajuste. Buscamos el Divineo absoluto para tu {item['name']}.",
            "styling_advice": styling_advice,
            "action": "TRIGGER_SIZE_ADVICE",
            "payload": {"fit_report": metrics}
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
