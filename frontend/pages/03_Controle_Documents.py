"""Page 3 : Controle de Documents (Vision CLIP).

Starter Kit Apprenants - Brief 3 IA-TOS.
"""

import os

import requests
import streamlit as st

FASTAPI_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Controle de Documents | Brief 3",
    page_icon="💬",
    layout="wide",
)

st.title("Page 3 : Controle de Documents")
st.markdown("""
Cette page interroge le microservice d'analyse de documents.
""")

# ==============================================================================
# Implémenter l'upload de fichier et l'appel API
#
# Étapes suggérées :
# 1. Proposer une zone d'upload de fichier avec st.file_uploader().
# 2. Ajouter un bouton d'action avec st.button("Analyser le document").
# 3. Lors du clic :
#    a. Émettre un POST vers f"{FASTAPI_URL}/vision/classify-document"
#    b. Récupérer la réponse JSON (DocumentClassificationResponse) 
#    c. Restituer le résultat avec des composants visuels adaptés (st.metric, st.progress, etc.).
# ==============================================================================

## Choix de l'image par l'utilisateur
uploaded_file = st.file_uploader(
    "Choisissez un fichier", type=["png", "jpg", "jpeg", "pdf"]
)

## Prévisualisation de l'image si c'est un fichier image
if uploaded_file is not None:  # noqa: SIM102
    if uploaded_file.type.startswith("image/"):
        st.image(uploaded_file, caption="Prévisualisation de l'image")


## Envoi de l'image au backend FastAPI pour l'upload puis analyse du document
if st.button("Analyser la nature du document", type="primary"):
    if not uploaded_file:
        st.warning("Veuillez sélectionner un fichier avant de lancer l'analyse.")
    else:
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
        }
        try:
            with st.spinner("Analyse en cours..."):
                #    a. Émettre un POST vers f"{FASTAPI_URL}/vision/classify-document" avec le doc JSON
                
                #[Gestion des URLs] Ne codez JAMAIS l'URL 'http://localhost:8000' en dur dans le code de vos pages ! Déclarez une variable d'environnement : FASTAPI_URL = os.getenv('FASTAPI_BACKEND_URL', 'http://localhost:8000'). 
                # En local, elle pointera vers localhost. Dans Docker, elle pointera vers le conteneur http://backend:8000
                
                response = requests.post(
                    f"{FASTAPI_URL}/vision/classify-document",
                    files=files,
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()

            #b. Récupérer la réponse JSON (DocumentPredictResponse) contenant :
            #       - filename (str : "specimen_rib.jpg")
            #       - detected_document (str : "bank statement")
            #       - confidence (float: 0,784)
            #       - candidates (List[Dict[str, float]]: 
            #     [ {"label": "bank statement", "score": 0.784},
            #     {"label": "identity card", "score": 0.121},
            #     {"label": "bank check", "score": 0.082},
            #     {"label": "blank paper", "score": 0.013} ] )
            filename = data["filename"]
            detected_document = data["detected_document"]
            confidence = data["confidence"]
            candidates = data["candidates"]

            st.subheader("Resultat")

            #c. Restituer le résultat avec des composants visuels adaptés (st.metric, st.progress, etc.).
            # badge de validation de conformité et jauge de confiance.
            st.metric(label="Document détecté", value=detected_document)
            st.progress(confidence)
            
            # Afficher la confidence avec le libellé "Confiance" puis la valeur puis la jauge de progression.
            st.metric(label="Confiance", value=f"{confidence:.2f}")
            st.write("Candidats :")
            for candidate in candidates:
                st.write(f"{candidate['label']}: {candidate['score']:.2f}") 


        # Gestion des exceptions
        except requests.exceptions.ConnectionError as e:
            st.error(f"Impossible de joindre l'API ({FASTAPI_URL}). Détail : {e}")
        except requests.exceptions.Timeout:
            st.error("L'API a mis trop de temps a repondre.")
        except requests.exceptions.HTTPError as e:
            st.error(f"Erreur renvoyee par l'API : {e}")
        except (KeyError, ValueError) as e:
            st.error(f"Reponse inattendue de l'API : {e}")
                       

st.info("Ceci est un analyseur documents IA-TOS")
