from dotenv import load_dotenv
import os

load_dotenv()  # Esto carga las variables de entorno desde el archivo .env

api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("La clave de API de OpenAI no está configurada en las variables de entorno")

print("Clave de API de OpenAI obtenida correctamente")


from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from typing import TypedDict, List

# Define un estado personalizado que incluya los nuevos campos
class PersonalityState(TypedDict):
    messages : List[AIMessage | HumanMessage | SystemMessage]
    descripcion : str
    contexto : str
    mensaje_usuario : str

# Inicializar el modelo
llm = ChatOpenAI(model="gpt-4o-mini")

# Función de nodo modificada para manejar la personalidad
def assistant(state: PersonalityState):
    # Crear un mensaje de sistema dinámico basado en la descripción y el contexto
    sys_msg = SystemMessage(content=f"""
    Asume la siguiente personalidad:
    Descripción: {state['descripcion']}
    Contexto adicional: {state['contexto']}
    
    Responde al siguiente mensaje manteniendo esta personalidad:
    """)
    
    # Combinar el mensaje de sistema, los mensajes anteriores y el nuevo mensaje del usuario
    messages = [sys_msg] + state['messages'] + [HumanMessage(content=state['mensaje_usuario'])]
    
    # Invocar el LLM con los mensajes
    response = llm.invoke(messages)
    
    # Devolver el estado actualizado con la respuesta
    return {"messages": state['messages'] + [response]}

def construir_y_ejecutar_grafo( descripcion , contexto , mensaje_usuario , id ):
    # Construir el grafo
    builder = StateGraph(PersonalityState)
    builder.add_node("assistant", assistant)
    builder.add_edge(START, "assistant")

    # Compilar el grafo con memoria
    from langgraph.checkpoint.memory import MemorySaver
    memory = MemorySaver()
    react_graph_memory = builder.compile(checkpointer=memory)

    # Definir el estado inicial
    initial_state = {
        "descripcion": descripcion,
        "contexto": contexto,
        "mensaje_usuario": mensaje_usuario,
        "messages": []
    }

    config = {"configurable": {"thread_id": id}}
    
    # Ejecutar el grafo
    result = react_graph_memory.invoke(initial_state, config)
    
    return result['messages'][-1].content

