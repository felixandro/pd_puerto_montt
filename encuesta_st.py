import streamlit as st
import pandas as pd
import backend as be
from random import choice, random
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

#if "lista_tarjetas" not in st.session_state:
#    st.session_state.lista_tarjetas = list(range(1,9))
#    st.session_state.nro_tarjeta = choice(st.session_state.lista_tarjetas)
#    st.session_state.orden_tarjetas = [st.session_state.nro_tarjeta]

if "alt_A" not in st.session_state:
    alternativas = [1, 2]
    st.session_state.alt_A = choice(alternativas)
    alternativas.remove(st.session_state.alt_A)
    st.session_state.alt_B = alternativas[0]

if "elecciones_dict" not in st.session_state:
    st.session_state.elecciones_dict = {}

if "encuestadores_dict" not in st.session_state:
    encuestadores_df = pd.read_csv("encuestadores.csv", sep =";")
    st.session_state.encuestadores_dict = be.generar_encuestadores_dict(encuestadores_df)

if "horas_list" not in st.session_state:
    st.session_state.horas_list = []

st.set_page_config(layout="centered")

# Imagen de fondo

background_url = "https://raw.githubusercontent.com/felixandro/pd_puerto_montt/refs/heads/master/figura_fondo.png"
be.agregar_imagen_fondo(background_url)

# Identificación del Encuestador

if not st.session_state.id_encuestador:

    be.texto_con_fondo("Lugar de Encuesta", upper_margin=0)

    lugar = st.selectbox(
        "",
        [""] + list(st.session_state.encuestadores_dict.keys())
    )

    if lugar != "":

        be.texto_con_fondo("Encuestador", upper_margin=0)

        id_encuestador = st.selectbox(
            "",
            [""] + st.session_state.encuestadores_dict[lugar]
        )

        if id_encuestador != "" :
            next_button_0 = st.button("Siguiente", use_container_width=True, type = "primary")
            
            if next_button_0:
                st.session_state.id_encuestador = True
                st.session_state.id_encuestador_valor = id_encuestador
                st.session_state.lugar = lugar
                st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))
                st.rerun()


# Características del Encuestado

