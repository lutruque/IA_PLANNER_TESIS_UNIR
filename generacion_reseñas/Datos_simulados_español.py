import pandas as pd
from faker import Faker
import random
from tqdm import tqdm
import os
import torch

# ============================================================
# CONFIGURACIÓN INICIAL
# ============================================================

fake = Faker("es_CO")

# 🔧 PARÁMETRO EDITABLE: CANTIDAD TOTAL DE RESEÑAS
TOTAL_RESEÑAS = 150  # 🔁 Modifica este número según tus necesidades

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================
def inferir_region(departamento):
    dept = str(departamento).lower()
    if any(p in dept for p in ['cundinamarca', 'antioquia', 'santander', 'boyacá', 'huila', 'tolima']):
        return 'Andina'
    elif any(p in dept for p in ['risaralda', 'caldas', 'quindío', 'pereira', 'manizales', 'armenia']):
        return 'Eje Cafetero'
    elif any(p in dept for p in ['bolívar', 'magdalena', 'atlántico', 'guajira', 'cartagena', 'santa marta', 'san andrés', 'riohacha']):
        return 'Caribe'
    else:
        return 'Otra'

# ============================================================
# GENERADOR DE RESEÑAS
# ============================================================
class GeneradorResenasAvanzado:
    def __init__(self):
        self.aspectos = {
            'servicio': [
                "El personal fue {adjetivo} y {adjetivo}",
                "La atención al cliente {fue} {adjetivo}",
                "El servicio {fue} {adjetivo} y {adjetivo}",
                "Los empleados {eran} {adjetivo} y {adjetivo}",
                "La recepción {fue} {adjetivo} en todo momento",
                "El staff {demostró} {adjetivo} profesionalismo"
            ],
            'habitacion': [
                "La habitación {fue} {adjetivo} y {adjetivo}",
                "El cuarto {tenia} {caracteristica} y {caracteristica}",
                "Las instalaciones {eran} {adjetivo}",
                "El espacio {fue} {adjetivo} para {actividad}",
                "La cama {resultó} {adjetivo} y {adjetivo}",
                "El baño {estaba} {adjetivo} y {adjetivo}"
            ],
            'comida': [
                "La comida {fue} {adjetivo} y {adjetivo}",
                "El restaurante {ofrecia} {plato} {adjetivo}",
                "El desayuno {incluia} {comida} y {comida}",
                "La gastronomía {fue} {adjetivo}",
                "Los platos {eran} {adjetivo} y {adjetivo}",
                "La variedad de alimentos {fue} {adjetivo}"
            ],
            'ubicacion': [
                "La ubicación {fue} {adjetivo} para {actividad}",
                "El hotel está {situado} cerca de {lugar}",
                "La localización {permite} {actividad} fácilmente",
                "Queda {distancia} de {atraccion}",
                "El acceso a {punto_interes} {fue} {adjetivo}",
                "La zona {es} {adjetivo} para {actividad}"
            ],
            'limpieza': [
                "La limpieza {fue} {adjetivo} en todas las áreas",
                "Las instalaciones {estaban} {adjetivo} mantenidas",
                "La higiene {cumplió} con los estándares {adjetivo}",
                "Todo {estaba} {adjetivo} y {adjetivo}",
                "El orden y aseo {eran} {adjetivo}",
                "La presentación {fue} {adjetivo} en general"
            ]
        }

        self.adjetivos_positivos = [
            "excelente", "maravilloso", "increíble", "fantástico", "sobresaliente",
            "impresionante", "magnífico", "perfecto", "espectacular", "agradable",
            "cómodo", "acogedor", "eficiente", "atento", "amable", "profesional",
            "excepcional", "destacable", "notable", "superior", "óptimo", "ideal"
        ]

        self.adjetivos_negativos = [
            "decepcionante", "regular", "mediocre", "pobre", "deficiente",
            "lento", "desorganizado", "antiguo", "incómodo", "ruidoso",
            "insuficiente", "inadecuado", "limitado", "básico", "simple"
        ]

        self.caracteristicas = [
            "vista panorámica", "cama king size", "jacuzzi", "balcón privado",
            "diseño moderno", "iluminación natural", "aislamiento acústico",
            "decoración elegante", "espacio amplio", "armarios espaciosos"
        ]

        self.actividades = [
            "descansar", "trabajar", "explorar la ciudad", "hacer turismo",
            "realizar negocios", "disfrutar en familia", "relajarse",
            "conocer la cultura local", "probar la gastronomía", "visitar museos"
        ]

        self.lugares = [
            "el centro histórico", "restaurantes locales", "centros comerciales",
            "atracciones turísticas", "estaciones de transporte", "parques naturales",
            "museos importantes", "zonas comerciales", "barrios tradicionales"
        ]

        self.puntos_interes = [
            "centro histórico", "zona comercial", "playa", "montaña",
            "área gastronómica", "parque natural", "museos", "galerías de arte"
        ]

        self.platos = [
            "platos típicos", "especialidades locales", "comida internacional",
            "gastronomía regional", "buffet variado", "menú ejecutivo"
        ]

        self.comidas = [
            "frutas frescas", "café colombiano", "jugos naturales", "panadería artesanal",
            "carnes selectas", "pescados locales", "ensaladas frescas", "postres caseros"
        ]

        self.conclusiones_positivas = [
            "Sin duda volveré al {hotel} en mi próxima visita a {ciudad}.",
            "Recomiendo ampliamente el {hotel} para cualquier viajero que visite {ciudad}.",
            "Una experiencia memorable en el {hotel} de {ciudad} que superó todas las expectativas.",
            "Excelente relación calidad-precio en el {hotel}. Definitivamente regresaré.",
            "El {hotel} se ha convertido en mi opción preferida en {ciudad}.",
            "Perfecto para disfrutar de {ciudad} con comodidad y buen servicio.",
            "Ideal para viajes en familia o pareja, el {hotel} ofrece una experiencia completa.",
            "Cada detalle del {hotel} en {ciudad} fue pensado para una estadía inolvidable."
        ]

        self.conclusiones_negativas = [
            "No recomendaría el {hotel} de {ciudad}.",
            "Esperaba más del {hotel} por las referencias en {ciudad}.",
            "Hay aspectos importantes por mejorar en el {hotel} de {ciudad}.",
            "Considero que hay mejores opciones hoteleras en {ciudad}.",
            "La experiencia en el {hotel} no cumplió con las expectativas básicas.",
            "El {hotel} necesita mejorar su servicio para competir en {ciudad}.",
            "No volvería a alojarme en el {hotel} por la falta de atención al cliente.",
            "La relación calidad-precio del {hotel} en {ciudad} deja mucho que desear."
        ]

    def generar_resena_aleatoria(self, hotel, ciudad, rating):
        """Genera una reseña con reemplazos seguros y sin placeholders residuales."""
        aspectos = random.sample(list(self.aspectos.keys()), random.randint(3, 4))
        partes = []
        positivos = rating >= 6
        adjetivos = self.adjetivos_positivos if positivos else self.adjetivos_negativos
        verbos_positivos = ["fue", "estuvo", "resultó", "demostró", "mostró"]
        verbos_negativos = ["fue", "estuvo", "dejó que desear", "careció de", "no cumplió"]
        verbos = verbos_positivos if positivos else verbos_negativos

        for asp in aspectos:
            template = random.choice(self.aspectos[asp])

            # seleccionar dos adjetivos distintos
            if len(adjetivos) >= 2:
                adj1, adj2 = random.sample(adjetivos, 2)
            else:
                adj1 = adj2 = adjetivos[0]

            frase = template

            # reemplazos ordenados y seguros (uso .replace con conteo cuando corresponde)
            frase = frase.replace("{adjetivo}", adj1, 1)
            frase = frase.replace("{adjetivo}", adj2)
            frase = frase.replace("{fue}", random.choice(verbos))
            frase = frase.replace("{eran}", random.choice(verbos))
            frase = frase.replace("{estaba}", random.choice(verbos))
            frase = frase.replace("{estaban}", random.choice(verbos))
            frase = frase.replace("{es}", random.choice(verbos))
            frase = frase.replace("{tenia}", "tenía" if positivos else "carecía de")
            frase = frase.replace("{demostró}", "demostró" if positivos else "no demostró")
            frase = frase.replace("{mostró}", "mostró" if positivos else "no mostró")
            frase = frase.replace("{cumplió}", "cumplió" if positivos else "no cumplió")
            frase = frase.replace("{situado}", "estratégicamente situado" if positivos else "mal ubicado")
            frase = frase.replace("{permite}", "permite" if positivos else "dificulta")
            frase = frase.replace("{distancia}", "a pocos minutos" if positivos else "bastante lejos")
            frase = frase.replace("{ofrecia}", "ofrecía" if positivos else "no ofrecía")
            frase = frase.replace("{incluia}", "incluía" if positivos else "no incluía")

            # contenido contextual
            frase = frase.replace("{caracteristica}", random.choice(self.caracteristicas))
            frase = frase.replace("{actividad}", random.choice(self.actividades))
            frase = frase.replace("{lugar}", random.choice(self.lugares))
            frase = frase.replace("{punto_interes}", random.choice(self.puntos_interes))
            frase = frase.replace("{atraccion}", random.choice(self.puntos_interes))
            frase = frase.replace("{plato}", random.choice(self.platos))
            frase = frase.replace("{comida}", random.choice(self.comidas))

            # eliminar cualquier placeholder restante por si acaso
            # (sustituimos llaves residuales por texto neutro para evitar salidas con {...})
            frase = frase.replace("{", "").replace("}", "")

            # limpieza y capitalizar
            frase = " ".join(frase.split()).strip()
            if frase:
                frase = frase[0].upper() + frase[1:]
            partes.append(frase)

        # conclusión
        conclusion = random.choice(self.conclusiones_positivas if positivos else self.conclusiones_negativas)
        conclusion = conclusion.format(hotel=hotel, ciudad=ciudad)
        partes.append(conclusion)

        reseña = ". ".join([p for p in partes if p])
        if not reseña.endswith("."):
            reseña += "."
        return reseña

    def generar_resena_mezclada(self, hotel, ciudad, rating, reseñas_reales=None, prop_real=0.10):
        """
        Si 'reseñas_reales' se pasa (lista), mezcla una reseña real con probabilidad 'prop_real'.
        Devuelve la reseña (ya limpia).
        """
        if reseñas_reales and random.random() < prop_real:
            real = random.choice(reseñas_reales).strip()
            # si la reseña real tiene placeholders, limpiarlos
            real = real.replace("{", "").replace("}", "")
            # si la reseña real es muy corta, generar sintética en vez de usarla
            if len(real.split()) < 5:
                return self.generar_resena_aleatoria(hotel, ciudad, rating)
            return real
        else:
            return self.generar_resena_aleatoria(hotel, ciudad, rating)



