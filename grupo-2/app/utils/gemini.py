import requests
from flask import current_app

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)

def consultar_gemini(prompt: str) -> str:
    """Envía un prompt a Gemini y retorna el texto de respuesta."""
    api_key = current_app.config.get("GEMINI_API_KEY", "")
    response = requests.post(
        GEMINI_URL,
        params={"key": api_key},
        json={
            "contents": [{"parts": [{"text": prompt}]}]
        },
        timeout=30,
    )
    if response.status_code != 200:
        return f"Error al contactar Gemini: {response.status_code} - {response.text}"
    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return "No se pudo obtener respuesta de Gemini."