if st.session_state.id_encuestador and not st.session_state.caracteristicas:

    be.texto_con_fondo(f"Encuestador: {st.session_state.id_encuestador_valor}", 
                    upper_margin="1rem",
                    bg_color="rgba(10, 20, 176, 0.95)",
                    text_color="#FFFFFF")
    be.texto_con_fondo(f"Lugar de Encuesta: {st.session_state.lugar}", 
                    upper_margin="1rem",
                    bg_color="rgba(10, 20, 176, 0.95)",
                    text_color="#FFFFFF")

    if st.session_state.lugar == "Centro":
        be.texto_con_fondo("Par OD", upper_margin=0)

        modo_par = st.selectbox("",
                                ["", "Manuel Montt - Centro", "Mirasol - Centro", "Alerce - Centro"])

    else:

        be.texto_con_fondo("Modo", upper_margin=0)

        if st.session_state.lugar == "Alerce":
            modos_list = ["", "Taxibus", "Taxi Colectivo", "Tren"]

        else:
            modos_list = ["", "Taxibus", "Taxi Colectivo"]

        modo_par = st.selectbox("",
                                modos_list)

    be.texto_con_fondo("Género", upper_margin=0)

    genero = st.selectbox(
        "",
        ["", "Femenino", "Masculino", "No Responde"]
    )

    be.texto_con_fondo("Edad", upper_margin=0)

    edad = st.number_input(
        "",
        min_value=14,
        max_value=100,
        value=None,
        step=1
    )

    be.texto_con_fondo("¿Cuál es el propósito de su viaje?", upper_margin=0)

    proposito = st.selectbox(
        "",
        ["", "Trabajo", "Estudio", "Otro"]
    )

    if modo_par != "" and genero != "" and edad  and proposito != "":

        next_button_1 = st.button("Siguiente", use_container_width=True, type = "primary")
        
        if next_button_1:
            st.session_state.caracteristicas = True
            st.session_state.modo_par = modo_par
            st.session_state.genero = genero
            st.session_state.edad = edad
            st.session_state.proposito = proposito
            st.session_state.nro_disenho = be.definir_nro_disenho(st.session_state.lugar, st.session_state.modo_par)
            st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))
            st.session_state.nro_bloque = 1 if random() < 0.5 else 2
            st.session_state.lista_tarjetas = be.definir_lista_tarjetas(st.session_state.nro_disenho, st.session_state.nro_bloque)
            st.session_state.nro_tarjeta = choice(st.session_state.lista_tarjetas)
            st.session_state.orden_tarjetas = [st.session_state.nro_tarjeta]
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
    
    tiene_transbordo = (int(len(altA_label.split("-"))-1)>0) or (int(len(altB_label.split("-"))-1)>0)
    if tiene_transbordo:
        texto_transbordo = ", cantidad de **transbordos**"
    else:
        texto_transbordo = ""
    
    hay_auto = (altA_label == "Auto") or (altB_label == "Auto")
    if hay_auto:
        texto_costo = "Tenga claro que el **costo** del auto corresponde aL gasto en **bencina** y **estacionamiento**, mientras que para la otra alternativa corresponde al **pasaje**."
    else:
        texto_costo = "Tenga claro que el **costo** corresponde al **pasaje** de cada alternativa."


    texto_introductorio1 = textwrap.dedent(f"""
        El objetivo de esta encuesta es conocer sus preferencias respecto al medio de transporte que usaría ante una eventual construcción de un teleférico en Puerto Montt.

        Para esto suponga un viaje desde **{origen}** al **Centro de Puerto Montt** (idéntico al que está realizando hoy) y que sus opciones son **{altA_label}** y **{altB_label}**.

        Se le presentarán 5 escenarios distintos, donde las alternativas serán caracterizadas mediante su **costo** monetario{texto_transbordo} y **tiempos** de viaje, espera y caminata. **(Ver ejemplo a continuación)**""")

    texto_introductorio2 = textwrap.dedent(f"""
        {texto_costo}
                                           
        **ES CRUCIAL** que **analice detenidamente** cada escenario, **compare** los atributos de ambas alternativas y seleccione aquella que elegiría en una situación **real** con un contexto **idéntico** al de su actual viaje.
                                           
        Su elección **no debe verse influida** por si usted cree que el teleférico va o no a construirse.
                                           
        La encuesta es totalmente **anónima** y **no hay respuestas correctas o incorrectas**.""")


    be.texto_con_fondo(texto_introductorio1, upper_margin="1rem")

    altA_label = data[f"alt{st.session_state.alt_A}"]
    altB_label = data[f"alt{st.session_state.alt_B}"]

    niveles_a_ejemplo = [altA_label] + data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_A}"] + [int(len(altA_label.split("-"))-1)]
    niveles_b_ejemplo = [altB_label] + data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_B}"] + [int(len(altB_label.split("-"))-1)]
    
    be.perfil_eleccion(niveles_a_ejemplo, niveles_b_ejemplo)
    be.texto_con_fondo(texto_introductorio2, upper_margin="1rem")


    next_button_2 = st.button("Siguiente", use_container_width=True, type = "primary")
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

    be.texto_con_fondo(f"Pregunta {len(st.session_state.orden_tarjetas)} - ¿Cuál alternativa elegiría?", upper_margin=0)

    niveles_a = [altA_label] + data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_A}"] + [int(len(altA_label.split("-"))-1)]
    niveles_b = [altB_label] + data[f"T{st.session_state.nro_tarjeta}"][f"A{st.session_state.alt_B}"] + [int(len(altB_label.split("-"))-1)]
    be.perfil_eleccion(niveles_a, niveles_b)

    button_a = st.button(altA_label, use_container_width= True)
    button_b = st.button(altB_label, use_container_width= True)

    if button_a:
        be.texto_con_fondo(f"Seleccionó {altA_label}")
        st.session_state.elecciones_dict[st.session_state.nro_tarjeta] = altA_label
        
    if button_b:
        be.texto_con_fondo(f"Seleccionó {altB_label}")
        st.session_state.elecciones_dict[st.session_state.nro_tarjeta] = altB_label

    if  st.session_state.nro_tarjeta in st.session_state.elecciones_dict:
        next_button_3 = st.button("Siguiente", use_container_width=True, type = "primary")
        
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
                        "fecha": hora_actual,
                        "bloque": st.session_state.nro_bloque,
                        "id_respuesta": be.generar_id_respuesta(
                            hora_id=st.session_state.hora_id,
                            nro_disenho=st.session_state.nro_disenho,
                            nro_tarjeta=st.session_state.nro_tarjeta,
                            id_encuestador=st.session_state.id_encuestador_valor,
                            edad=st.session_state.edad,
                            genero=st.session_state.genero,
                            proposito=st.session_state.proposito
                        )
                    }
            st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))

            be.guardar_respuestas(respuesta)

            if len(st.session_state.elecciones_dict) <= 4:
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
    #dst.write(st.session_state.orden_tarjetas)

if st.session_state.perfiles and not st.session_state.ingreso:

    be.texto_con_fondo("¿Cuántos vehículos posee en el hogar?", upper_margin=0)

    veh_hogar = st.selectbox(
        "",
        ["", "0", "1", "2 o más"]
    )

    be.texto_con_fondo("¿En qué rango se encuentra su ingreso familiar mensual?", upper_margin=0)

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
        next_button_4 = st.button("Finalizar Encuesta", use_container_width=True, type = "primary")
        
        if next_button_4:
            st.session_state.ingreso = True
            st.session_state.veh_hogar = veh_hogar
            st.session_state.ing_familiar = ing_familiar
            st.session_state.horas_list.append(time.strftime("%Y-%m-%d %H:%M:%S"))

            assert len(st.session_state.horas_list) == 9

            ingresos_respuesta = {
                "id_encuestador": st.session_state.id_encuestador_valor,
                "lugar": st.session_state.lugar,
                "hora_id": st.session_state.hora_id,
                "genero": st.session_state.genero,
                "edad": st.session_state.edad,
                "proposito": st.session_state.proposito,
                "veh_hogar": veh_hogar,
                "ingreso": ing_familiar,
                "nro_dis" : st.session_state.nro_disenho,
                "bloque": st.session_state.nro_bloque,
                "id_encuesta": be.generar_id_encuesta(
                    hora_id=st.session_state.hora_id,
                    nro_disenho=st.session_state.nro_disenho,
                    id_encuestador=st.session_state.id_encuestador_valor,
                    edad=st.session_state.edad,
                    genero=st.session_state.genero,
                    proposito=st.session_state.proposito
                )
            }

            tiempos_respuesta = be.generar_tiempos_dict(st.session_state.horas_list)

            total_dict = ingresos_respuesta | tiempos_respuesta

            be.guardar_ingresos(total_dict)
            st.rerun()


if st.session_state.ingreso:
    be.texto_con_fondo("¡Encuesta Finalizada!", upper_margin="1rem")

    new_survey_button = st.button("Nueva Encuesta", use_container_width=True, type = "primary")

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

