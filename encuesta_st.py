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
alpha = 0.9  # Transparencia del fondo
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

def texto_con_fondo(
    texto,
    bg_color="rgba(255, 255, 255, 0.95)",
    padding="0.8rem",
    font_size="18px",
    bold=True,
    text_color="#000000",
    centrar=True,
    margen="0 0 2rem 0"  # margen inferior de 2rem
):
    weight = "bold" if bold else "normal"
    alineacion = "center" if centrar else "left"
    
    st.markdown(f"""
    <div style="
        background-color: {bg_color};
        padding: {padding};
        margin: {margen};
        border-radius: 8px;
        font-size: {font_size};
        font-weight: {weight};
        color: {text_color};
        text-align: {alineacion};
    ">
        {texto}
    </div>
    """, unsafe_allow_html=True)



texto_con_fondo(
    "¿Cuál Elegiría?")

button_a = st.button("Elijo A", use_container_width= True)
button_b = st.button("Elijo B", use_container_width= True)
