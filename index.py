import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Dashboard Avanzado de Precios de Viviendas",
    page_icon="🏠",
    layout="wide"
)

# --- TÍTULO PRINCIPAL ---
st.title("🏠 Dashboard Avanzado de Precios de Viviendas")
st.markdown("Un análisis interactivo del mercado inmobiliario en King County, WA.")

# --- BARRA LATERAL (SIDEBAR) CON FILTROS ---
with st.sidebar:
    st.header("Filtros de Búsqueda 🔎")

    # Filtro por ciudad
    cities = sorted(df['city'].unique())
    selected_cities = st.multiselect(
        "Selecciona Ciudades:",
        options=cities,
        default=["Seattle", "Bellevue", "Redmond", "Renton"]
    )
