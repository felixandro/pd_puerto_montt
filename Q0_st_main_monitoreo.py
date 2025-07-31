import streamlit as st
import pandas as pd
from backend import generar_encuestadores_dict
from backend_monitoreo import cargar_bbdd
from random import choice
import json
import time
import textwrap
import matplotlib.pyplot as plt


# Variables de Estado de la Sesión

if "hora_id" not in st.session_state:
    st.session_state.hora_id = time.strftime("%Y-%m-%d %H:%M:%S")

if "id_encuestador" not in st.session_state:
    st.session_state.id_encuestador = False

if "texto_introductorio" not in st.session_state:
    st.session_state.texto_introductorio = False

if "caracteristicas" not in st.session_state:
    st.session_state.caracteristicas = False

if "perfiles" not in st.session_state:
    st.session_state.perfiles = False

if "ingreso" not in st.session_state:
    st.session_state.ingreso = False

if "lista_tarjetas" not in st.session_state:
    st.session_state.lista_tarjetas = list(range(1,9))
    st.session_state.nro_tarjeta = choice(st.session_state.lista_tarjetas)
    st.session_state.orden_tarjetas = [st.session_state.nro_tarjeta]

if "alt_A" not in st.session_state:
    alternativas = [1, 2]
    st.session_state.alt_A = choice(alternativas)
    alternativas.remove(st.session_state.alt_A)
    st.session_state.alt_B = alternativas[0]

if "elecciones_dict" not in st.session_state:
    st.session_state.elecciones_dict = {}

if "encuestadores_dict" not in st.session_state:
    encuestadores_df = pd.read_csv("encuestadores.csv", sep =";")
    st.session_state.encuestadores_dict = generar_encuestadores_dict(encuestadores_df)

#nro_disenho = st.session_state.nro_disenho

# Frontend

st.set_page_config(layout="centered")

start_date = "2025-07-31T09:40:00+00:00"
end_date = "2025-07-31T16:40:00+00:00"

#bbdd_pd_df = cargar_bbdd("bbdd_pd", start_date, end_date)

#bbdd_pd_df

ingresos_df = cargar_bbdd("ingresos", start_date, end_date)


# Imagen de fondo

#background_url = "https://storage.googleapis.com/chile-travel-cdn/2021/07/puerto-montt_prin-min.jpg"
#background_url = "https://raw.githubusercontent.com/felixandro/pd_puerto_montt/refs/heads/master/figura_fondo.png"
#agregar_imagen_fondo(background_url)

# Identificación del Encuestador

lugar = st.selectbox(
    "Lugar de Encuesta",
    [""] + list(st.session_state.encuestadores_dict.keys())
)

if lugar != "":

    id_encuestador = st.selectbox(
        "Encuestador",
        [""] + st.session_state.encuestadores_dict[lugar]
    )

    if id_encuestador != "":

        ingresos_df_filtered = ingresos_df[ingresos_df["id_encuestador"] == id_encuestador].sort_values(by="hora_id", ascending=True)

        ingresos_df_filtered["dia"] = pd.to_datetime(ingresos_df_filtered["hora_id"]).dt.strftime("%d/%m")
        ingresos_df_filtered["hora"] = pd.to_datetime(ingresos_df_filtered["hora_id"]).dt.strftime("%H:%M:%S")

        t_cols = {"t_caract": "Características", 
                  "t_intro": "Introducción", 
                  "t_pd1": "PD 1", 
                  "t_pd2": "PD 2", 
                  "t_pd3": "PD 3", 
                  "t_pd4": "PD 4", 
                  "t_ing": "Posesión de Vehículo e Ingreso"}

        df = ingresos_df_filtered[["dia", "hora", "genero", "edad", "proposito", "veh_hogar", "ingreso"] + list(t_cols.keys())]
        df

        for t_col, label_col in t_cols.items():
            fig, ax = plt.subplots()
            ax.plot(df["hora"], df[t_col], marker='o')
            ax.set_xlabel("Hora")
            ax.set_ylabel("segundos")
            ax.set_ylim(0, 60)
            ax.set_title(f"Tiempo de Respuesta {label_col}")
            plt.xticks(rotation=45)
            if label_col.startswith("PD"):
                ax.axhline(10, color='red', linestyle='--', linewidth=1)
                ax.axhline(20, color='red', linestyle='--', linewidth=1)
                ax.axhline(30, color='red', linestyle='--', linewidth=1)
            st.pyplot(fig)
        #ingresos_df_filtered = ingresos_df_filtered.sort_values(by="hora_id", ascending=False)
