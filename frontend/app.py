import streamlit as st
from components.header import render_header
from state.session import init_session
from pages.home import home_tab
from pages.reviews import reviews_tab
from pages.itinerary import itinerary_tab

st.set_page_config(page_title="TrueTrip UI", layout="wide")

init_session()
render_header()

tab1, tab2, tab3 = st.tabs(["Home", "Reseñas", "Itinerario"])

with tab1:
    home_tab()

with tab2:
    reviews_tab()

with tab3:
    itinerary_tab()
