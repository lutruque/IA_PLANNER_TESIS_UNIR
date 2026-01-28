import folium
import streamlit.components.v1 as components

def render_map(lat, lon, city):
    m = folium.Map(location=[lat, lon], zoom_start=12)
    folium.Marker([lat, lon], popup=city).add_to(m)
    components.html(m._repr_html_(), height=500)
