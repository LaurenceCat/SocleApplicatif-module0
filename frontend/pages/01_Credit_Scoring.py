"""Page 1 : Formulaire de Scoring de Credit (Baseline Regression Lineaire M0).

Starter Kit Apprenants - Brief 1 IA-TOS.
"""

import os

import requests
import streamlit as st

FASTAPI_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Scoring Credit | Brief 1",
    page_icon="💳",
    layout="wide",
)

st.title("Page 1 : Formulaire Predictif de Scoring de Credit")
st.markdown("""
Cette page interroge le microservice de scoring de credit base sur une **Regression Lineaire Scikit-Learn** 
entrainee sur les 3 variables financieres neutres du dossier (`montant_demande`, `duree_mois`, `revenu_mensuel`).
""")

st.info("""
**Note d'architecture pedagogique (M0)** : Ce modele est restreint a 3 variables neutres. 
Le dataset complet contient des variables demographiques et contextuelles qui serviront au **Module 2** 
pour realiser l'audit d'equite algorithmique (Disparate Impact), l'anonymisation RGPD et la mitigation des biais.
""")

# ==============================================================================
# TODO (Apprenants) : Implémenter le formulaire Streamlit et l'appel API
#
# Étapes suggérées :
# 1. Créer un formulaire avec st.form("form_credit").
# 2. Ajouter les champs de saisie :
#    - montant_demande (st.number_input, ex: 1000 à 50000 €)
#    - duree_mois (st.slider, ex: 6 à 84 mois)
#    - revenu_mensuel (st.number_input, ex: 500 à 20000 €)
#    - bouton de soumission (st.form_submit_button)
# 3. Lors de la soumission du formulaire :
#    a. Émettre un POST vers f"{FASTAPI_URL}/predict/credit" avec le payload JSON :
#       {"montant_demande": float, "duree_mois": int, "revenu_mensuel": float}
#    b. Récupérer la réponse JSON (CreditPredictResponse) contenant :
#       - score (float entre 300 et 850)
#       - decision (str : 'Favorable', 'Ajourne / Examen Approfondi', 'Defavorable')
#       - seuil_recommande (float)
#       - model_version (str)
#    c. Restituer visuellement le score (ex: st.metric, jauge de progression, couleur de badge).
# ==============================================================================



# 1. Créer un formulaire avec st.form("form_credit").
# 2. Ajouter les champs de saisie :
#    - montant_demande (st.number_input, ex: 1000 à 50000 €)
#    - duree_mois (st.slider, ex: 6 à 84 mois)
#    - revenu_mensuel (st.number_input, ex: 500 à 20000 €)
#    - bouton de soumission (st.form_submit_button)
with st.form("form_credit"):
    col1, col2 = st.columns(2)

    with col1:
        montant_demande = st.number_input(
            "Montant demande (€)",
            min_value=1000.0,
            max_value=50000.0,
            value=10000.0,
            step=500.0,
        )
        duree_mois = st.slider(
            "Duree du pret (mois)",
            min_value=6,
            max_value=84,
            value=36,
            step=6,
        )

    with col2:
        revenu_mensuel = st.number_input(
            "Revenu mensuel (€)",
            min_value=500.0,
            max_value=20000.0,
            value=2500.0,
            step=100.0,
        )

    submitted = st.form_submit_button("Calculer le score", type="primary")
    
    
# 3. Lors de la soumission du formulaire
if submitted:
    payload = {
        "montant_demande": float(montant_demande),
        "duree_mois": int(duree_mois),
        "revenu_mensuel": float(revenu_mensuel),
    }

    try:
        with st.spinner("Calcul du score en cours..."):
            #    a. Émettre un POST vers f"{FASTAPI_URL}/predict/credit" avec le payload JSON :
            #       {"montant_demande": float, "duree_mois": int, "revenu_mensuel": float}
            response = requests.post(
                f"{FASTAPI_URL}/predict/credit",
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()


        #    b. Récupérer la réponse JSON (CreditPredictResponse) contenant :
        #       - score (float entre 300 et 850)
        #       - decision (str : 'Favorable', 'Ajourne / Examen Approfondi', 'Defavorable')
        #       - seuil_recommande (float) ??
        #       - model_version (str) ??
        ### incohérence entre le commentaire et la réponse réelle de l'API??
        score = data["score"]
        decision = data["decision"]
        motif = data["motif"]
        features_utilisees = data["features_utilisees"]
        type_modele = data["type_modele"]

        st.subheader("Resultat")




        #    c. Restituer visuellement le score (ex: st.metric, jauge de progression, couleur de badge).
        # Score, decision et modele utilise
        m1, m2, m3 = st.columns(3)
        m1.metric("Score de credit", f"{score:.0f}")
        m2.metric("Decision", decision)
        m3.metric("Modele utilise", type_modele)
        st.caption(f"Motif : {motif}")
        st.markdown("**Features utilisees**")
        for feature, value in features_utilisees.items():
            st.write(f"- {feature} : {value}")

        # Jauge de progression (score ramene de 300-850 vers 0-1)
        progression = min(max((score - 300) / (850 - 300), 0.0), 1.0)
        st.progress(progression, text=f"Score : {score:.0f} / 850")

        # Badge colore selon la decision
        if decision == "Favorable":
            st.success(f"Decision : {decision}")
        elif decision == "Defavorable":
            st.error(f"Decision : {decision}")
        else:
            st.warning(f"Decision : {decision}")



    # Gestion des exceptions
    except requests.exceptions.ConnectionError:
        st.error(f"Impossible de joindre l'API ({FASTAPI_URL}). Verifiez que FastAPI est lance.")
    except requests.exceptions.Timeout:
        st.error("L'API a mis trop de temps a repondre.")
    except requests.exceptions.HTTPError as e:
        st.error(f"Erreur renvoyee par l'API : {e}")
    except (KeyError, ValueError) as e:
        st.error(f"Reponse inattendue de l'API : {e}")



st.info("Ceci est un formulaire et un affichage des predictions de credit IA-TOS")
