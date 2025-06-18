import streamlit as st
from supabase import create_client

def agregar_imagen_fondo(url):
    """
    Agrega una imagen de fondo a la aplicación Streamlit.
    
    Args:
        url (str): URL de la imagen de fondo.
    """
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("{url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-color: rgba(255,255,255,0.8);
        }}
        </style>
    """, unsafe_allow_html=True)

def definir_nro_disenho(lugar, modo_par):
    """
    Define el número de diseño de la encuesta.
    
    Returns:
        int: Número de diseño.
    """

    if lugar == "Centro":
        if modo_par == "Manuel Montt - Centro":
            return 1
        elif modo_par == "Mirasol - Centro":
            return 4
        elif modo_par == "Alerce - Centro":
            return 7
    elif lugar == "Manuel Montt":
        if modo_par == "Taxibus":
            return 2
        elif modo_par == "Taxi Colectivo":
            return 3
    elif lugar == "Mirasol":
        if modo_par == "Taxibus":
            return 5
        elif modo_par == "Taxi Colectivo":
            return 6
    elif lugar == "Alerce":
        if modo_par == "Taxibus":
            return 8
        elif modo_par == "Taxi Colectivo":
            return 9
        elif modo_par == "Tren":
            return 10

def perfil_eleccion(niveles_a, niveles_b):
    # Variables de estilo
    alpha = 0.95
    font_size_header = "18px"
    font_size_cells = "16px"

    # Datos
    index = ["Costo", "Minutos de Viaje", "Minutos de Espera", "Minutos de Caminata", "Transbordos"]

    # Estilo CSS
    estilo_tabla = f"""
    <style>
    table {{
        border-collapse: collapse;
        width: 100%;
        table-layout: fixed;
    }}
    td {{
        border: 1px solid #ddd;
        padding: 6px 12px;
        text-align: center;
        vertical-align: middle;
        font-size: {font_size_cells};
    }}
    /* Estilo fila encabezado (primera fila) */
    tr:first-child td {{
        background-color: rgba(255, 255, 255, {alpha});
        font-size: {font_size_header};
        font-weight: bold;
    }}
    /* Anchos fijos columnas */
    tr:first-child td:nth-child(1),
    td:nth-child(1) {{
        width: 30%;
    }}
    tr:first-child td:nth-child(2),
    td:nth-child(2) {{
        width: 35%;
    }}
    tr:first-child td:nth-child(3),
    td:nth-child(3) {{
        width: 35%;
    }}
    /* Estilo primera columna */
    td.col-criterio {{
        color: black;
        font-weight: 600;
        background-color: rgba(255, 255, 255, {alpha});
    }}
    /* Estilo segunda columna (rojo) */
    td.col-a {{
        color: red;
        font-weight: bold;
        background-color: rgba(255, 255, 255, {alpha});
    }}
    /* Estilo tercera columna (azul) */
    td.col-b {{
        color: blue;
        font-weight: bold;
        background-color: rgba(255, 255, 255, {alpha});
    }}
    /* Filas pares con gris suave */
    tr:nth-child(even) td {{
        background-color: #f5f5f5;
    }}
    </style>
    """

    # Construcción de la tabla HTML
    tabla_html = estilo_tabla + "<table>"

    modo_a = niveles_a[0]
    modo_b = niveles_b[0]

    emojis_dict = {
        "Auto": "🚗",
        "Teleférico": "🚡",
        "Taxi Colectivo": "🚕",
        "Taxibus": "🚌",
        "Tren": "🚆",
        "Taxibus - Teleférico": "🚌🚡",
        "Taxibus - Tren - Taxibus": "🚌🚆🚌"
    }

    # Fila encabezado como primera fila con <td>
    tabla_html += (
        f"<tr>"
        f"<td class='col-criterio'>Criterio</td>"
        f"<td class='col-a'>{niveles_a[0]} {emojis_dict[modo_a]} </td>"
        f"<td class='col-b'>{niveles_b[0]} {emojis_dict[modo_b]}</td>"
        f"</tr>"
    )

    # Filas de datos
    for i in range(len(index)):
        if i == 0:
            # Formatear los valores de costo con separador de miles y signo $
            niv_a = f"${niveles_a[i+1]:,}".replace(",", ".")
            niv_b = f"${niveles_b[i+1]:,}".replace(",", ".")
        else:
            niv_a = niveles_a[i+1]
            niv_b = niveles_b[i+1]
        tabla_html += (
            f"<tr>"
            f"<td class='col-criterio'>{index[i]}</td>"
            f"<td class='col-a'>{niv_a}</td>"
            f"<td class='col-b'>{niv_b}</td>"
            f"</tr>"
        )

    tabla_html += "</table>"

    # Mostrar en Streamlit
    st.markdown(tabla_html, unsafe_allow_html=True)



def texto_con_fondo_v0(texto, 
                    upper_margin="1rem", 
                    bg_color="rgba(255, 255, 255, 0.95)",
                    text_color="#000000"):
    padding="0.8rem"
    font_size="18px"
    bold=True
    centrar=True
    margen=f"0 0 {upper_margin} 0"  # margen inferior de 2rem
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

def texto_con_fondo(texto, 
                    upper_margin="1rem", 
                    bg_color="rgba(255, 255, 255, 0.95)",
                    text_color="#000000"):
    padding = "0.8rem"
    font_size = "18px"
    bold = True
    centrar = True
    margen = f"0 0 {upper_margin} 0"
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
        word-wrap: break-word;
        overflow-wrap: break-word;
    ">
        {texto}
    </div>
    """, unsafe_allow_html=True)



def guardar_respuestas(respuestas):

    print("Guardando respuestas:", respuestas)

    # Configurar Supabase
    SUPABASE_URL = "https://gkgxipnjsoxgqsaukhtg.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdrZ3hpcG5qc294Z3FzYXVraHRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAxMTI1NjEsImV4cCI6MjA2NTY4ODU2MX0.TNyYDvpLhBX-Ocr03jzdo9GulXYfYMmOh0Vx20hlJfg"
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    print("hola")

    response = supabase.table("bbdd_pd").insert(respuestas).execute()

    print("sdadsa")

def guardar_ingresos(ingresos):
    """
    Guarda los ingresos del usuario en la base de datos.
    
    Args:
        ingresos (dict): Diccionario con los datos de ingresos del usuario.
    """
    SUPABASE_URL = "https://gkgxipnjsoxgqsaukhtg.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdrZ3hpcG5qc294Z3FzYXVraHRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAxMTI1NjEsImV4cCI6MjA2NTY4ODU2MX0.TNyYDvpLhBX-Ocr03jzdo9GulXYfYMmOh0Vx20hlJfg"
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    response = supabase.table("ingresos").insert(ingresos).execute()