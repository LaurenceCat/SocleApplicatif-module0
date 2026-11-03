"""Construction du graphe d'agent LangGraph avec Tool Calling arithmetique."""

from typing import Any, Dict, List, Optional
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

from iatos_core.config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TEMPERATURE
from iatos_core.logger import logger
from iatos_core.tools.math_tool import calculer

SYSTEM_PROMPT = (
    "Tu es l'assistant intelligent IA-TOS de la plateforme ATLAS. "
    "Tu es courtois, rigoureux et precis. "
    "Lorsque l'utilisateur te demande un calcul arithmetique (addition, soustraction, multiplication, division), "
    "tu DOIS systematiquement appeler l'outil 'calculer' dedie au lieu de calculer mentalement."
)


def get_llm():
    """Initialise le connecteur ChatOllama."""
    return ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=OLLAMA_TEMPERATURE,
    )


def create_agent(llm=None):
    """Cree et compile le graphe ReAct LangGraph."""
    model = llm or get_llm()
    tools = [calculer]
    logger.info("Compilation du graphe LangGraph avec le modele '{m}' et {n} tool(s)", m=OLLAMA_MODEL, n=len(tools))
    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=SYSTEM_PROMPT,
    )
    return agent


# Instance par defaut du graphe
_agent_instance = None


def get_agent():
    """Recupere ou instancie le graphe de maniere paresseuse (lazy loading)."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = create_agent()
    return _agent_instance


def run_agent_message(
    user_message: str,
    history: Optional[List[Dict[str, str]]] = None,
    agent=None,
) -> Dict[str, Any]:
    """Execute un tour de conversation avec l'agent LangGraph.
    
    Args:
        user_message: Texte saisi par l'utilisateur.
        history: Historique au format [{'role': 'user'|'assistant', 'content': '...'}].
        agent: Instance optionnelle de l'agent (utile pour les tests/mocks).
        
    Returns:
        Dictionnaire avec la reponse finale, le statut et les traces d'outils.
    """
    history = history or []
    current_agent = agent or get_agent()

    messages = []
    for item in history:
        role = item.get("role")
        content = item.get("content", "")
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))

    messages.append(HumanMessage(content=user_message))

    try:
        logger.info("Invocation de l'agent LangGraph avec le message : '{msg}'", msg=user_message)
        result = current_agent.invoke({"messages": messages})
        final_messages = result.get("messages", [])
        
        # Extraire la reponse du dernier AIMessage
        ai_response = "Je n'ai pas pu generer de reponse."
        tool_invoked = False
        tool_results = []

        for msg in reversed(final_messages):
            if isinstance(msg, AIMessage) and msg.content:
                ai_response = str(msg.content)
                break

        for msg in final_messages:
            if isinstance(msg, ToolMessage):
                tool_invoked = True
                tool_results.append(str(msg.content))

        logger.success("Reponse de l'agent generee avec succes (outil appele: {t})", t=tool_invoked)
        return {
            "success": True,
            "response": ai_response,
            "tool_called": tool_invoked,
            "tool_results": tool_results,
        }

    except Exception as exc:
        logger.error("Erreur lors de l'appel a l'agent LangGraph : {err}", err=exc)
        return {
            "success": False,
            "response": (
                f"Desole, le service de conversation locale est momentanement indisponible "
                f"(verifiez qu'Ollama est actif sur {OLLAMA_BASE_URL} avec le modele {OLLAMA_MODEL}). "
                f"Details techniques : {exc}"
            ),
            "tool_called": False,
            "tool_results": [],
        }
