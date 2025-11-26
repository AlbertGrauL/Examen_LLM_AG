import json
from langchain_core.messages import AIMessage, HumanMessage


def obtener_respuesta(chat_model, historial):
    """
    Generate a response from the model using the provided conversation history.

    Parameters
    ----------
    chat_model : object
        The language model instance that exposes an `.invoke()` method.
    historial : list of BaseMessage
        Ordered list of conversation messages (user and assistant).

    Returns
    -------
    AIMessage
        The generated response from the model.
    """
    return chat_model.invoke(historial)


def exportar_chat(historial):
    """
    Export conversation history into a JSON-formatted string.

    Each message is serialized into a dict containing the role
    ("user" or "assistant") and its content.

    Parameters
    ----------
    historial : list of BaseMessage
        A list containing the full conversation messages to be exported.

    Returns
    -------
    str
        JSON string containing the serialized conversation.
    """
    data = []
    for msg in historial:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        data.append({"role": role, "content": msg.content})
    return json.dumps(data, indent=4)


def importar_chat(json_str):
    """
    Import a chat history from a JSON string and reconstruct
    LangChain-compatible message objects.

    Parameters
    ----------
    json_str : str
        JSON string containing messages previously exported with `exportar_chat()`.

    Returns
    -------
    list of BaseMessage
        Reconstructed conversation history as HumanMessage and AIMessage objects.

    Raises
    ------
    json.JSONDecodeError
        If the input string is not valid JSON.
    KeyError
        If an expected field such as ``"role"`` or ``"content"`` is missing.
    """
    data = json.loads(json_str)
    historial = []

    for item in data:
        if item["role"] == "user":
            historial.append(HumanMessage(content=item["content"]))
        else:
            historial.append(AIMessage(content=item["content"]))

    return historial
