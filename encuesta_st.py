import streamlit as st
import pandas as pd
from backend import agregar_imagen_fondo, perfil_eleccion, texto_con_fondo, guardar_respuestas, guardar_ingresos, definir_nro_disenho
from random import choice
import json
import time
import textwrap

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

if "horas_list" not in st.session_state:
    st.session_state.horas_list = []

#nro_disenho = st.session_state.nro_disenho


st.set_page_config(layout="centered")

# Imagen de fondo

#background_url = "https://storage.googleapis.com/chile-travel-cdn/2021/07/puerto-montt_prin-min.jpg"
background_url = "https://raw.githubusercontent.com/felixandro/pd_puerto_montt/refs/heads/master/figura_fondo.png"
agregar_imagen_fondo(background_url)

# Identificación del Encuestador

if not st.session_state.id_encuestador:
    
    texto_con_fondo("Lugar de Encuesta", upper_margin=0)

    lugar = st.selectbox(
        "",
        [""] + list(st.session_state.encuestadores_dict.keys())
    )

    if lugar != "":

        texto_con_fondo("Encuestador", upper_margin=0)

        id_encuestador = st.selectbox(
            "",
            [""] + st.session_state.encuestadores_dict[lugar]
        )

        if id_encuestador != "" :
            next_button_0 = st.button("Siguiente", use_container_width=True)
            
            if next_button_0:
                st.session_state.id_encuestador = True
                st.session_state.id_encuestador_valor = id_encuestador
                st.session_state.lugar = lugar
                st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))
                st.rerun()


# Características del Encuestado

if st.session_state.id_encuestador and not st.session_state.caracteristicas:

    texto_con_fondo(f"Encuestador: {st.session_state.id_encuestador_valor}", 
                    upper_margin="1rem",
                    bg_color="rgba(10, 20, 176, 0.95)",
                    text_color="#FFFFFF")
    texto_con_fondo(f"Lugar de Encuesta: {st.session_state.lugar}", 
                    upper_margin="1rem",
                    bg_color="rgba(10, 20, 176, 0.95)",
                    text_color="#FFFFFF")

    if st.session_state.lugar == "Centro":
        texto_con_fondo("Par OD", upper_margin=0)

        modo_par = st.selectbox("",
                                ["", "Manuel Montt - Centro", "Mirasol - Centro", "Alerce - Centro"])

    else:

        texto_con_fondo("Modo", upper_margin=0)
        
        if st.session_state.lugar == "Alerce":
            modos_list = ["", "Taxibus", "Taxi Colectivo", "Tren"]

        else:
            modos_list = ["", "Taxibus", "Taxi Colectivo"]

        modo_par = st.selectbox("",
                                modos_list)

    texto_con_fondo("Género", upper_margin=0)

    genero = st.selectbox(
        "",
        ["", "Femenino", "Masculino", "No Responde"]
    )

    texto_con_fondo("Edad", upper_margin=0)

    edad = st.number_input(
        "",
        min_value=14,
        max_value=100,
        value=None,
        step=1
    )

    texto_con_fondo("¿Cuál es el propósito de su viaje?", upper_margin=0)

    proposito = st.selectbox(
        "",
        ["", "Trabajo", "Estudio", "Otro"]
    )

    if modo_par != "" and genero != "" and edad  and proposito != "":

        next_button_1 = st.button("Siguiente", use_container_width=True)
        
        if next_button_1:
            st.session_state.caracteristicas = True
            st.session_state.modo_par = modo_par
            st.session_state.genero = genero
            st.session_state.edad = edad
            st.session_state.proposito = proposito
            st.session_state.nro_disenho = definir_nro_disenho(st.session_state.lugar, st.session_state.modo_par)
            st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))
            st.rerun()

