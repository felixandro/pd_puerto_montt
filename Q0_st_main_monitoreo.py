import streamlit as st
import pandas as pd
from backend import generar_encuestadores_dict
from backend_monitoreo import cargar_bbdd, generar_resumen_encuestas_val, generar_encuestas_val_xdisenho
from random import choice
import json
import time
import textwrap
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


# Variables de Estado de la Sesión

if "encuestadores_dict" not in st.session_state:
    encuestadores_df = pd.read_csv("encuestadores.csv", sep =";")
    st.session_state.encuestadores_dict = generar_encuestadores_dict(encuestadores_df)

#####################################
############# Frontend ##############
#####################################

st.set_page_config(layout="centered")#frontend

st.header("Monitoreo PD Puerto Montt")#frontend

# Definir rango temporal (Fecha, Hora inicio, Hora Fin)

fecha = st.date_input("Día", value=datetime.now().date())
hora_inicio_local = st.time_input("Hora de Inicio", value=pd.to_datetime("09:00:00").time())
hora_fin_local = st.time_input("Hora de Fin", value=pd.to_datetime("17:00:00").time())

start_date = (datetime.combine(fecha, hora_inicio_local) + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%S%z") + "+00:00"
end_date = (datetime.combine(fecha, hora_fin_local) + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%S%z") + "+00:00"

# Obtener Datos asociados al rango temporal
try:
    ingresos_df = cargar_bbdd("ingresos", start_date, end_date)
except Exception as e:
    st.error(f"No se tienen encuestas para el rango temporal señalado")
    st.stop()

st.divider()#frontend

# Análisis General

st.header("Análisis General") #frontend

t_min_pd = st.number_input(
    "Tiempo mínimo de respuesta para PD (en segundos)",
    min_value=0,
    max_value=90,
    value=20,
    step=1
) #frontend

ingresos_df["val"] = (ingresos_df["t_pd1"] >= t_min_pd) * (ingresos_df["t_pd2"] >= t_min_pd) * (ingresos_df["t_pd3"] >= t_min_pd) * (ingresos_df["t_pd4"] >= t_min_pd)

st.subheader("Encuestas Válidas por Diseño") #frontend
conteo_df = generar_encuestas_val_xdisenho(ingresos_df)
st.dataframe(conteo_df, 
             hide_index=True, 
             column_config={"Porcentaje": st.column_config.ProgressColumn(
                    "Porcentaje", 
                    format="%d%%"
             )}) #frontend

st.subheader("Encuestas Válidas por Encuestador") #frontend
conteo_xEncuestador_df = generar_resumen_encuestas_val(ingresos_df, "id_encuestador")
st.dataframe(conteo_xEncuestador_df, 
             hide_index=True,
             column_config={"Porcentaje": st.column_config.ProgressColumn(
                    "Porcentaje", 
                    format="%d%%"
             )}) #frontend

st.divider()

# Análisis por Encuestador

st.header("Análisis por Encuestador") #frontend

# Identificación del Encuestador

lugar = st.selectbox(
    "Lugar de Encuesta",
    [""] + list(st.session_state.encuestadores_dict.keys())
) #frontend

if lugar != "":

    id_encuestador = st.selectbox(
        "Encuestador",
        [""] + st.session_state.encuestadores_dict[lugar]
    ) #frontend

    if id_encuestador != "":

        ingresos_df_filtered = ingresos_df[ingresos_df["id_encuestador"] == id_encuestador].sort_values(by="hora_id", ascending=True)

        conteo_df_filtered = generar_resumen_encuestas_val(ingresos_df_filtered)
        st.dataframe(conteo_df_filtered)    

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
        
        st.subheader("Encuestas Realizadas")
        df

        st.subheader("Graficos de Tiempos de Respuesta")

        df['hora'] = pd.to_datetime(df['hora']) - pd.Timedelta(hours=4)

        for t_col, label_col in t_cols.items():
            fig, ax = plt.subplots()
            ax.plot(df["hora"], df[t_col], marker='o')
            ax.set_xlabel("Hora")
            ax.set_ylabel("segundos")
            ax.set_ylim(0, max(60, df[t_col].max() + 1))
            ax.set_title(f"Tiempo de Respuesta {label_col}")

            primera_hora = df["hora"].iloc[0]
            ultima_hora = df["hora"].iloc[-1]

            hora_media = primera_hora + (ultima_hora - primera_hora) / 2

            xticks = [df["hora"].iloc[0], hora_media, df["hora"].iloc[-1]]
            xtick_labels = [xticks[0].strftime("%H:%M:%S"), xticks[1].strftime("%H:%M:%S"), xticks[2].strftime("%H:%M:%S")]

            plt.xticks(ticks=xticks, labels=xtick_labels,rotation=45)
            if label_col.startswith("PD"):
                ax.axhline(10, color='red', linestyle='--', linewidth=1)
                ax.axhline(20, color='red', linestyle='--', linewidth=1)
                ax.axhline(30, color='red', linestyle='--', linewidth=1)
            st.pyplot(fig)