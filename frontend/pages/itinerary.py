import streamlit as st
from services.db_query import obtener_foto_atraccion


def render_itinerary():
    st.subheader("Itinerario generado")

    if not st.session_state.get("plan"):
        st.info("Genera un plan desde la pestaña Home.")
        return

    plan = st.session_state.plan
    days = plan.get("days", [])

    for d in days:
        st.markdown(f"## Día {d['day']} — {d['city']}")

        col_text, col_img = st.columns([1.2, 1])
        slots = d["slots"]

        with col_text:
            st.subheader(f"☀ Mañana – {slots['morning']['activity']}")
            st.write(slots["morning"].get("description", ""))

            st.subheader(f"🌤 Tarde – {slots['afternoon']['activity']}")
            st.write(slots["afternoon"].get("description", ""))

            st.subheader(f"🌙 Noche – {slots['evening']['activity']}")
            st.write(slots["evening"].get("description", ""))

        with col_img:
            st.markdown("### 📸 Atracciones")

            for icon, slot in zip(
                ["☀", "🌤", "🌙"],
                ["morning", "afternoon", "evening"]
            ):
                actividad = slots[slot]["activity"]
                st.caption(f"{icon} {actividad}")

                img = obtener_foto_atraccion(
                    actividad,
                    st.session_state.city
                )

                if img:
                    st.image(img, width=200)
                else:
                    st.caption("Imagen no disponible")

        st.markdown("---")