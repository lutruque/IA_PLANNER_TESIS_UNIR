import pandas as pd
import random
from faker import Faker
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm import tqdm
import torch

# Inicializar Faker en español y en inglés
fake_es = Faker("es_CO")
fake_en = Faker("en_US")

# Cargar modelo FLAN-T5
modelo = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(modelo)
model = AutoModelForSeq2SeqLM.from_pretrained(modelo)

# Usar GPU si está disponible
if torch.cuda.is_available():
    model = model.to("cuda")
nombres_hoteles = {
    "Bogotá": [
        "Hotel Tequendama", "Hotel Dann Carlton", "Hotel Bacatá", "Hotel Habitel", "Hotel Capital",
        "Hotel Bogotá Plaza", "Hotel Estelar La Boheme", "Hotel Morrison", "Hotel NH Collection",
        "Hotel Dorado Plaza", "Hotel San Francisco", "Hotel La Opera", "Hotel Casa Deco",
        "Hotel Boutique BH", "Hotel GHL Suite", "Hotel Ibis", "Hotel Hilton", "Hotel Sheraton",
        "Hotel Wyndham", "Hotel Grand Hyatt"
    ],
    "Medellín": [
        "Hotel Dann Carlton Belfort", "Hotel Nutibara", "Hotel Poblado Plaza", "Hotel Charlee",
        "Hotel Celestino", "Hotel Sites", "Hotel Viaggio", "Hotel Mercure", "Hotel Diez",
        "Hotel Cabo Verde", "Hotel Portón de San Joaquín", "Hotel Boutique Lleras",
        "Hotel San Fernando Plaza", "Hotel Poblado Alejandría", "Hotel Mónaco",
        "Hotel Parque 87", "Hotel Inntu", "Hotel Los Balsos", "Hotel Estelar Blue",
        "Hotel Torre Poblado"
    ],
    "Bucaramanga": [
        "Hotel Chicamocha", "Hotel Dann Carlton", "Hotel Bh Búcaros", "Hotel Ruitoque Plaza",
        "Hotel San Francisco", "Hotel Girón Plaza", "Hotel Carrizal", "Hotel Cumbre",
        "Hotel Morrorico", "Hotel Guane", "Hotel Santorini", "Hotel Boutique La Quinta",
        "Hotel Casa Madrileña", "Hotel Floridablanca", "Hotel Girón Real", "Hotel Portal del Sol",
        "Hotel Villa Antigua", "Hotel San Pío", "Hotel Campestre", "Hotel La Triada"
    ],
    "Tunja": [
        "Hotel Hunza", "Hotel Muisca", "Hotel Santa Fe", "Hotel Boyacá", "Hotel San Carlos",
        "Hotel Colonial", "Hotel Camino Real", "Hotel Casa Real", "Hotel La Posada",
        "Hotel San Agustín", "Hotel Villa de Leyva", "Hotel Suescún", "Hotel Boutique San Ignacio",
        "Hotel Casona del Molino", "Hotel Plaza Mayor", "Hotel Mansión de los Virreyes",
        "Hotel Real de Minas", "Hotel Campestre La Casona", "Hotel San Francisco de Asís",
        "Hotel Doña Jerónima"
    ],
    "Neiva": [
        "Hotel Plaza", "Hotel Boutique La Casona", "Hotel Campestre Matamundo", "Hotel San Miguel",
        "Hotel Himalaya", "Hotel Neiva Plaza", "Hotel Huila Real", "Hotel Opalla",
        "Hotel Campestre La Esperanza", "Hotel Villa Sara", "Hotel Tolima", "Hotel Rivera",
        "Hotel Boutique San Jorge", "Hotel Campestre Los Guaduales", "Hotel Hacaritama",
        "Hotel San Agustín", "Hotel Colonial", "Hotel Las Palmas", "Hotel Río Neiva",
        "Hotel Campestre La Voragine"
    ],
    "Pereira": [
        "Hotel Movich", "Hotel Sonesta", "Hotel Boutique Sazagua", "Hotel Decameron",
        "Hotel Café Royal", "Hotel Abadia Plaza", "Hotel Gran", "Hotel Soratama",
        "Hotel Ibis", "Hotel Los Granados", "Hotel Campestre La Gaviota", "Hotel Mirador",
        "Hotel Edivan", "Hotel San Joaquín", "Hotel Boutique La Casona", "Hotel Hacienda San José",
        "Hotel Campestre La Pradera", "Hotel Don Lolo", "Hotel Villa Maria", "Hotel Arauca"
    ],
    "Manizales": [
        "Hotel Termales del Otoño", "Hotel Varuna", "Hotel Las Colinas", "Hotel Estelar",
        "Hotel Recinto del Pensamiento", "Hotel Campestre La Rochela", "Hotel Boutique Casa de Lola",
        "Hotel Fundadores", "Hotel Mirador del Nevado", "Hotel Carretero", "Hotel Tinamú",
        "Hotel Campestre Hacienda Venecia", "Hotel Los Rosales", "Hotel Montecarlo",
        "Hotel Casa de los Arrieros", "Hotel Terrazas", "Hotel Campestre La Cabaña",
        "Hotel San Francisco", "Hotel Mirador Andino", "Hotel La Suiza"
    ],
    "Armenia": [
        "Hotel Bolívar Plaza", "Hotel Café Quindío", "Hotel Estelar", "Hotel Zuldemayda",
        "Hotel Mirador del Cocora", "Hotel Campestre La Cabaña", "Hotel Boutique La Posada",
        "Hotel Mariscal", "Hotel San Hotel", "Hotel Mirador Andino", "Hotel Campestre La Pequeña",
        "Hotel Las Colinas", "Hotel Portal del Quindío", "Hotel Campestre La Pradera",
        "Hotel Villa de Leyva", "Hotel Los Álamos", "Hotel Hacienda San Rafael",
        "Hotel Boutique El Edén", "Hotel Mirador del Valle", "Hotel La Casona"
    ],
    "Salento": [
        "Hotel Salento Real", "Hotel Boutique Kawa Mountain", "Hotel El Mirador del Cocora",
        "Hotel La Posada del Café", "Hotel Campestre El Edén", "Hotel Las Acacias",
        "Hotel La Cabaña", "Hotel Villa Martha", "Hotel El Rancho de Emilio",
        "Hotel Boutique Los Pinos", "Hotel Campestre La Floresta", "Hotel El Portal de Salento",
        "Hotel Las Palmeras", "Hotel Mirador Andino", "Hotel La Casona de Lili",
        "Hotel Boutique El Nogal", "Hotel Campestre La Colina", "Hotel Los Fundadores",
        "Hotel Villa del Café", "Hotel El Rinconcito"
    ],
    "Filandia": [
        "Hotel Boutique La Posada de la Plaza", "Hotel El Mirador de Filandia",
        "Hotel Campestre El Jardín", "Hotel La Casona de los Arrieros", "Hotel Boutique El Balcón",
        "Hotel Las Colinas", "Hotel El Portal del Quindío", "Hotel Campestre La Pradera",
        "Hotel Villa Helvetica", "Hotel Boutique La Floresta", "Hotel El Rancho",
        "Hotel Mirador del Paisaje", "Hotel La Cabaña", "Hotel Boutique Los Alamos",
        "Hotel Campestre La Esperanza", "Hotel El Refugio", "Hotel Las Acacias",
        "Hotel Boutique El Nogal", "Hotel La Posada", "Hotel Mirador Andino"
    ],
    "Cartagena": [
        "Hotel Charleston Santa Teresa", "Hotel Sofitel Legend Santa Clara", "Hotel Casa San Agustín",
        "Hotel Hyatt Regency", "Hotel Hilton Cartagena", "Hotel Estelar Cartagena de Indias",
        "Hotel Movich Cartagena", "Hotel Casa Pestagua", "Hotel Boutique La Passion",
        "Hotel Las Américas", "Hotel Caribe", "Hotel San Pedro de Majagua", "Hotel Boutique Bantú",
        "Hotel GHL Collection", "Hotel Holiday Inn", "Hotel Boutique Casa del Arzobispado",
        "Hotel Don Pedro de Heredia", "Hotel Boutique La Merced", "Hotel Tres Banderas",
        "Hotel Boutique El Viajero"
    ],
    "Santa Marta": [
        "Hotel Irotama", "Hotel Estelar Santamar", "Hotel Dann Carlton", "Hotel La Riviera",
        "Hotel Zuana", "Hotel Los Delfines", "Hotel Boutique La Casa del Farol",
        "Hotel GHL Relax", "Hotel Tamacá", "Hotel Aluna", "Hotel Boutique Don Pepe",
        "Hotel Sierra Nevada", "Hotel La Bahía", "Hotel Boutique La Tagua",
        "Hotel San Fernando", "Hotel Playa Salguero", "Hotel Boutique Casa de Isabella",
        "Hotel Marazul", "Hotel Miramar", "Hotel Boutique El Rodadero"
    ],
    "Barranquilla": [
        "Hotel El Prado", "Hotel Dann Carlton", "Hotel Barranquilla Plaza", "Hotel Estelar Reina Catalina",
        "Hotel Howard Johnson", "Hotel Majestic", "Hotel Casa del Mar", "Hotel GHL Collection",
        "Hotel Ibis", "Hotel Boutique La Cueva", "Hotel San Francisco", "Hotel Riviera",
        "Hotel Dorado", "Hotel Campestre La Sierra", "Hotel Boutique El Granadillo",
        "Hotel Miramar", "Hotel Las Américas", "Hotel Costa Caribe", "Hotel Boutique La Quinta",
        "Hotel Plaza Central"
    ],
    "San Andrés": [
        "Hotel Decameron San Luis", "Hotel Sol Caribe San Andrés", "Hotel GHL Relax",
        "Hotel Casablanca", "Hotel Portobelo", "Hotel Sunrise", "Hotel Cocoplum",
        "Hotel Bahía Sardina", "Hotel Aquamare", "Hotel Sea Garden", "Hotel Lord Pierre",
        "Hotel Isla Bonita", "Hotel Crystal Beach", "Hotel Maryland", "Hotel Tiuna",
        "Hotel Villa San Andrés", "Hotel Boutique Las Palmeras", "Hotel Playa Tranquila",
        "Hotel Caribbean Paradise", "Hotel Boutique Sea Flower"
    ],
    "Riohacha": [
        "Hotel Taroa", "Hotel Waya Guajira", "Hotel Los Cardones", "Hotel Boutique Malecón",
        "Hotel Costa del Sol", "Hotel Riohacha Plaza", "Hotel Villa del Mar",
        "Hotel Boutique La Guajira", "Hotel Las Américas", "Hotel Miramar",
        "Hotel Campestre El Paraíso", "Hotel Boutique El Faro", "Hotel La Riviera",
        "Hotel San Juan", "Hotel Las Dunas", "Hotel Boutique Mar Azul", "Hotel La Casona",
        "Hotel El Prado", "Hotel Bahía de la Guajira", "Hotel Boutique Los Flamencos"
    ]
}
# === Sufijos para hoteles ===
sufijos_hoteles = [
    "", " Internacional", " Plaza", " Suites", " Boutique", " Express", " Premier",
    " Luxury", " Business", " Resort", " Campestre", " & Spa", " Royal", " Gran",
    " Central", " del Sol", " de la Montaña", " City", " Executive", " Inn"
]
# === Definir regiones y ciudades ===
regiones = {
    "Andina": ["Bogotá", "Medellín", "Bucaramanga", "Tunja", "Neiva"],
    "Eje Cafetero": ["Pereira", "Manizales", "Armenia", "Salento", "Filandia"],
    "Caribe": ["Cartagena", "Santa Marta", "Barranquilla", "San Andrés", "Riohacha"]
}

