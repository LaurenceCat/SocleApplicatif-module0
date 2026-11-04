"""Definitions d'etat pour le graphe LangGraph."""

from collections.abc import Sequence
from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """Etat conversationnel contenant l'historique des messages echanges."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
