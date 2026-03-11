import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Mi Dashboard", layout="wide")

st.title('Análisis de Datos con Streamlit')
st.write('Entorno configurado exitosamente en GitHub Codespaces.')

# Generación de datos de prueba
datos = pd.DataFrame(
    np.random.randn(50, 3),
    columns=['Variable X', 'Variable Y', 'Variable Z']
)

# Visualización rápida
st.subheader('Tendencias Simuladas')
st.line_chart(datos)