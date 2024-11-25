import streamlit as st
from groq import Groq

modelos = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]
modelo_en_uso = ""
mensaje = ""
clave_secreta = ""
cliente_usuario = ""

def crear_usuario():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensaje_de_entrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role": "user", "content" : mensaje_de_entrada}],
        stream = True
    )

def generar_respuesta(chat_completo):
      respuesta_completa = ""
      for frase in chat_completo:
          if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
          yield frase.choices[0].delta.content
      return respuesta_completa

def configurar_pagina():
    #LA PESTAÑA
    st.set_page_config("Chat Cat IA")
    #TITULO DE LA PAGINA
    st.title("Chat Cat IA")
    #SIDEBAR
    st.sidebar.title("Modelos")
    #SELECTOR DE MODELOS
    m = st.sidebar.selectbox("Modelos", modelos, 0)
    #DEVUELVO EL VALOR DE LO SELECCIONADO
    return m 

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
    contenedorDelChat = st.container(height=250,border=True)
    with contenedorDelChat:
     mostrar_historial()

inicializar_estado()


def main():

    modelo_en_uso = configurar_pagina()

    cliente_usuario = crear_usuario()

    inicializar_estado()

    area_chat()

    mensaje = st.chat_input()

    chat_completo = None

    if mensaje:
        actualizar_historial("user", mensaje, "😎")
        chat_completo = configurar_modelo(cliente_usuario, modelo_en_uso, mensaje)
       
    if chat_completo:
        with st.chat_message("assistant"):
            respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
        actualizar_historial("assistant", respuesta_completa,"😺")

    st.rerun()

    print(mensaje)

if __name__ == "__main__":
    main()
