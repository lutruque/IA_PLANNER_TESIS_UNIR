import streamlit as st
from services.api_client import generar_itinerario, enviar_itinerario
from services.db_query import obtener_ciudades


def render_home():
    st.subheader("Planifica tu viaje con TrueTrip")

    col1, col2 = st.columns([1.2, 1.8])

    with col1:
        st.subheader("Región")
        st.session_state.region = st.selectbox(
            "Seleccione",
            ["Andina", "Caribe", "Eje Cafetero"]
        )

        st.subheader("Ciudad")
        ciudades = obtener_ciudades()
        st.session_state.city = st.selectbox(
            "Seleccione la ciudad",
            ciudades
        )

        st.subheader("Tipo de turismo")
        st.session_state.profile = st.selectbox(
            "Perfil",
            [
                "Pareja", "Viajero solo", "Familia",
                "Grupo de amigos", "Luna de miel", "Viaje de trabajo"
            ]
        )

        st.subheader("Duración del viaje")
        st.session_state.days = st.number_input(
            "Número de días",
            min_value=1,
            max_value=30,
            value=3
        )

        # -----------------------------
        # Envío por correo
        # -----------------------------
        st.markdown("### Envío por correo")
        enviar = st.radio(
            "¿Desea enviar el itinerario por correo?",
            ["No", "Sí"],
            horizontal=True
        )

        if enviar == "Sí":
            st.session_state.correo_destino = st.text_input(
                "Correo electrónico",
                placeholder="ejemplo@correo.com"
            )

        if st.button("✈ Crear mi plan", type="primary"):
            try:
                plan = generar_itinerario(
                    region=st.session_state.region,
                    days=st.session_state.days,
                    profile=st.session_state.profile,
                    city=st.session_state.city
                )

                st.session_state.plan = plan
                st.session_state.generate_plan = True
                st.success("Itinerario generado correctamente")

                if enviar == "Sí" and st.session_state.correo_destino:
                    payload = {
                        **plan,
                        "to_email": st.session_state.correo_destino,
                        "subject": f"Tu itinerario turístico {st.session_state.city}"
                    }
                    enviar_itinerario(payload)
                    st.success("Itinerario enviado por correo")

            except Exception as e:
                st.error("Error al generar el itinerario")
                st.exception(e)

    with col2:
        st.image("mapa.jpg", use_container_width=True)