# ============================================================
# CIUDADES, HOTELES Y PORCENTAJES
# ============================================================
nombres_hoteles = {
    "Bogotá": ["Hotel Tequendama", "Hotel Dann Carlton", "Hotel Bacatá", "Hotel Habitel", "Hotel Capital"],
    "Medellín": ["Hotel Dann Carlton Belfort", "Hotel Nutibara", "Hotel Poblado Plaza", "Hotel Charlee", "Hotel Sites"],
    "Pereira": ["Hotel Movich", "Hotel Sonesta", "Hotel Boutique Sazagua", "Hotel Decameron", "Hotel Soratama"],
    "Manizales": ["Hotel Termales del Otoño", "Hotel Varuna", "Hotel Las Colinas", "Hotel Estelar", "Hotel Carretero"],
    "Armenia": ["Hotel Bolívar Plaza", "Hotel Estelar", "Hotel Zuldemayda", "Hotel Mirador del Cocora", "Hotel Mariscal"],
    "Cartagena": ["Hotel Charleston Santa Teresa", "Hotel Sofitel Legend Santa Clara", "Hotel Casa San Agustín", "Hotel Hyatt Regency", "Hotel Hilton Cartagena"],
    "Santa Marta": ["Hotel Irotama", "Hotel Estelar Santamar", "Hotel Dann Carlton", "Hotel La Riviera", "Hotel Zuana"],
    "Barranquilla": ["Hotel El Prado", "Hotel Dann Carlton", "Hotel Barranquilla Plaza", "Hotel Estelar Reina Catalina", "Hotel Majestic"],
    "San Andrés": ["Hotel Decameron San Luis", "Hotel Sol Caribe San Andrés", "Hotel GHL Relax", "Hotel Casablanca", "Hotel Sunrise"],
    "Riohacha": ["Hotel Taroa", "Hotel Waya Guajira", "Hotel Los Cardones", "Hotel Boutique Malecón", "Hotel Costa del Sol"]
}

