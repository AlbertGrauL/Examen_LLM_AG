from user_interface.interface import (
    init_ui, 
    sidebar_controls, 
    mostrar_historial, 
    manejar_input
)
from Controlers.llms import init_chat_model, obtener_respuesta

# Configurar página
init_ui()

# Sidebar, modelo y temperatura
model_name, temp = sidebar_controls()

# Inicializar modelo con esos parámetros
chat_model = init_chat_model(model_name, temp)

# Mostrar historial del chat actual
mostrar_historial()

# Manejar input y respuesta
manejar_input(chat_model, obtener_respuesta)
