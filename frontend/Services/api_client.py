import requests

API_URL = "http://127.0.0.1:8000/plan_v3"
EMAIL_URL = "http://127.0.0.1:8000/plan_and_email"

def generar_itinerario(region, days, profile, city):
    payload = {
        "region": region,
        "days": days,
        "profile": [profile],
        "city_base": city
    }
    r = requests.post(API_URL, json=payload)
    r.raise_for_status()
    return r.json()


def enviar_itinerario(payload):
    r = requests.post(EMAIL_URL, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