departamentos = {
    "Bogotá": "Cundinamarca", "Medellín": "Antioquia", "Pereira": "Risaralda",
    "Manizales": "Caldas", "Armenia": "Quindío", "Cartagena": "Bolívar",
    "Santa Marta": "Magdalena", "Barranquilla": "Atlántico",
    "San Andrés": "San Andrés y Providencia", "Riohacha": "La Guajira"
}

porcentaje_ciudad = {
    "Bogotá": 0.20, "Medellín": 0.15, "Pereira": 0.10, "Manizales": 0.10,
    "Armenia": 0.10, "Cartagena": 0.10, "Santa Marta": 0.08,
    "Barranquilla": 0.07, "San Andrés": 0.05, "Riohacha": 0.05
}

# ============================================================
# GENERACIÓN DE DATOS
# ============================================================
resenas_por_ciudad = {c: int(TOTAL_RESEÑAS * p) for c, p in porcentaje_ciudad.items()}
generador = GeneradorResenasAvanzado()
data = []

print(f"🔄 Generando {TOTAL_RESEÑAS} reseñas distribuidas por ciudad...\n")

for ciudad, cantidad in tqdm(resenas_por_ciudad.items(), desc="Generando"):
    dept = departamentos.get(ciudad, "Desconocido")
    hoteles = nombres_hoteles[ciudad]
    for _ in range(cantidad):
        hotel = random.choice(hoteles)
        rating = round(random.uniform(3.0, 10.0), 1)
        reseña = generador.generar_resena_aleatoria(hotel, ciudad, rating)
        data.append({
            "hotel": hotel,
            "ciudad": ciudad,
            "departamento": dept,
            "region": inferir_region(dept),
            "rating": rating,
            "userName": fake.name(),
            "resena": reseña
        })

