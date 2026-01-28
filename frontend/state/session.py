import streamlit as st

def init_session():
    defaults = {
        "menu_open": False,
        "generate_plan": False,
        "region": None,
        "profile": None,
        "city": None,
        "days": None,
        "plan": None,
        "tab_to_show": "Tab1",
        "enviar_correo": "No",
        "correo_destino": ""
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

