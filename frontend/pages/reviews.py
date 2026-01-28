import streamlit as st


def _separar_resenas(texto: str):
    if not texto:
        return []
    texto = texto.replace("Estas son las reseñas mejor calificadas:", "").strip()
    return [t.strip() for t in texto.split("-") if t.strip()]


def render_reviews():
    st.subheader("Reseñas del destino")

    if not st.session_state.get("plan"):
        st.info("Primero genera un itinerario desde la pestaña Home.")
        return

    plan = st.session_state.plan
    summary = plan.get("summary", {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 🏨 Hoteles")
        resenas = _separar_resenas(summary.get("review_summary_hotels"))
        if not resenas:
            st.info("No hay reseñas disponibles.")
        for r in resenas:
            st.write(r)
            st.markdown("---")

    with col2:
        st.markdown("## 📍 Atracciones")
        resenas = _separar_resenas(summary.get("review_summary_attractions"))
        if not resenas:
            st.info("No hay reseñas disponibles.")
        for r in resenas:
            st.write(r)
            st.markdown("---")