# ============================================================
# GUARDAR RESULTADOS
# ============================================================
df = pd.DataFrame(data)
archivo = f"Resenas_Turismo_Colombia_{TOTAL_RESEÑAS}.csv"
df.to_csv(archivo, index=False, encoding="utf-8-sig")

print(f"\n✅ Archivo guardado: {archivo}")
print(f"📊 Total reseñas generadas: {len(df)}")
print("\n📝 Ejemplos:\n")
for i in range(5):
    row = df.iloc[i]
    print(f"🏨 {row['hotel']} - {row['ciudad']} ({row['region']}) ⭐ {row['rating']}")
    print(f"👤 {row['userName']}")
    print(f"💬 {row['resena']}\n")





from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import text

# 🔗 Conexión a tu base de datos (ajusta si cambian tus credenciales)
CADENA = "postgresql+pg8000://postgres:Ja2141429@localhost:5432/tfe"



try:
    engine = create_engine(CADENA)
    with engine.connect() as conn:
        r = conn.execute(text("SELECT version();"))
        print("Conexión exitosa:", r.fetchone())
except Exception as e:
    print("Error:", e)


# ==========================
# ⚙️ FUNCIÓN: INSERTAR HOTEL SOLO SI NO EXISTE
# ==========================
def insertar_hotel_si_no_existe(row, conn):
    """
    Inserta un hotel solo si no existe en la base de datos.
    Retorna el id_hotel.
    """
    nombre = row["nombre_hotel"]
    ciudad = row["ciudad"]
   ## departamento = row["departamento"]

    # 1️⃣ Verificar existencia
    query_existencia = text("""
        SELECT id_hotel 
        FROM auxiliary_master.hoteles
        WHERE nombre_hotel = :nombre;
    """)

    result = conn.execute(query_existencia, {
        "nombre": nombre,
        "ciudad": ciudad
    }).fetchone()

    if result:
        # Ya existe → retornar id_hotel existente
        return result[0]

    # 2️⃣ Insertar si NO existe
    query_insert = text("""
        INSERT INTO auxiliary_master.hoteles (nombre_hotel, ciudad, descripcion_hotel, id_ciudad, direccion)
        VALUES (:nombre, :ciudad, NULL, NULL, NULL)
        RETURNING id_hotel;
    """)

    result_insert = conn.execute(query_insert, {
        "nombre": nombre,
        "ciudad": ciudad
    }).fetchone()

    return result_insert[0]