# Texto introductorio
if st.session_state.caracteristicas and not st.session_state.texto_introductorio:

    if st.session_state.lugar == "Centro":
        origen = st.session_state.modo_par.split(" - ")[0]
    else:
        origen = st.session_state.lugar

    nro_disenho = st.session_state.nro_disenho
    with open(f'Disenhos/disenho_{nro_disenho}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    altA_label = data[f"alt{st.session_state.alt_A}"]
    altB_label = data[f"alt{st.session_state.alt_B}"]
    
    texto_introductorio = textwrap.dedent(f"""        
        A continuación, le propondremos una serie de situaciones hipotéticas de elección entre dos modos de transporte para realizar el mismo viaje que está haciendo hoy (Desde {origen} al Centro), para lo cual podrá elegir entre **{altA_label}** y **{altB_label}**

        Cada alternativa será definida por el costo monetario y los tiempos de viaje, espera y caminata que implicaría. Para cada escenario le pedimos que indique cuál de las dos opciones elegiría si ambas estuvieran disponibles.

        Sabemos que en una ciudad con desniveles pronunciados, sectores densamente poblados en altura y frecuentes problemas de congestión, es importante explorar nuevas formas de transporte. Sin embargo, queremos enfatizar que su elección no debe verse influida por si usted cree que el teleférico va o no a construirse. Lo más importante es que elija la alternativa que realmente refleje su preferencia personal, tal como si tuviera que tomar esa decisión en la vida real.

        Favor analice cada escenario con detención y tenga presente que no hay respuestas correctas o incorrectas.""")
    
    texto_con_fondo(texto_introductorio, upper_margin="1rem")

    next_button_2 = st.button("Siguiente", use_container_width=True)
    if next_button_2:
        st.session_state.texto_introductorio = True
        st.session_state.hora_id = time.strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))
        st.rerun()

# Perfiles de Elección

elif st.session_state.texto_introductorio and not st.session_state.perfiles:

    nro_disenho = st.session_state.nro_disenho
    with open(f'Disenhos/disenho_{nro_disenho}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    altA_label = data[f"alt{st.session_state.alt_A}"]
    altB_label = data[f"alt{st.session_state.alt_B}"]


    texto_con_fondo(f"Pregunta {len(st.session_state.orden_tarjetas)} - ¿Cuál alternativa elegiría?", upper_margin=0)

    niveles_a = [altA_label] + data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_A}"] + [int(len(altA_label.split("-"))-1)]
    niveles_b = [altB_label] + data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_B}"] + [int(len(altB_label.split("-"))-1)]
    perfil_eleccion(niveles_a, niveles_b)

    button_a = st.button(altA_label, use_container_width= True)
    button_b = st.button(altB_label, use_container_width= True)

    if button_a:
        texto_con_fondo(f"Seleccionó {altA_label}")
        st.session_state.elecciones_dict[st.session_state.nro_tarjeta] = altA_label
        
    if button_b:
        texto_con_fondo(f"Seleccionó {altB_label}")
        st.session_state.elecciones_dict[st.session_state.nro_tarjeta] = altB_label

    if  st.session_state.nro_tarjeta in st.session_state.elecciones_dict:
        next_button_3 = st.button("Siguiente", use_container_width=True)
        
        if next_button_3:
            st.session_state.lista_tarjetas.remove( st.session_state.nro_tarjeta)
            hora_actual = time.strftime("%Y-%m-%d %H:%M:%S")
            respuesta = {
                        "id_encuestador": st.session_state.id_encuestador_valor,
                        "lugar": st.session_state.lugar,
                        "hora_id": st.session_state.hora_id,
                        "genero": st.session_state.genero,
                        "edad": st.session_state.edad,
                        "proposito": st.session_state.proposito,
                        "disenho": st.session_state.nro_disenho,
                        "tarjeta": st.session_state.nro_tarjeta,
                        "a1": data[f"alt{st.session_state.alt_A}"],
                        "c_a1": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_A}"][0],
                        "tv_a1": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_A}"][1],
                        "te_a1": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_A}"][2],
                        "tc_a1": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_A}"][3],
                        "tr_a1": int(len(altA_label.split("-"))-1),
                        "a2": data[f"alt{st.session_state.alt_B}"],
                        "c_a2": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_B}"][0],
                        "tv_a2": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_B}"][1],
                        "te_a2": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_B}"][2],
                        "tc_a2": data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_B}"][3],
                        "tr_a2": int(len(altB_label.split("-"))-1),
                        "choice": st.session_state.elecciones_dict[st.session_state.nro_tarjeta],
                        "fecha": hora_actual
                    }
            st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))

            guardar_respuestas(respuesta)

            if len(st.session_state.elecciones_dict) <= 3:
                st.session_state.nro_tarjeta = choice(st.session_state.lista_tarjetas)
                st.session_state.orden_tarjetas.append(st.session_state.nro_tarjeta)
                st.rerun()
            else:
                st.session_state.perfiles = True
                st.rerun()

                
    #st.divider()
    #st.write(f"Tarjeta seleccionada: {st.session_state.nro_tarjeta}")
    #st.write(f"Alternativa A: {st.session_state.alt_A} {altA_label}")
    #st.write(f"Alternativa B: {st.session_state.alt_B} {altB_label}")

    #st.write("Tus elecciones hasta ahora:")
    #st.write(st.session_state.elecciones_dict)
    #st.write("Orden de tarjetas seleccionadas:")
    #st.write(st.session_state.orden_tarjetas)

