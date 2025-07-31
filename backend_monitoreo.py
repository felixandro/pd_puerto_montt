import streamlit as st
from supabase import create_client, Client
import pandas as pd



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