# ==========================
# ⚙️ INSERTAR HOTELES DESDE EL DATAFRAME
# ==========================
def insertar_hoteles(df):
    df_hoteles = df[['hotel','ciudad']].drop_duplicates()

    df_hoteles = df_hoteles.rename(columns={
        "hotel": "nombre_hotel",
        "ciudad": "ciudad"
        ##"departamento": "departamento"
    })

    with engine.begin() as conn:
        df_hoteles["id_hotel"] = df_hoteles.apply(lambda row: insertar_hotel_si_no_existe(row, conn), axis=1)

    print("✔ Hoteles insertados correctamente o ya existentes validados.")
    return df_hoteles


print("\n📌 Cargando archivo de reseñas...")
df = pd.read_csv("Resenas_Turismo_Colombia_FLAN_Final.csv")

print("\n📌 Insertando hoteles si no existen...")
df_hoteles = insertar_hoteles(df)

print("\n📌 Recuperando IDs de hoteles...")
hoteles_db = pd.read_sql(
    "SELECT id_hotel, nombre_hotel FROM auxiliary_master.hoteles",
    engine
)

# ============================================================
# 8. INSERTAR HOTELES Y TRAER ID ASIGNADO
# ============================================================

# 1️⃣ Insertar hoteles en la BD si no existen
df_hoteles = insertar_hoteles(df)

# 2️⃣ Merge con df_original usando SOLO df_hoteles (sin duplicarlo)
df = df.merge(
    df_hoteles[["nombre_hotel", "id_hotel"]],
    left_on="hotel",
    right_on="nombre_hotel",
    how="left"
)

# Validación
print("\n📌 Después del primer merge con df_hoteles:")
print(df[["hotel", "id_hotel"]].head())

if df["id_hotel"].isna().any():
    print("⚠ Advertencia: Existen hoteles sin ID asignado. Vamos a recuperarlos desde la BD.")
else:
    print("✔ Todos los hoteles tienen ID asignado por df_hoteles.")


# ============================================================
# 9. Recuperar IDs directamente desde la base de datos (segunda verificación)
# ============================================================

hoteles_db = pd.read_sql(
    "SELECT id_hotel, nombre_hotel FROM auxiliary_master.hoteles",
    engine
)

df = df.drop(columns=["id_hotel"], errors="ignore")  # evitar duplicados de columna

df = df.merge(
    hoteles_db,
    left_on="hotel",
    right_on="nombre_hotel",
    how="left"
)

if df["id_hotel"].isna().any():
    print("❌ ERROR: aún existen hoteles sin ID. Revisa nombres o normalización.")
    print(df[df["id_hotel"].isna()][["hotel"]].drop_duplicates())
    raise ValueError("id_hotel no asignado para todas las filas.")

print("\n✔ ID de hoteles asignado correctamente para todas las filas.")


# ============================================================
# 10. Generar fechas aleatorias
# ============================================================
def fecha_aleatoria(inicio="2024-01-01", fin="2025-12-31"):
    inicio_dt = pd.to_datetime(inicio)
    fin_dt = pd.to_datetime(fin)
    delta = (fin_dt - inicio_dt).days
    dias_random = random.randrange(delta)
    return inicio_dt + timedelta(days=dias_random)


# ============================================================
# 11. Construcción del DataFrame limpio para hoteles_resenas
# ============================================================
df_res = pd.DataFrame({
    "nombre_persona": df["userName"],
    "calificacion": df["rating"],
    "fecha_resena": [fecha_aleatoria() for _ in range(len(df))],
    "id_hotel": df["id_hotel"],
    "resena": df["resena"]
})

print("\nColumnas df_res:", df_res.columns)
print(df_res.head())

# ============================================================
# 12. Insertar reseñas en PostgreSQL con manejo de errores
# ============================================================
# Limpia cualquier transacción fallida previa
engine.dispose()  # Reinicia el pool de conexiones


with engine.connect() as conn:
    conn.execute(text("ROLLBACK"))


try:
    df_res.to_sql(
        "hoteles_resenas",
        engine,
        schema="auxiliary_master",
        if_exists="append",
        index=False,
        chunksize=300
    )
    print("✔ Reseñas cargadas correctamente.")
except Exception as e:
    print("❌ ERROR al insertar reseñas:", e)
