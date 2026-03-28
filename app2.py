import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

#titulo de la pestaña del navegador
st.set_page_config(page_title="Dashboard del Análisis de Divergencia Cultural en Videojuegos", layout="wide")

#estetica del trabajo, para que parezcan cuadrados con sombra y bordes redondeados
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
st.markdown("### Investigación sobre la validez de la universalidad de videojuegos en el mercado global")
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
    top_n = st.number_input("Ver el Top de juegos:", 5, 50, 10)

#organizacion de los tabs y sus nombres
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Volúmenes de Venta", 
    "🧪 Comparativa Regional", 
    "🚀 Dinámicas de Plataformas", 
    "📂 Validación de Resultados",
    "🔍 Divergencias del Mercado"
])

#tab1, con respecto al primer objetivo de la investigacion
with tab1:
    st.header("1. Cuantificación de Preferencias por Género")
#se divide en 2 columnas para aprovechar el espacio
    col_bar, col_pie = st.columns(2)

#un grafico de barras, eje horzontal generos y vertical las regiones, un colo distinto segun cada variable
    with col_bar:
        fig1 = px.bar(df_filtrado, x="Genre", y=reg_tech, 
                     title=f"Ventas por Género en {region_sel}",
                     color="Genre", template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)

#un grafico circular para ver el peso de cada género
    with col_pie:
        fig_pie = px.pie(df_filtrado, values=reg_tech, names='Genre',
                         title=f"Distribución porcentual en {region_sel}",
                         hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

#tab2, con respecto al segundo objetivo
with tab2:
    st.header("2. Similitud entre Mercados Globales")
    
#grafico de caja que muestra la mediana (la línea del medio) y que tan dispersos están los datos
    st.subheader("Dispersión y Mediana de Ventas")
    fig_box = px.box(df_filtrado, x="Genre", y=reg_tech, color="Genre",
                    title=f"Distribución de éxito por título en {region_sel}",
                    points="outliers", template="plotly_white")
    st.plotly_chart(fig_box, use_container_width=True)
    st.divider()

#titulo del segundo grafico en este mismo tab
    st.subheader("Matriz de Identidad de Consumo")
    
#cambiamos el nombre tecnico por nombres bonitos
    df_corr = df_filtrado[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].rename(columns={
        "NA_Sales": "Norteamérica",
        "EU_Sales": "Europa",
        "JP_Sales": "Japón",
        "Other_Sales": "Otros"
    })
#calculo de la correlación (un número entre 0 y 1)
    corr_matrix = df_corr.corr()

#dibujo del mapa de colores 
    fig_corr = px.imshow(corr_matrix, 
                         text_auto=True, 
                         color_continuous_scale='RdYlGn',
                         title="Correlación entre Mercados (Similitud de gustos)")
    st.plotly_chart(fig_corr, use_container_width=True)

#tab3, con respecto al tercer objetivo de la investigacion
with tab3:
    st.header("3. Estudio de la Distribución de las Plataformas")
    col_plat1, col_plat2 = st.columns(2)

#primera columna 
    with col_plat1:
        st.write("Cuota de mercado por Consola")
#agrupamos los datos, se suman las ventas de la región elegida por cada plataforma
        platform_summary = df_filtrado.groupby("Platform")[reg_tech].sum().reset_index()
#gráfico de dona, se toman solo las 10 mejores para que el gráfico no se amontone
        fig_pie_hw = px.pie(platform_summary.nlargest(10, reg_tech), values=reg_tech, names="Platform", 
                            hole=0.5, title="Top 10 Consolas Dominantes")
        st.plotly_chart(fig_pie_hw, use_container_width=True)

#segunda columna
    with col_plat2:
        st.write("Ventas por Consola y Género")
#se agrupan por plataforma y género para ver la combinación de ambos
        df_plat = df_filtrado.groupby(['Platform', 'Genre'])[reg_tech].sum().reset_index()
#solo nos quedamos con las 10 plataformas que más venden en total
        top_platforms = df_plat.groupby('Platform')[reg_tech].sum().nlargest(10).index
        df_plat_top = df_plat[df_plat['Platform'].isin(top_platforms)]

#gráfico de barras agrupadas
        fig_plat = px.bar(df_plat_top, x="Platform", y=reg_tech, color="Genre", barmode="group",
                         title=f"Especialización de Hardware en {region_sel}", template="plotly_white")
        st.plotly_chart(fig_plat, use_container_width=True)

#tab4, muestra el exito segun la data
with tab4:
    st.header("4. Evidencia de Éxito Comercial")
#el dataframe filtrado en orden para poner los juegos más vendidos arriba
    df_top = df_filtrado.sort_values(by=reg_tech, ascending=False).head(top_n)
#se muestra la tabla interactiva en la pantalla
    st.dataframe(df_top[['Name', 'Platform', 'Genre', reg_tech]], hide_index=True, use_container_width=True)