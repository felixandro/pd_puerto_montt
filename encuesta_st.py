import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Imagen de fondo (usa tu propia URL o archivo local codificado en base64)
background_url = "https://storage.googleapis.com/chile-travel-cdn/2021/07/puerto-montt_prin-min.jpg"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{background_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-color: rgba(255,255,255,0.8);
    }}
    </style>
""", unsafe_allow_html=True)


st.title("Encuesta")

# Variables para controlar tamaño de letra y transparencia
alpha = 0.9  # Transparencia del fondo (0 a 1)
font_size_header = "30px"  # Tamaño letra encabezados
font_size_cells = "18px"   # Tamaño letra celdas

# Datos
index = ["Costo", "Tiempo de Viaje", "Tiempo de Caminata", "Tiempo de Espera", "Transbordo"]
opcion_a = [1000, 30, 5, 9, 0]
opcion_b = [2000, 20, 8, 12, 1]

# Estilos con variables CSS
estilos = f"""
<style>
table, th, td {{
  border: 1px solid #ddd;
  text-align: center;
  padding: 6px;
  border-collapse: collapse;
  width: 100%;
}}

th {{
  background-color: rgba(255, 255, 255, {alpha});
  font-size: {font_size_header};
  font-weight: bold;
}}

td {{
  background-color: rgba(255, 255, 255, {alpha});
  font-size: {font_size_cells};
}}
</style>
"""

# Tabla índice
tabla_idx = estilos + '<table><tr><th>Criterio</th></tr>'
for item in index:
    tabla_idx += f"<tr><td>{item}</td></tr>"
tabla_idx += "</table>"

# Tabla opción A
tabla_a = '<table><tr><th>Opción A</th></tr>'
for val in opcion_a:
    tabla_a += f"<tr><td>{val}</td></tr>"
tabla_a += "</table>"

# Tabla opción B
tabla_b = '<table><tr><th>Opción B</th></tr>'
for val in opcion_b:
    tabla_b += f"<tr><td>{val}</td></tr>"
tabla_b += "</table>"

# Mostrar en columnas
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown(tabla_idx, unsafe_allow_html=True)

with col2:
    st.markdown(tabla_a, unsafe_allow_html=True)
    if st.button("Elegir A", use_container_width=True):
        st.success("Elegiste Opción A")

with col3:
    st.markdown(tabla_b, unsafe_allow_html=True)
    if st.button("Elegir B", use_container_width=True):
        st.success("Elegiste Opción B")
