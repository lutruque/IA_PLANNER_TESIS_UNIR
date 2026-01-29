from transformers import pipeline
from app.utils.text_utils import clean_one_line

summarizer = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    max_length=220
)

def summarize_with_llm(city, traveler_type, reviews):
    system_prompt = (
        "Eres un asistente turístico. Resume reseñas de hoteles "
        "de forma breve, en español, sin repetir frases."
    )

    user_prompt = (
        f"Ciudad: {city}\n"
        f"Tipo de viajero: {traveler_type or 'general'}\n\n"
        "Reseñas:\n" +
        "\n".join(f"- {r}" for r in reviews) +
        "\n\nTarea: genera un resumen interpretativo en 3 a 5 viñetas."
    )

    out = summarizer(user_prompt)[0]["generated_text"]
    return clean_one_line(out)