departamentos = {
    "Bogotá": "Cundinamarca",
    "Medellín": "Antioquia",
    "Bucaramanga": "Santander",
    "Tunja": "Boyacá",
    "Neiva": "Huila",
    "Pereira": "Risaralda",
    "Manizales": "Caldas",
    "Armenia": "Quindío",
    "Salento": "Quindío",
    "Filandia": "Quindío",
    "Cartagena": "Bolívar",
    "Santa Marta": "Magdalena",
    "Barranquilla": "Atlántico",
    "San Andrés": "San Andrés y Providencia",
    "Riohacha": "La Guajira"
}

# === Parámetros de simulación ===
num_resenas = 100  # puedes subirlo a 10000 cuando lo pruebes
idiomas = ["English"]
viajeros = ["Pareja", "Familia", "Amigos", "Negocios", "Individual"]
hotel = ["nombres_hoteles"]

def generar_nombre_hotel_realista(ciudad):
    """Genera un nombre de hotel realista para la ciudad"""
    if ciudad in nombres_hoteles:
        nombre_base = random.choice(nombres_hoteles[ciudad])
        # A veces agregar un sufijo para variación
        if random.random() < 0.3:  # 30% de probabilidad de agregar sufijo
            sufijo = random.choice(sufijos_hoteles)
            # Evitar duplicar palabras
            if sufijo.strip() not in nombre_base:
                return nombre_base + sufijo
        return nombre_base
    else:
        # Fallback para ciudades no listadas
        return f"Hotel {ciudad} {random.choice(['Plaza', 'Real', 'Central', 'del Sol', 'Boutique'])}"
    