if st.session_state.perfiles and not st.session_state.ingreso:
    
    texto_con_fondo("¿Cuántos vehículos posee en el hogar?", upper_margin=0)

    veh_hogar = st.selectbox(
        "",
        ["", "0", "1", "2 o más"]
    )

    texto_con_fondo("¿En qué rango se encuentra su ingreso familiar mensual?", upper_margin=0)

    ing_familiar = st.selectbox(
        "",
        ["", 
         "Menos de 500.000", 
         "Entre    500.001 y   750.000", 
         "Entre    750.001 y 1.000.000",
         "Entre  1.000.001 y 1.250.000",
         "Entre  1.250.001 y 1.500.000", 
         "Entre  1.500.001 y 1.750.000",
         "Entre  1.750.001 y 2.000.000",
         "Entre  2.000.001 y 2.250.000",
         "Entre  2.250.001 y 2.500.000",
         "Más de 2.500.000",
         "No Responde"]
    )

    if veh_hogar != "" and ing_familiar != "":
        next_button_4 = st.button("Finalizar Encuesta", use_container_width=True)
        
        if next_button_4:
            st.session_state.ingreso = True
            st.session_state.veh_hogar = veh_hogar
            st.session_state.ing_familiar = ing_familiar
            st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))

            assert len(st.session_state.horas_list) == 8

            ingresos_respuesta = {
                "id_encuestador": st.session_state.id_encuestador_valor,
                "lugar": st.session_state.lugar,
                "hora_id": st.session_state.hora_id,
                "genero": st.session_state.genero,
                "edad": st.session_state.edad,
                "proposito": st.session_state.proposito,
                "veh_hogar": veh_hogar,
                "ingreso": ing_familiar
            }

            tiempos_respuesta = generar_tiempos_dict(st.session_state.horas_list)

            total_dict = ingresos_respuesta | tiempos_respuesta

            guardar_ingresos(total_dict)
            st.rerun()


if st.session_state.ingreso:
    texto_con_fondo("¡Encuesta Finalizada!", upper_margin="1rem")

    new_survey_button = st.button("Nueva Encuesta", use_container_width=True)

    if new_survey_button:
        id_encuestador = st.session_state.id_encuestador_valor
        lugar = st.session_state.lugar

        

        st.session_state.clear()
        st.session_state.id_encuestador = True
        st.session_state.id_encuestador_valor = id_encuestador
        st.session_state.lugar = lugar
        
        st.session_state.horas_list = []
        st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))


    #st.write("Tus respuestas han sido guardadas exitosamente.")
    
    # Mostrar tabla de resultados
    #st.write("Resultados de la Encuesta:")
    
    # Crear DataFrame con las respuestas
    #df = pd.DataFrame(st.session_state.elecciones_dict.items(), columns=["Tarjeta", "Elección"])
    
    # Mostrar DataFrame como tabla
    #st.dataframe(df, use_container_width=True)

    # Mostrar información adicional
    #st.write(f"Vehículos en el hogar: {st.session_state.veh_hogar}")
    #st.write(f"Ingreso familiar mensual: {st.session_state.ing_familiar}")

