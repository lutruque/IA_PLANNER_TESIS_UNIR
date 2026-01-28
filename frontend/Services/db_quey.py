from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine(
    "postgresql+pg8000://usuario:password@localhost:5432/nombre_base_datos"
)

def obtener_ciudades():
    query = text("""
        SELECT ciudad
        FROM auxiliary_master.ciudades C
        JOIN auxiliary_master.departamentos D ON C.id_departamento = D.id_departamento
        JOIN auxiliary_master.paises P ON D.id_pais = P.id_pais
        WHERE P.id_pais = 1;
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df["ciudad"].dropna().unique().tolist()


def obtener_coordenadas(ciudad: str):
    query = text("""
        SELECT latitud, longitud
        FROM auxiliary_master.ciudades C
        JOIN auxiliary_master.departamentos D ON C.id_departamento = D.id_departamento
        JOIN auxiliary_master.paises P ON D.id_pais = P.id_pais
        WHERE P.id_pais = 1 AND ciudad = :ciudad;
    """)
    with engine.connect() as conn:
        r = conn.execute(query, {"ciudad": ciudad}).fetchone()
    return {"latitud": r[0], "longitud": r[1]} if r else None


def obtener_foto_atraccion(nombre_atraccion: str, ciudad: str):
    query = text("""
        SELECT "Link_atraccion"
        FROM auxiliary_master.atracciones
        WHERE LOWER(nombre_atraccion) = LOWER(:nombre)
        LIMIT 1;
    """)
    with engine.connect() as conn:
        r = conn.execute(query, {"nombre": nombre_atraccion}).fetchone()
    return r[0] if r else None


def obtener_datos_turismo():
    query = text("""
        SELECT anio, mes, establecimiento, tipo_establecimiento,
               llegadas_nacionales, llegadas_internacionales,
               habitaciones, camas, prestadores_turisticos,
               ciudad, id_ciudad
        FROM auxiliary_master.datos_turismo;
    """)
    with engine.connect() as conn:
        return pd.read_sql(query, conn)
