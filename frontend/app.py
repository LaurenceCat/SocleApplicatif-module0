"""Application Streamlit multi-pages - Page d'accueil & Page 0 (Chatbot LangGraph).

Starter Kit Apprenants - Brief 1 IA-TOS.
"""

import os

import requests
import streamlit as st

# URL du backend FastAPI (injectable via variable d'environnement)
FASTAPI_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Plateforme IA-TOS | Brief 1",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar globale avec statut de l'API
with st.sidebar:
    st.title("Plateforme IA-TOS")
    st.caption("Module 0 : Socle Applicatif & Microservices")
    st.divider()

    # Verification de l'etat de l'API FastAPI
    try:
        resp = requests.get(f"{FASTAPI_URL}/health", timeout=2)
        if resp.status_code == 200:
            st.success("API Backend : En ligne")
        else:
            st.warning(f"API Backend : Statut {resp.status_code}")
    except Exception:  # noqa: BLE001
        st.error("API Backend : Hors ligne (Vérifiez le port 8000)")

    st.markdown("""
    **Pages disponibles :**
    - **Page 0** : Chatbot Agentique (LangGraph)
    - **Page 1** : Scoring Credit (Regression Lineaire)
    - **Page 2** : Analyse de Sentiment (NLTK)
    """)
    st.divider()
    st.caption("Projet OPCO Atlas - Simplon & Atos 2026")

# En-tete principal
st.title("Page 0 : Assistant Conversationnel Agentique")
st.markdown("""
Bienvenue sur la plateforme unifiee **IA-TOS**. Cet agent conversationnel est orchestre avec **LangGraph** 
et connecte au LLM local **Qwen 2.5** via **Ollama**. Il possede un outil deterministe de calcul arithmetique (`calculer`).
""")

# ==============================================================================
# TODO (Apprenants) : Implémenter l'interface de chat conversationnelle
# 
# Étapes suggérées :
# 1. Initialiser st.session_state["messages"] s'il n'existe pas encore.
# 2. Afficher les messages existants de st.session_state["messages"] avec st.chat_message().
# 3. Récupérer la saisie utilisateur avec st.chat_input().
# 4. Lors de l'envoi :
#    a. Ajouter le message utilisateur dans st.session_state["messages"] et l'afficher.
#    b. Préparer l'historique et faire une requête HTTP POST vers f"{FASTAPI_URL}/chat"
#       avec le payload : {"message": user_prompt, "history": history_payload}
#    c. Récupérer la réponse JSON (ChatResponse) :
#       - response (str) : texte de réponse
#       - tool_called (bool) : indique si l'outil a été utilisé
#       - tool_results (list) : traces des outils
#    d. Afficher la réponse dans le chat assistant et ajouter au session_state.
#    e. Si tool_called est True, afficher un expander montrant les calculs effectués.
# ==============================================================================

def afficher_traces_outils(tool_results: list) -> None:
    """Affiche dans un expander les traces des outils utilises par l'agent."""
    with st.expander("Outils utilises par l'agent"):
        for i, trace in enumerate(tool_results, start=1):
            st.markdown(f"**Appel {i}**")
            st.code(str(trace), language="text")




# 1. Initialiser st.session_state["messages"] s'il n'existe pas encore.
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 2. Affichage des messages existants
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("tool_called") and msg.get("tool_results"):
            afficher_traces_outils(msg["tool_results"])

# 3. Saisie utilisateur: Récupérer la saisie utilisateur avec st.chat_input()
user_prompt = st.chat_input("Posez votre question a l'assistant...")


### 4. Gérer la saisie utilisateur et l'appel à l'API
if user_prompt:
    # Historique envoye a l'API (= tous les messages qui ont été envoyés)
    history_payload = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state["messages"]
    ]

    # 4a. Ajouter le message utilisateur dans st.session_state["messages"]
    st.session_state["messages"].append({"role": "user", "content": user_prompt})
    ## afficher le message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 4 b/c/d. Appel API et affichage de la reponse
    with st.chat_message("assistant"):
        try:
            # requête HTTP POST vers f"{FASTAPI_URL}/chat"
            # avec le payload : {"message": user_prompt, "history": history_payload}
            with st.spinner("L'agent reflechit..."):
                response = requests.post(
                    f"{FASTAPI_URL}/chat",
                    json={"message": user_prompt, "history": history_payload},
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()

            #    c. Récupérer la réponse JSON (ChatResponse) :
            #       - response (str) : texte de réponse
            #       - tool_called (bool) : indique si l'outil a été utilisé
            #       - tool_results (list) : traces des outils
            reponse_texte = data["response"]
            tool_called = data.get("tool_called", False)
            tool_results = data.get("tool_results", [])

            #Afficher la réponse dans le chat assistant et ajouter au session_state.
            st.markdown(reponse_texte)

            st.session_state["messages"].append(
                {
                    "role": "assistant",
                    "content": reponse_texte,
                    "tool_called": tool_called,
                    "tool_results": tool_results,
                }
            )
            
            # 4e. Si tool_called est True, afficher un expander montrant les calculs effectués. 
            if tool_called and tool_results:
                afficher_traces_outils(tool_results)

        ## Gérer les exceptions
        except requests.exceptions.ConnectionError:
            st.error(f"Impossible de joindre l'API ({FASTAPI_URL}). Verifiez que FastAPI est lance.")
        except requests.exceptions.Timeout:
            st.error("L'agent a mis trop de temps a repondre.")
        except requests.exceptions.HTTPError as e:
            st.error(f"Erreur renvoyee par l'API : {e}")
        except (KeyError, ValueError) as e:
            st.error(f"Reponse inattendue de l'API : {e}")

st.info("Ceci est un chat conversationnelle IA-TOS !")
