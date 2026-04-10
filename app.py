import streamlit as st
import pandas as pd
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

#diccionario para poner tdo en español
labels_es = {
    "Genre": "Género",
    "Platform": "Plataforma",
    "NA_Sales": "Ventas Norteamérica",
    "EU_Sales": "Ventas Europa",
    "JP_Sales": "Ventas Japón",
    "Other_Sales": "Otras Ventas",
    "Global_Sales": "Ventas Globales",
    "Indice_Regionalismo": "Índice de Regionalismo (%)",
    "Name": "Nombre del Juego"
}

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
st.markdown("### Estudio estadístico sobre la variabilidad del consumo de videojuegos en los mercados regionales y en el mercado global")
st.divider()

#orden por columnas para mostrar un resumen estadístico sobre los datos filtrados
col1, col2 = st.columns(2)
with col1:
    st.metric("Ventas Totales (Región)", f"{df_filtrado[reg_tech].sum():.2f}M")
#calculo de la diferencia del rendimiento actual respecto al promedio global de la región elegida
with col2:
    avg_global = df_base[reg_tech].mean()
    avg_sel = df_filtrado[reg_tech].mean() if not df_filtrado.empty else 0
    st.metric("Rendimiento Promedio", f"{avg_sel:.2f}M", delta=f"{avg_sel - avg_global:.2f}M vs Global")

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

#columnas de separacion
    col_bar, col_tree = st.columns(2)

#grafico de barras en la primera columna
    with col_bar:
        st.write("### Ventas por Género") # Un título pequeño para la columna
        fig1 = px.bar(df_filtrado, x="Genre", y=reg_tech, 
                     color="Genre", template="plotly_white",
                     labels=labels_es)
        
#se ajustan los margenes para que no haya espcio desperdiciado
        fig1.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=400)
        st.plotly_chart(fig1, use_container_width=True)

#grafico de ramas o arbol
    with col_tree:
        st.write("### Ecosistema de la Región") 
        if not df_filtrado.empty:
            fig_tree_gen = px.treemap(df_filtrado, 
                                     path=['Genre'], 
                                     values=reg_tech,
                                     color='Genre',
                                     template="plotly_white",
                                     labels=labels_es)
            
            fig_tree_gen.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=400)
            fig_tree_gen.update_traces(textinfo="label+percent entry")
            
            st.plotly_chart(fig_tree_gen, use_container_width=True)

#informacion/comentario de la grafica
    st.info("**Interpretación**: Las barras muestran volumen total, mientras que el mapa de cuadros permite visualizar la relevancia relativa de cada género.")

#tab2, con respecto al segundo objetivo
with tab2:
    st.header("2. Similitud entre Mercados Globales")
    
    st.subheader("Dispersión y Mediana de Ventas")
#calculo del valor que deja por debajo al 95% de los datos en la región actual, así eliminando los outliers que aplastan el gráfico
    limite_95 = df_filtrado[reg_tech].quantile(0.95)
#filtro de la data para el grafico de caja, asi usando ese límite
    df_box = df_filtrado[df_filtrado[reg_tech] <= limite_95].copy()

#el graico con la data optimizada
    fig_box = px.box(df_box, 
                    x="Genre", 
                    y=reg_tech, 
                    color="Genre",
                    title=f"Distribución del 95% del Mercado en {region_sel}",
                    points=False, #quita los puntos y hace que las cajas se vean mas grandes
                    template="plotly_white", labels=labels_es)
    
#para que el eje Y no deje espacio en blanco innecesario
    fig_box.update_layout(yaxis_range=[0, limite_95 * 1.05])
    
    st.plotly_chart(fig_box, use_container_width=True)

#informacion/comentario de la grafica
    st.info(""" 
**Si la caja es pequeña**: Significa que la mayoría de los juegos de ese género venden cantidades parecidas en la región. El éxito es más estable.
**Si la caja es grande**: Significa que hay mucha diferencia entre los juegos. Algunos venden poco y otros muchísimo, siendo un mercado más variado.
""")

#espacio entre las graficas
    st.divider()

    st.header("2. Composición Relativa del Mercado")
    
#dataframe que vuelve las ventas a porcentajes
    df_prop = df_filtrado.groupby('Genre')[reg_tech].sum().reset_index()
    total_ventas = df_prop[reg_tech].sum()
    df_prop['% del Mercado'] = (df_prop[reg_tech] / total_ventas * 100).round(2)

#gráfico de barras horizontal 
    fig_prop = px.bar(df_prop, 
                      y="Genre", 
                      x="% del Mercado", 
                      orientation='h',
                      title=f"Cuota de Mercado por Género en {region_sel}",
                      text="% del Mercado",
                      color="Genre",
                      template="plotly_white",
                      labels=labels_es)

#el símbolo de % y quitamos líneas
    fig_prop.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_prop.update_layout(xaxis_ticksuffix="%", xaxis_range=[0, 100])
#simplificacion estetica de los ejes
    fig_prop.update_xaxes(showgrid=False)
    fig_prop.update_yaxes(showgrid=False)

    st.plotly_chart(fig_prop, use_container_width=True)

#informacion/comentario de la grafica
    st.info("**Análisis de Proporción**: Se muestra que domina cada género. Esto permite comparar regiones de distintos tamaños bajo la misma escala.")

#tab3, con respecto al tercer objetivo de la investigacion
with tab3:
    st.header("3. Dinámicas de Consumo por Plataforma")
    
    if not df_filtrado.empty:
