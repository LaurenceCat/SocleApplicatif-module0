.. iatos_core documentation master file

Bienvenue sur la documentation technique de iatos_core
======================================================

.. image:: ../assets/1.png
   :width: 600
   :align: center
   :alt: Plateforme IA-TOS

Le package Python **iatos_core** constitue le socle applicatif métier du projet **IA-TOS (Intellicenter & Supervision de Microservices IA)**.

Il encapsule trois briques algorithmiques majeures :
1. **Scoring de Crédit Tabulaire** (`iatos_core.ml.scoring`) : Modèle Scikit-Learn de régression linéaire baseline entraîné sur 3 variables financières neutres.
2. **Analyse de Sentiment NLP** (`iatos_core.ml.sentiment`) : Analyseur lexical NLTK VADER pour classifier la polarité des avis clients.
3. **Agent Conversationnel Outillé** (`iatos_core.agent`) : Orchestration sous **LangGraph** reliée au LLM local **Qwen 2.5** via **Ollama**, intégrant un outil arithmétique déterministe (`iatos_core.tools`).

Ce package est conçu pour être consommé par une API REST (**FastAPI**) et visualisé via une interface utilisateur multi-pages (**Streamlit**).

.. toctree::
   :maxdepth: 2
   :caption: Guide Développeur:

   installation
   modules/scoring
   modules/sentiment
   modules/agent
   modules/tools
   modules/config_logging

Index et Recherche
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
