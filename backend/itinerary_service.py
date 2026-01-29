import time
from typing import Optional, List

from app.schemas import PlanRequest
from app.db.db_utils_1 import (
    get_attractions_for_itinerary,
    get_top_hotels_by_city,
)
from app.services.llm_service import summarize_with_llm
from app.services.metrics import print_metrics
from app.utils.text_utils import clean_one_line

# -----------------------------------
# Etiquetas en español para franjas
# -----------------------------------
SPANISH_SLOT_LABEL = {
    "morning": "mañana",
    "afternoon": "tarde",
    "evening": "noche",
    "any": "cualquier horario",
}


# ======================================================
# FUNCIÓN PRINCIPAL — CONSTRUCCIÓN DEL ITINERARIO
# ======================================================
def build_itinerary(req: PlanRequest) -> dict:
    """
    Construye un itinerario turístico determinístico a partir de
    atracciones almacenadas en la base de datos y complementa el
    resultado con resúmenes generados por IA.

    Métricas registradas:
    - Latencia de generación de resúmenes
    - Longitud de los textos generados
    - Uso de fallback nocturno
    """

    city = req.city_base
    days = req.days
    traveler_type: Optional[str] = req.profile[0] if req.profile else None

    # -----------------------------------
    # Obtener atracciones por franja
    # -----------------------------------
    slots = get_attractions_for_itinerary(city)

    morning_list = slots["morning"] or slots["any"]
    afternoon_list = slots["afternoon"] or slots["any"]
    evening_list = slots["evening"]  # puede ser vacía

    itinerary_days = []

    # índices circulares por franja
    m_idx = a_idx = e_idx = 0

    # evitar repetir atracciones
    used_global = set()

    fallback_night_count = 0

    # -----------------------------------
    # Selector circular sin repetición
    # -----------------------------------
    def choose_for_slot(lst, idx, used_ids):
        if not lst:
            return None, idx

        n = len(lst)
        for k in range(n):
            candidate = lst[(idx + k) % n]
            cid = candidate.get("id_atraccion")
            if cid not in used_ids:
                return candidate, (idx + k + 1) % n

        return None, idx

    # -----------------------------------
    # Construcción día a día
    # -----------------------------------
    for day in range(days):
        # MAÑANA
        m_act, m_idx = choose_for_slot(morning_list, m_idx, used_global)
        if m_act:
            used_global.add(m_act.get("id_atraccion"))

        # TARDE
        a_act, a_idx = choose_for_slot(afternoon_list, a_idx, used_global)
        if a_act:
            used_global.add(a_act.get("id_atraccion"))

        # NOCHE
        if evening_list:
            e_act, e_idx = choose_for_slot(evening_list, e_idx, used_global)
            if e_act:
                used_global.add(e_act.get("id_atraccion"))
        else:
            e_act = None

        # -----------------------------------
        # Formateo de actividades
        # -----------------------------------
        def fmt(act, fallback_text):
            if not act:
                return {
                    "activity": fallback_text,
                    "description": None,
                    "address": None,
                }
            return {
                "activity": act.get("nombre_atraccion"),
                "description": act.get("descripcion_atraccion"),
                "address": act.get("direccion"),
            }

        morning_slot = {
            "label": SPANISH_SLOT_LABEL["morning"],
            **fmt(
                m_act,
                "Desayuno tranquilo en el barrio donde te alojas para "
                "disfrutar el ambiente local.",
            ),
        }

        afternoon_slot = {
            "label": SPANISH_SLOT_LABEL["afternoon"],
            **fmt(
                a_act,
                "Recorrido libre por zonas comerciales y espacios urbanos "
                "para caminar y descansar.",
            ),
        }

        if not evening_list or e_act is None:
            fallback_night_count += 1
            evening_slot = {
                "label": SPANISH_SLOT_LABEL["evening"],
                "activity": f"Noche libre para disfrutar {city} a tu ritmo.",
                "description": None,
                "address": None,
            }
        else:
            evening_slot = {
                "label": SPANISH_SLOT_LABEL["evening"],
                **fmt(e_act, "Actividad nocturna sugerida"),
            }

        itinerary_days.append(
            {
                "day": day + 1,
                "city": city,
                "slots": {
                    "morning": morning_slot,
                    "afternoon": afternoon_slot,
                    "evening": evening_slot,
                },
                "notes": (
                    "Itinerario generado a partir de la base de datos de "
                    "atracciones y reglas determinísticas."
                ),
            }
        )

    # -----------------------------------
    # Hoteles sugeridos
    # -----------------------------------
    hotel_suggestions_raw = get_top_hotels_by_city(city, limit=2)

    hotel_suggestions = [
        {
            "name": h.get("nombre_hotel"),
            "city": h.get("ciudad"),
            "address": h.get("direccion"),
            "ranking": round(float(h.get("rating_avg", 0)), 1),
            "review_count": int(h.get("review_count", 0)),
        }
        for h in hotel_suggestions_raw
    ]

    if hotel_suggestions:
        hotel_text = "Hoteles recomendados: " + ", ".join(
            f"{h['name']} (⭐ {h['ranking']})" for h in hotel_suggestions
        )
    else:
        hotel_text = f"No hay hoteles con reseñas suficientes en {city}."

    # ======================================================
    # RESÚMENES CON IA + MÉTRICAS
    # ======================================================
    t0 = time.perf_counter()
    review_summary_hotels = summarize_with_llm(
        city=city,
        traveler_type=traveler_type,
        reviews=[h["name"] for h in hotel_suggestions],
    )
    review_summary_hotels = clean_one_line(review_summary_hotels)
    print_metrics("Resumen hoteles", t0, review_summary_hotels)

    # -----------------------------------
    # Métrica fallback nocturno
    # -----------------------------------
    print("[METRIC] Fallback nocturno")
    print(f"  - Veces utilizado: {fallback_night_count}")
    print(f"  - Total noches: {days}")
    print(f"  - Porcentaje fallback: {(fallback_night_count / days) * 100:.1f}%")

    # ======================================================
    # RESPUESTA FINAL
    # ======================================================
    return {
        "itinerary_id": f"it_{req.region.lower()}_{city.lower()}",
        "summary": {
            "region": req.region,
            "city_base": city,
            "days": days,
            "profile": req.profile,
            "review_summary_hotels": review_summary_hotels,
            "hotel_recommendation": hotel_text,
        },
        "days": itinerary_days,
        "hotel_suggestions": hotel_suggestions,
    }
