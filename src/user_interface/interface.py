import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from Controlers.export_import import exportar_chat, importar_chat



def init_ui():
    """
    Initialize the main Streamlit UI configuration.

    This function sets up page metadata such as title and icon,
    and displays the main page header and description.

    Returns
    -------
    None
        This function does not return a value. It only configures
        the Streamlit interface.
    """
    st.set_page_config(page_title="Chatbot Pro", page_icon="🤖")
    st.title("🤖 Chatbot Mejorado")
    st.markdown("Chatbot con selección de modelo, temperatura, múltiples conversaciones y exportación/importación.")



def sidebar_controls():
    """
    Render the sidebar configuration panel.

    This includes model selection, temperature adjustment,
    chat management (new, delete, switch), and chat export/import.

    Returns
    -------
    tuple
        A tuple containing:
        
        - modelo : str  
            Name of the selected language model.

        - temperatura : float  
            Temperature setting for generation control.
    """
    st.sidebar.header("⚙️ Configuración")

    modelo = st.sidebar.selectbox(
        "Modelo",
        [
            "gemini-2.5-flash",
            "gemini-2.5-pro"
        ]
    )

    temperatura = st.sidebar.slider(
        "Temperatura",
        0.0, 1.0, 0.4, 0.1
    )


    st.sidebar.subheader("🗂️ Chats")


    if "chats" not in st.session_state:
        st.session_state.chats = {"Chat 1": []}
        st.session_state.chat_actual = "Chat 1"

    chat_seleccionado = st.sidebar.selectbox(
        "Conversación",
        list(st.session_state.chats.keys()),
        index=list(st.session_state.chats.keys()).index(st.session_state.chat_actual),
        key="selector_chat"
    )

    st.session_state.chat_actual = chat_seleccionado


    if st.sidebar.button("➕ Nuevo chat", key="btn_nuevo"):
        nuevo_nombre = f"Chat {len(st.session_state.chats) + 1}"
        st.session_state.chats[nuevo_nombre] = []
        st.session_state.chat_actual = nuevo_nombre
        st.rerun()


    if st.sidebar.button("🗑️ Eliminar chat", key="btn_eliminar"):
        if len(st.session_state.chats) == 1:
            st.sidebar.warning("Debe quedar al menos 1 chat activo.")
        else:
            chat_borrar = st.session_state.chat_actual
            del st.session_state.chats[chat_borrar]
            st.session_state.chat_actual = list(st.session_state.chats.keys())[0]
            st.rerun()

    st.sidebar.subheader("⬇️ Exportar chat")
    if st.sidebar.button("Exportar este chat"):
        historial = st.session_state.chats[st.session_state.chat_actual]
        json_data = exportar_chat(historial)
        st.sidebar.download_button(
            label="Descargar JSON",
            data=json_data,
            file_name=f"{st.session_state.chat_actual}.json",
            mime="application/json"
        )


    st.sidebar.subheader("⬆️ Importar chat")
    archivo = st.sidebar.file_uploader("Sube un archivo JSON", type=["json"])

    if archivo:
        try:
            contenido = archivo.read().decode("utf-8")
            nuevo_chat = importar_chat(contenido)

            nombre = f"Chat {len(st.session_state.chats) + 1}"
            st.session_state.chats[nombre] = nuevo_chat
            st.session_state.chat_actual = nombre

            st.sidebar.success("Chat importado correctamente.")

        except Exception as e:
            st.sidebar.error(f"Error al importar: {e}")

    return modelo, temperatura



def mostrar_historial():
    """
    Display the chat history of the currently selected conversation.

    Each message is rendered in the appropriate chat bubble depending
    on whether it's an AI response or a user message.

    Returns
    -------
    None
        This function only handles UI rendering.
    """
    historial = st.session_state.chats[st.session_state.chat_actual]
    for msg in historial:
        role = "assistant" if isinstance(msg, AIMessage) else "user"
        with st.chat_message(role):
            st.markdown(msg.content)



def manejar_input(chat_model, obtener_respuesta_fn):
    """
    Handle user input, send it to the model, render the response,
    and store both in the conversation history.

    Parameters
    ----------
    chat_model : object
        Model instance used to generate responses.
    obtener_respuesta_fn : callable
        Function that accepts `(chat_model, historial)` and returns an AIMessage.

    Returns
    -------
    None
        The function updates session_state and renders chat messages.
    """
    user_msg = st.chat_input("Escribe tu mensaje:")

    if not user_msg:
        return

    
    with st.chat_message("user"):
        st.markdown(user_msg)
    st.session_state.chats[st.session_state.chat_actual].append(
        HumanMessage(content=user_msg)
    )

    
    respuesta = obtener_respuesta_fn(
        chat_model,
        st.session_state.chats[st.session_state.chat_actual]
    )

    with st.chat_message("assistant"):
        st.markdown(respuesta.content)

    st.session_state.chats[st.session_state.chat_actual].append(respuesta)
