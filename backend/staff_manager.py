"""
TRYONYOU V10 - STAFF UNIFORM MANAGER
Protocol: Minimalist Spotify Vibe
Official House Direct Order System
"""

class StaffUniformManager:
    def __init__(self):
        self.style = "Minimalist_Spotify_Vibe"
        self.colors = ["Matte_Black", "Peacock_White"]
        self.status = "READY"

    def pedir_dotacion(self, num_colaboradores: int):
        """Genera el pedido a la Casa Oficial (Sin intermediarios)"""
        pedido = {
            "items": ["Chaqueta_Tecnica", "Camisa_SavoirFaire", "Pin_Grinch"],
            "total_staff": num_colaboradores,
            "custom_qr": "https://open.spotify.com/playlist/artist_link",
            "colors": self.colors,
            "venue_size": "65m2",
            "venue_type": "Sac Museum Curators"
        }
        return f"ORDEN ENVIADA: Vestuario para {num_colaboradores} Curadores del Sac Museum (65m2)."

if __name__ == "__main__":
    manager = StaffUniformManager()
    print(manager.pedir_dotacion(5))
