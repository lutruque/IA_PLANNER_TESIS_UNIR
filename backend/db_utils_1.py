from sqlalchemy import create_engine, text
import pandas as pd

#  Conexión a tu base de datos (ajusta si cambian tus credenciales)
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ------------------------------------
# HOTELES REVIEWS
# ------------------------------------
def get_hotel_reviews(limit: int = 50, traveler_type: str | None = None):
    """
    Obtiene reseñas reales de la tabla hoteles_resenas.
    Si traveler_type no es None, filtra por r.tipo_viajero.
    """

    query = text("""
        SELECT 
            h.*, 
            r.nombre_persona, 
            r.calificacion, 
            r.resena, 
            r.fecha_resena, 
            r.tipo_viajero
        FROM auxiliary_master.hoteles_resenas r
        JOIN auxiliary_master.hoteles h 
            ON r.id_hotel = h.id_hotel
        WHERE (:traveler_type IS NULL 
               OR LOWER(r.tipo_viajero) = LOWER(:traveler_type))
        ORDER BY r.fecha_resena DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        df = pd.read_sql(
            query,
            conn,
            params={
                "limit": limit,
                "traveler_type": traveler_type,
            },
        )

    return df.to_dict(orient="records")


# ------------------------------------
# ATRACCIONES REVIEWS
# ------------------------------------
def get_attraction_reviews(
    ciudad: str,
    limit: int = 50,
    traveler_type: str | None = None,
):
    """
    Obtiene reseñas de atracciones filtradas por ciudad.
    JOIN con tabla atracciones para obtener información adicional.
    Si traveler_type no es None, filtra por A.tipo_viajero.
    """

    query = text("""
        SELECT 
            t.*, 
            a.id_resena_atraccion, 
            a.nombre_persona, 
            a.calificacion, 
            a.resena, 
            a.fecha_resena, 
            a.tipo_viajero
        FROM auxiliary_master.atracciones_resenas a
        JOIN auxiliary_master.atracciones t 
            ON t.id_atraccion = a.id_atraccion
        WHERE LOWER(t.ciudad) = LOWER(:ciudad)
          AND (:traveler_type IS NULL 
               OR LOWER(a.tipo_viajero) = LOWER(:traveler_type))
        ORDER BY a.fecha_resena DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        df = pd.read_sql(
            query,
            conn,
            params={
                "ciudad": ciudad,
                "limit": limit,
                "traveler_type": traveler_type,
            },
        )

    return df.to_dict(orient="records")


#-------------------------------------
# ATRACCIONES para itineario
# ------------------------------------

def get_attractions_for_itinerary(city: str):
    """
    Devuelve atracciones agrupadas por franja horaria:
    morning, afternoon, evening y any.
    """
    query = text("""
        SELECT 
            id_atraccion,
            nombre_atraccion,
            descripcion_atraccion,
            ciudad,
            direccion,
            franja_horaria
        FROM auxiliary_master.atracciones
        WHERE LOWER(ciudad) = LOWER(:city)
    """)

    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"city": city})

    records = df.to_dict(orient="records")

    # ==================================================
    #  DEBUG 1 — Ver qué datos vienen desde PostgreSQL
    # ==================================================
    print("\n=== DEBUG: ATRACCIONES CARGADAS DESDE BD ===")
    print(f"Ciudad solicitada: {city}")
    print(f"Total registros encontrados: {len(records)}")

    for r in records:
        print(f"- {r.get('nombre_atraccion')} | franjas: {r.get('franja_horaria')}")
    print("=== FIN DEBUG ===\n")
    # ==================================================

    # Slots para itinerario
    slots = {
        "morning": [],
        "afternoon": [],
        "evening": [],
        "any": []
    }

    for r in records:
        raw_franja = r.get("franja_horaria")

        # 1) Convertir a lista "cruda" de partes
        if raw_franja is None:
            parts = ["any"]

        elif isinstance(raw_franja, list):
            # puede traer elementos tipo '"morning"' → limpiar después
            parts = raw_franja

        else:
            # string tipo '{morning,afternoon}' o 'morning,afternoon'
            s = str(raw_franja).strip()
            s = s.replace("{", "").replace("}", "")
            parts = [p for p in s.split(",") if p.strip()]

        # 2) Limpiar cada parte: quitar comillas, espacios, pasar a minúsculas
        franjas = []
        for p in parts:
            cleaned = (
                str(p)
                .strip()
                .strip('"')
                .strip("'")
                .strip()
                .lower()
            )
            if cleaned:
                franjas.append(cleaned)

        if not franjas:
            franjas = ["any"]

        # 3) Asignar a slots
        for franja in franjas:
            if franja not in slots:
                franja = "any"
            slots[franja].append(r)

    return slots

def get_top_hotels_by_city(city: str, limit: int = 2):
    """
    Devuelve los mejores hoteles para una ciudad, usando:
    - promedio de calificación (rating_avg)
    - fecha de reseña más reciente (last_review_date) como desempate
    Solo considera hoteles que tengan al menos 1 reseña.
    """
    query = text("""
        SELECT
            h.id_hotel,
            h.nombre_hotel,
            h.descripcion_hotel,
            h.ciudad,
            h.direccion,
            AVG(r.calificacion)       AS rating_avg,
            MAX(r.fecha_resena)       AS last_review_date,
            COUNT(r.id_resena_hotel)  AS review_count
        FROM auxiliary_master.hoteles h
        JOIN auxiliary_master.hoteles_resenas r
            ON r.id_hotel = h.id_hotel
        WHERE LOWER(h.ciudad) = LOWER(:city)
        GROUP BY
            h.id_hotel,
            h.nombre_hotel,
            h.descripcion_hotel,
            h.ciudad,
            h.direccion
        HAVING COUNT(r.id_resena_hotel) > 0
        ORDER BY
            rating_avg DESC,
            last_review_date DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"city": city, "limit": limit})

    return df.to_dict(orient="records")
