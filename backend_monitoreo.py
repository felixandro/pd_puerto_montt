import streamlit as st
from supabase import create_client, Client
import pandas as pd
import json



def cargar_bbdd(table_name, start_date, end_date):
    # Configura tus credenciales de Supabase
    url = "https://gkgxipnjsoxgqsaukhtg.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdrZ3hpcG5qc294Z3FzYXVraHRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAxMTI1NjEsImV4cCI6MjA2NTY4ODU2MX0.TNyYDvpLhBX-Ocr03jzdo9GulXYfYMmOh0Vx20hlJfg"

    # Crea el cliente
    supabase: Client = create_client(url, key)

    all_data = []
    page_size = 1000
    offset = 0

    while True:
        response = (
            supabase.table(table_name)
            .select('*')
            .gte("hora_id", start_date)
            .lte("hora_id", end_date)
            .range(offset, offset + page_size - 1)
            .execute()
        )
        batch = response.data
        if not batch:
            break
        all_data.extend(batch)
        offset += page_size

        df = pd.DataFrame(all_data)

    return df

def generar_resumen_encuestas_val(df, groupby_col):
    conteo_df = df.groupby(groupby_col).agg(
        suma_val=('val', 'sum'),
        conteo=('val', 'count')
    ).reset_index()

    conteo_df["Porcentaje"] = (conteo_df["suma_val"] / conteo_df["conteo"])

    conteo_df.rename(columns={'id_encuestador': 'Encuestador', 
                              'nro_dis': 'Diseño', 
                              'conteo': 'Total Encuestas', 
                              'suma_val': 'Encuestas Válidas'}, 
                              inplace=True)

    return conteo_df

def generar_encuestas_val_xdisenho(df):

    filas = []
    for i in range(1, 11):
        json_path = f"Disenhos/disenho_{i}.json"
        with open(json_path, "r", encoding="utf-8") as f:
            datos_json = json.load(f)
        nro_dis = datos_json["nro_disenho"]
        sector = datos_json["par"]
        modo_1 = datos_json["alt1"]
        modo_2 = datos_json["alt2"]
        enc_val = df[df["nro_dis"] == nro_dis]["val"].sum()
        enc_total = df[df["nro_dis"] == nro_dis].shape[0]
        filas.append({
            "Diseño": nro_dis,
            "Par": sector + " - Centro",
            "Modo 1": modo_1,
            "Modo 2": modo_2,
            "Val": enc_val,
            "Total": enc_total,
            "Porcentaje": (enc_val / enc_total)  if enc_total > 0 else 0
        })

    df = pd.DataFrame(filas)

    return df

def generar_encuestadores_list(encuestadores_df):
    encuestadores_list = []
    for index, row in encuestadores_df.iterrows():
        encuestador = row['Encuestador']
        if encuestador not in encuestadores_list:
            encuestadores_list.append(encuestador)
    return encuestadores_list