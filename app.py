import streamlit as st
from state.session import init_session
from pages.home import render_home
from pages.reviews import render_reviews
from pages.itinerary import render_itinerary

st.set_page_config(page_title="TrueTrip Colombia", layout="wide")
init_session()

tab1, tab2, tab3 = st.tabs(["Home", "Reseñas", "Itinerario"])

with tab1:
    render_home()

with tab2:
    render_reviews()

with tab3:
    render_itinerary()