# === Función de generación de reseñas ===
def generar_resena(hotel, ciudad, departamento, region, rating, idioma):
    if idioma == "English":
            
        if rating >= 6:
            prompt = (
                f"Write a fully English, positive and realistic review about the hotel {hotel} located in {ciudad}, "
                f"{region} region of Colombia. Mention staff friendliness, cleanliness and comfort."
            )
        else:
            prompt = (
                f"Write a fully English, negative and realistic review about the hotel {hotel} located in {ciudad}, "
                f"{region} region of Colombia. Mention issues such as noise, poor service or cleanliness problems."
            )

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=256)
    if torch.cuda.is_available():
        inputs = {k: v.to("cuda") for k, v in inputs.items()}

    outputs = model.generate(
        **inputs,
        max_new_tokens=120,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7
    )

    reseña = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reseña.strip()

# === Generar dataset ===
data = []
for _ in tqdm(range(num_resenas), desc="Generando reseñas..."):
    region = random.choice(list(regiones.keys()))
    ciudad = random.choice(regiones[region])
    departamento = departamentos[ciudad]
    hotel = generar_nombre_hotel_realista(ciudad)
    rating = round(random.uniform(1, 10), 1)
    idioma = "English"
    traveler_type = random.choice(viajeros)

    # Nombre realista
    if idioma == "English":
        user = fake_en.name()

    reseña = generar_resena(hotel, ciudad, departamento, region, rating, idioma)

    data.append({
        "hotel": hotel,
        "ciudad": ciudad,
        "departamento": departamento,
        "region": region,
        "language": idioma,
        "rating": rating,
        "travelerType": traveler_type,
        "userName": user,
        "resena": reseña
    })

# === Guardar ===
df = pd.DataFrame(data)
df.to_csv("Resenas_Turismo_Colombia_FLAN_Final.csv", index=False, encoding="utf-8-sig", quotechar='"')

print("✅ Archivo generado: Resenas_Turismo_Colombia_FLAN_Final.csv")
print(df.sample(3))





