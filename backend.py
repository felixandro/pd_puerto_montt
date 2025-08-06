import streamlit as st
from supabase import create_client
from datetime import datetime
import json

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
        "Taxibus - Tren - Taxibus": "🚌🚆🚌",
        "Alternativa 1": "",
        "Alternativa 2": ""
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

    response = supabase.table("bbdd_pd_v2").insert(respuestas).execute()

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

    response = supabase.table("ingresos_v2").insert(ingresos).execute()

def generar_encuestadores_dict(encuestadores_df):
    encuestadores_dict = {}
    for index, row in encuestadores_df.iterrows():
        encuestador = row['Encuestador']
        lugar = row['Lugar']
        if lugar not in encuestadores_dict:
            encuestadores_dict[lugar] = []
        encuestadores_dict[lugar].append(encuestador)
    return encuestadores_dict

def generar_tiempos_dict(horas_list):

    tiempos_dict = {}
    t_labels = ["t_caract", "t_intro", "t_pd1", "t_pd2", "t_pd3", "t_pd4", "t_pd5", "t_ing"]

    for i, hora in enumerate(horas_list[:-1]):
        
        next_hora = horas_list[i + 1]

        datetime_hora = datetime.strptime(hora, "%Y-%m-%d %H:%M:%S")
        datetime_next_hora = datetime.strptime(next_hora, "%Y-%m-%d %H:%M:%S")

        diferencia = datetime_next_hora - datetime_hora
        segundos = int(diferencia.total_seconds())

        assert segundos >= 0, f"Error: La diferencia de tiempo entre {hora} y {next_hora} es negativa."

        tiempos_dict[t_labels[i]] = segundos

    return tiempos_dict

def definir_lista_tarjetas(nro_disenho, nro_bloque):
    """
    Define la lista de tarjetas según el número de diseño.
    
    Args:
        nro_disenho (int): Número de diseño.
    
    Returns:
        list: Lista de tarjetas.
    """

    with open(f'Disenhos/disenho_{nro_disenho}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    lista_tarjetas = []

    for i in range(1,len(data)-3):
        bloque = data[f"T{i}"]["Bloque"]
        if bloque == nro_bloque or bloque == 0:
            lista_tarjetas.append(i)

    return lista_tarjetas

def generar_id_respuesta(hora_id, nro_disenho, nro_tarjeta, id_encuestador, edad, genero, proposito):

    # Extraer componentes de fecha y hora de hora_id
    dt = datetime.strptime(hora_id[:19], "%Y-%m-%d %H:%M:%S")
    hora_id_fmt = f"{dt.month:02d}{dt.day:02d}{dt.hour:02d}{dt.minute:02d}{dt.second:02d}"

    # Formatear nro_disenho
    nro_disenho_fmt = f"{nro_disenho:02d}"

    # Formatear id_encuestador: tomar las dos primeras letras de cada palabra
    id_encuestador_fmt = ''.join([w[:3] for w in id_encuestador.split()])

    return f"{hora_id_fmt}_{nro_disenho_fmt}_{nro_tarjeta}_{id_encuestador_fmt}_{edad}_{genero[0]}_{proposito[0]}"


def generar_id_encuesta(hora_id, nro_disenho, id_encuestador, edad, genero, proposito):

    # Extraer componentes de fecha y hora de hora_id
    dt = datetime.strptime(hora_id[:19], "%Y-%m-%d %H:%M:%S")
    hora_id_fmt = f"{dt.month:02d}{dt.day:02d}{dt.hour:02d}{dt.minute:02d}{dt.second:02d}"

    # Formatear nro_disenho
    nro_disenho_fmt = f"{nro_disenho:02d}"

    # Formatear id_encuestador: tomar las dos primeras letras de cada palabra
    id_encuestador_fmt = ''.join([w[:3] for w in id_encuestador.split()])

    return f"{hora_id_fmt}_{nro_disenho_fmt}_{id_encuestador_fmt}_{edad}_{genero[0]}_{proposito[0]}"
