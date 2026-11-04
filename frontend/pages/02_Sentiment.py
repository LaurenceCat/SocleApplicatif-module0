"""Page 2 : Analyseur de Sentiment (Baseline Lexicale NLTK VADER M0).

Starter Kit Apprenants - Brief 1 IA-TOS.
"""

import os

import requests
import streamlit as st

FASTAPI_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Analyse de Sentiment | Brief 1",
    page_icon="💬",
    layout="wide",
)

st.title("Page 2 : Analyseur de Sentiment des Retours Clients")
st.markdown("""
Cette page interroge le microservice NLP d'analyse de polarite base sur la methode lexicale 
**NLTK VADER** (`SentimentIntensityAnalyzer`).
""")

st.info("""
**Note d'architecture pedagogique (M0)** : Cette approche par dictionnaire lexical constitue notre 
baseline de depart. Elle sera confrontee puis remplacee dans les modules suivants par des modeles 
de Transformers pre-entraines en francais (**CamemBERT / RoBERTa**) et du Fine-Tuning LoRA (PEFT).
""")

# ==============================================================================
# TODO (Apprenants) : Implémenter la saisie textuelle et l'appel API
#
# Étapes suggérées :
# 1. Proposer une zone de saisie texte avec st.text_area().
# 2. Optionnel : Proposer des boutons de texte d'exemples (positif, négatif, neutre).
# 3. Ajouter un bouton d'action avec st.button("Analyser la polarité").
# 4. Lors du clic :
#    a. Émettre un POST vers f"{FASTAPI_URL}/predict/sentiment" avec le payload JSON :
#       {"texte": texte_saisi}
#    b. Récupérer la réponse JSON (SentimentPredictResponse) contenant :
#       - label (str : 'Positif', 'Neutre', 'Negatif')
#       - compound (float entre -1.0 et 1.0)
#       - details (dict avec 'pos', 'neu', 'neg')
#       - method (str)
#    c. Restituer le résultat avec des composants visuels adaptés (st.metric, st.progress, etc.).
# ==============================================================================


EXEMPLES = {
    "Positif": "The service was excellent and the staff were incredibly helpful!",
    "Negatif": "This was a terrible experience, I am very disappointed and angry.",
    "Neutre": "I received the package on Tuesday and it contained two items.",
}

# Initialisation du texte dans l'etat de session
if "texte_saisi" not in st.session_state:
    st.session_state["texte_saisi"] = ""


def charger_exemple(cle: str) -> None:
    """Callback : remplit la zone de texte avec un exemple."""
    st.session_state["texte_saisi"] = EXEMPLES[cle]


st.caption("Exemples rapides (VADER est entraine pour l'anglais) :")
c1, c2, c3 = st.columns(3)
c1.button("Exemple positif", on_click=charger_exemple, args=("Positif",), use_container_width=True)
c2.button("Exemple negatif", on_click=charger_exemple, args=("Negatif",), use_container_width=True)
c3.button("Exemple neutre", on_click=charger_exemple, args=("Neutre",), use_container_width=True)

texte = st.text_area(
    "Retour client a analyser",
    key="texte_saisi",
    height=150,
    placeholder="Saisissez ou collez un retour client...",
)

if st.button("Analyser la polarité", type="primary"):
    if not texte.strip():
        st.warning("Veuillez saisir un texte avant de lancer l'analyse.")
    else:
        try:
            with st.spinner("Analyse en cours..."):
                response = requests.post(
                    f"{FASTAPI_URL}/predict/sentiment",
                    json={"texte": texte},
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()

            label = data["label"]
            compound = data["compound"]
            scores = data["scores"]
            type_modele = data["type_modele"]

            st.subheader("Resultat")

            m1, m2, m3 = st.columns(3)
            m1.metric("Polarite", label)
            m2.metric("Score compound", f"{compound:+.3f}")
            m3.metric("Modele", type_modele)

            # Badge colore selon le label
            if label == "Positif":
                st.success(f"Sentiment : {label}")
            elif label == "Negatif":
                st.error(f"Sentiment : {label}")
            else:
                st.info(f"Sentiment : {label}")

            # Jauge compound : ramene de [-1, 1] vers [0, 1]
            st.progress(
                min(max((compound + 1) / 2, 0.0), 1.0),
                text=f"Compound : {compound:+.3f} (de -1 a +1)",
            )

            # Repartition pos / neu / neg
            st.markdown("**Repartition des polarites**")
            p1, p2, p3 = st.columns(3)
            p1.metric("Positif", f"{scores.get('pos', 0):.1%}")
            p2.metric("Neutre", f"{scores.get('neu', 0):.1%}")
            p3.metric("Negatif", f"{scores.get('neg', 0):.1%}")

            st.bar_chart(
                {
                    "Proportion": {
                        "Positif": scores.get("pos", 0),
                        "Neutre": scores.get("neu", 0),
                        "Negatif": scores.get("neg", 0),
                    }
                }
            )

        except requests.exceptions.ConnectionError:
            st.error(f"Impossible de joindre l'API ({FASTAPI_URL}). Verifiez que FastAPI est lance.")
        except requests.exceptions.Timeout:
            st.error("L'API a mis trop de temps a repondre.")
        except requests.exceptions.HTTPError as e:
            st.error(f"Erreur renvoyee par l'API : {e}")
        except (KeyError, ValueError) as e:
            st.error(f"Reponse inattendue de l'API : {e}")
            

st.info("Ceci est un analyseur de sentiment et un affichage des metriques NLP IA-TOS")
