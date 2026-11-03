"""Definitions d'etat pour le graphe LangGraph."""

from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """Etat conversationnel contenant l'historique des messages echanges."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
