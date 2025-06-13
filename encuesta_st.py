import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")

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

import streamlit as st

# Variables de estilo
alpha = 0.1  # Transparencia del fondo
font_size_header = "18px"
font_size_cells = "14px"

# Datos
index = ["Costo", "Tiempo de Viaje", "Tiempo de Caminata", "Tiempo de Espera", "Transbordo"]
opcion_a = [1000, 30, 5, 9, 0]
opcion_b = [2000, 20, 8, 12, 1]

# Estilo CSS actualizado: ancho 100%
estilo_tabla = f"""
<style>
table {{
  border-collapse: collapse;
  width: 100%;
}}

th, td {{
  border: 1px solid #ddd;
  padding: 6px 12px;
  text-align: center;
}}

th {{
  background-color: rgba(255, 255, 255, {alpha});
  font-size: {font_size_header};
}}

td {{
  background-color: rgba(255, 255, 255, {alpha});
  font-size: {font_size_cells};
}}
</style>
"""

# Construcción de la tabla HTML
tabla_html = estilo_tabla + "<table>"
tabla_html += "<tr><th>Criterio</th><th>Opción A</th><th>Opción B</th></tr>"

for i in range(len(index)):
    tabla_html += f"<tr><td>{index[i]}</td><td>{opcion_a[i]}</td><td>{opcion_b[i]}</td></tr>"

tabla_html += "</table>"

# Mostrar tabla en Streamlit
st.markdown(tabla_html, unsafe_allow_html=True)

# Botones de elección
col_criterio, col_a, col_b = st.columns(3)
with col_a:
    if st.button("Elegir A", use_container_width=True):
        st.success("Elegiste Opción A")
with col_b:
    if st.button("Elegir B", use_container_width=True):
        st.success("Elegiste Opción B")