#preparacion de los datos
        df_plat_vol = df_filtrado.groupby("Platform")[reg_tech].sum().reset_index()
        df_plat_vol = df_plat_vol.nlargest(10, reg_tech) #top 10 consolas por ventas

#grafico de piramide, enfocada en el volumen 
        st.write("### Jerarquía de Hardware")
        fig_piramide = px.funnel(df_plat_vol, 
                                 x=reg_tech, 
                                 y="Platform",
                                 color="Platform",
                                 title=f"Ventas Totales por Consola en {region_sel}",
                                 template="plotly_white",
                                 labels=labels_es)
        
#para que muestre el valor en millones (M)
        fig_piramide.update_traces(
            texttemplate="%{value:.2f}M", 
            textposition="inside"
        )
        fig_piramide.update_layout(showlegend=False)
        st.plotly_chart(fig_piramide, use_container_width=True)
        st.info("**Análisis de Magnitud**: La pirámide muestra el volumen de ventas acumulado. Es la métrica directa de éxito comercial en la región.")

        st.divider() #línea para separar los dos análisis

#grafico de barras aplidadas, enfacada en el porcentaje
        st.write("### Especialización (Porcentual)")
#preparacion de datos
        df_stack = df_filtrado.groupby(['Platform', 'Genre'])[reg_tech].sum().reset_index()
        top_10_plats = df_plat_vol['Platform'].tolist()
        df_stack = df_stack[df_stack['Platform'].isin(top_10_plats)]

        fig_stack = px.bar(df_stack, 
                           x=reg_tech, 
                           y="Platform", 
                           color="Genre",
                           title="Composición de Géneros por Consola",
                           orientation='h',
                           template="plotly_white",
                           labels=labels_es)
    
#la normalización al 100%
        fig_stack.update_layout(barmode='stack', barnorm='percent') 
        fig_stack.update_layout(xaxis_ticksuffix="%", showlegend=True)
        fig_stack.update_xaxes(title="Porcentaje de las ventas")
    
        st.plotly_chart(fig_stack, use_container_width=True)
        st.info("**Interpretación**: Aquí comparamos el 'ADN' de cada consola. Si una barra tiene un color predominante, significa que esa plataforma se especializa en ese género.")

#tab4, muestra el exito segun la data
with tab4:
    st.header("4. Evidencia de Éxito Comercial")
#para que el usuario controle la cantidad que quiere ver de la tabla
    top_n = st.number_input("Ver el Top de juegos:", 5, 50, 10, key="top_tab4")
#el dataframe filtrado en orden para poner los juegos más vendidos arriba
    df_top = df_filtrado.sort_values(by=reg_tech, ascending=False).head(top_n)
#se muestra la tabla interactiva en la pantalla
    st.dataframe(df_top[['Name', 'Platform', 'Genre', reg_tech]], hide_index=True, use_container_width=True)

#tab5, para analizar datos fuera de lo comun
with tab5:
    st.header("5. Éxitos Regionales vs Fracasos Globales")

    if region_sel == "Ventas Globales":
        st.warning("⚠️ El análisis de regionalismo no aplica para Ventas Globales.")
    else:
#seleccionamos juegos con ventas representativas (>0.3M)
        threshold = 0.3 
        df_outliers = df_filtrado[df_filtrado[reg_tech] > threshold].copy()
        
#calculo del peso relativo de la región sobre el total global
        df_outliers['Indice_Regionalismo'] = (df_outliers[reg_tech] / df_outliers['Global_Sales']) * 100
        top_3_outliers = df_outliers.sort_values(by='Indice_Regionalismo', ascending=False).head(3)

#visualizacion de la dispersión de la divergencia cultural y casos de exito local
        col_out_graf, col_out_cards = st.columns([2, 1])
        with col_out_graf:
            fig_out = px.scatter(df_outliers, x=reg_tech, y="Global_Sales", size="Global_Sales", 
                                 hover_name="Name", color="Indice_Regionalismo",
                                 title=f"Divergencia en {region_sel}", color_continuous_scale="OrRd", labels=labels_es)
            st.plotly_chart(fig_out, use_container_width=True)

        with col_out_cards:
            st.subheader("Top 3 Local")
            for i, row in top_3_outliers.iterrows():
                st.markdown(f"""
                <div style="border: 1px solid #FF4B4B; padding: 10px; border-radius: 10px; margin-bottom: 10px; background-color: #FFF5F5;">
                    <h4 style="margin:0; color: #FF4B4B;">{row['Name']}</h4>
                    <p style="margin:0; font-size: 14px;"><b>Plataforma:</b> {row['Platform']}</p>
                    <p style="margin:0; font-size: 18px;"><b>{row['Indice_Regionalismo']:.1f}%</b> de sus ventas son locales</p>
                </div>
                """, unsafe_allow_html=True)

        st.info("**Interpretacion:** Punto Grande: Dominancia regional (un gigante local). Punto Pequeño: Identidad regional (un tesoro local).")
#espacio para verificar o demostrar lo que esta en el grafico
        st.divider() 
        with st.expander("🔍 Verificación técnica de los cálculos"):
            
#la tabla con los datos crudos para comparar
            df_audit = top_3_outliers[['Name', reg_tech, 'Global_Sales', 'Indice_Regionalismo']]
            st.dataframe(df_audit.style.format({
                reg_tech: "{:.2f}M",
                "Global_Sales": "{:.2f}M",
                "Indice_Regionalismo": "{:.2f}%"
            }), use_container_width=True)