import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

#titulo de la pestaña del navegador
st.set_page_config(page_title="Dashboard del Análisis de Divergencia Cultural en Videojuegos", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #edf2f7;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff;
        border-radius: 5px 5px 0px 0px;
    }
    </style>
    """, unsafe_allow_html=True)

#carga de los datos
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset/12. Videogame_Sales_Limpio.csv")
    df = df.drop(columns=["Unnamed: 0"], errors="ignore")
    return df

df_base = load_data()

#sección que dinamiza la particpacion del usurio desde su entrada
st.sidebar.header("🕹️ Variables de Investigación")

#para que al usuario pueda comparar los generos y los primeros 5 como predeterminados
generos = st.sidebar.multiselect(
    "Selecciona los géneros:",
    options=df_base["Genre"].unique(),
    default=df_base["Genre"].unique()[:5]
)

#para que el usuario elige un nombre de la region que quiere ver
region_sel = st.sidebar.radio(
    "Región de análisis:",
    options=["Norteamérica", "Europa", "Japón", "Otros", "Ventas Globales"]
)

dict_regiones = {
    "Norteamérica": "NA_Sales", "Europa": "EU_Sales", 
    "Japón": "JP_Sales", "Otros": "Other_Sales", "Ventas Globales": "Global_Sales"
}
reg_tech = dict_regiones[region_sel]

#un filtrado dinámico donde se crea un nuevo dataframe
df_filtrado = df_base[df_base["Genre"].isin(generos)]

#titulo y subtitulo en la pagina
st.title("📊 Análisis de Divergencia Cultural en Videojuegos")
st.markdown("### Investigación sobre la validez de la universalidad en el mercado global")
st.divider()

#orden por columnas para mostrar un resumen estadístico sobre los datos filtrados
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Ventas Totales (Región)", f"{df_filtrado[reg_tech].sum():.2f}M")
#calculo de la diferencia del rendimiento actual respecto al promedio global de la región elegida
with col2:
    avg_global = df_base[reg_tech].mean()
    avg_sel = df_filtrado[reg_tech].mean() if not df_filtrado.empty else 0
    st.metric("Rendimiento Promedio", f"{avg_sel:.2f}M", delta=f"{avg_sel - avg_global:.2f}M vs Global")
#para que el usuario controle la cantidad que quiere ver de la tabla
with col3:
    top_n = st.number_input("Ver Top N juegos:", 5, 50, 10)