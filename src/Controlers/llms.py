from langchain_google_genai import ChatGoogleGenerativeAI


def init_chat_model(model_name: str, temperature: float):
    """
    Initialize and configure a ChatGoogleGenerativeAI model.

    Parameters
    ----------
    model_name : str
        Name of the model to load.
    temperature : float
        Temperature setting that controls randomness in the model's generation.
        Must be between 0.0 and 1.0.

    Returns
    -------
    ChatGoogleGenerativeAI
        An instance of the configured language model.
    """
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature
    )


def obtener_respuesta(chat_model, historial):
    """
    Generate a model response based on prior conversation history.

    Parameters
    ----------
    chat_model : ChatGoogleGenerativeAI
        The language model instance that will generate the response.
    historial : list of BaseMessage
        List of chat messages including both user and assistant messages.
        The full conversation is passed to provide context to the model.

    Returns
    -------
    AIMessage
        The assistant's generated response wrapped in a LangChain message object.
    """
    return chat_model.invoke(historial)
