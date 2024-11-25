import streamlit as st
from groq import Groq

modelos = ["llama3-8b-8192","llama3-70b-8192","mixtral-8x7b-32768"]
modelo_en_uso = ""
cliente_usuario = ""
clave_secreta = ""
mensaje = ""

def crear_usuario():
    #LE ASIGNAMOS LA CLAVE A UNA VARIABLE
    clave_secreta = st.secrets["CLAVE_API"]
    #RETORNAMOS LA CLAVE COMO "api_key"
    return Groq(api_key=clave_secreta)

#DEVUELVE LA RESPUESTA DEL CHATBOT PROCESADA POR EL MODELO ELEGIDO
def configurar_modelo(cliente, modelo, mensaje_de_entrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role" : "user", "content" : mensaje_de_entrada}],
        stream = True
    )

def configurar_pagina():
    #LA PESTAÑA
    st.set_page_config("Mi chat IA")
    #TITULO DE LA PAGINA
    st.title("Mi chat IA")
    #SIDEBAR
    st.sidebar.title("Panel de Modelos")
    #SELECTOR DE MODELOS
    m = st.sidebar.selectbox("Modelos", modelos, 0)
    #DEVUELVO EL VALOR DE LO SELECCIONADO
    return m

#INICIALIZAR ESTADO SI EL ESTADO NO EXISTE
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})

def mostrar_historial():
        for mensaje in st.session_state.mensajes:
                with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
                        st.markdown(mensaje["content"])

def area_chat():
        contenedorDelChat = st.container(height=400,border=True)
        # Abrimos el contenedor del chat y mostramos el historial.
        with contenedorDelChat:
                mostrar_historial()

#INICIALIZAMOS LA PAGINA
modelo_en_uso = configurar_pagina()
#INICIALIZAMOS EL CLIENTE USUARIO CON LA API KEY
cliente_usuario = crear_usuario()
#INICIALIZAMOS EL ESTADO "MENSAJES"
inicializar_estado()
#INICIALIZAMOS EL AREA DEL CHAT
area_chat()
#EL USUARIO TIENE QUE ESCRIBIR ALGO
mensaje = st.chat_input()
#SI ESCRIBE ALGO, SE INICIALIZA EL MODELO
if mensaje:
    actualizar_historial("user", mensaje, "😎")
    chat_completo = configurar_modelo(cliente_usuario, modelo_en_uso, mensaje)
    actualizar_historial("assistant", chat_completo,"🤖")
    st.rerun()
