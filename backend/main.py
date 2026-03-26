import os
import hmac
import hashlib
import time
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models import UserScan, StaffLogin, SHOPIFY_INVENTORY
from jules_engine import get_jules_advice

# Load .env file
load_dotenv()

app = FastAPI(title="Divineo Bunker Backend")

# 🛡️ Secure CORS configuration via environment variables
allowed_origins = os.getenv("LVT_ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🛡️ Configuración Maestra (abvetos.com) - Secrets moved to environment variables
SECRET_KEY = os.getenv("LVT_SECRET_KEY", "DEVELOPMENT_SECRET_DO_NOT_USE_IN_PROD")
STAFF_PASSWORD = os.getenv("STAFF_PASSWORD", "DEVELOPMENT_STAFF_PASS_DO_NOT_USE_IN_PROD")
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

@app.post("/api/verify-staff")
async def verify_staff(login: StaffLogin):
    """
    🛡️ Secure staff verification using hmac.compare_digest
    to prevent timing attacks.
    """
    if hmac.compare_digest(login.password.encode(), STAFF_PASSWORD.encode()):
        return {"status": "SUCCESS", "message": "Acceso concedido"}
    else:
        raise HTTPException(status_code=401, detail="Acceso denegado")

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
