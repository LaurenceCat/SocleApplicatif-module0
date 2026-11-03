Analyse de Sentiment (iatos_core.ml.sentiment)
==============================================

Présentation & Contexte NLP
---------------------------
Le module ``iatos_core.ml.sentiment`` implémente la classe :class:`SentimentAnalyzer`, qui exploite la méthode lexicale **NLTK VADER** (*Valence Aware Dictionary and sEntiment Reasoner*) pour quantifier la tonalité d'un message textuel ou d'un retour client.

.. note::
   **Perspective Pédagogique M0 vers M4 :**
   Cette approche lexicale par dictionnaire constitue notre baseline initiale de traitement du langage naturel. Dans les modules ultérieurs, elle sera comparée puis surclassée par des modèles de **Transformers pré-entraînés** (CamemBERT, RoBERTa) et des adaptateurs **LoRA (PEFT)**.

Indicateurs & Règles de Classification
--------------------------------------
La méthode :meth:`SentimentAnalyzer.analyze` retourne quatre indicateurs numériques :

1. ``compound`` (*float*) : Métrique synthétique normalisée entre **-1.0** (négativité absolue) et **+1.0** (positivité absolue).
2. ``pos`` (*float*) : Proportion de termes à valence positive (0.0 à 1.0).
3. ``neu`` (*float*) : Proportion de termes neutres (0.0 à 1.0).
4. ``neg`` (*float*) : Proportion de termes à valence négative (0.0 à 1.0).

Seuils de classification officielle :
* **Compound >= +0.05** : Label **Positif**.
* **-0.05 < Compound < +0.05** : Label **Neutre**.
* **Compound <= -0.05** : Label **Négatif**.

Exemple d'Utilisation
---------------------

.. code-block:: python

   from iatos_core.ml.sentiment import SentimentAnalyzer

   analyzer = SentimentAnalyzer()
   result = analyzer.analyze("The response time was fast and the team was really helpful!")

   print(result)
   # {
   #     'texte': 'The response time was fast and the team was really helpful!',
   #     'compound': 0.735,
   #     'label': 'Positif',
   #     'scores': {'neg': 0.0, 'neu': 0.449, 'pos': 0.551, 'compound': 0.735},
   #     'type_modele': 'NLTK VADER (Baseline Lexicale M0)'
   # }

Référence de l'API
------------------

.. automodule:: iatos_core.ml.sentiment
   :members:
   :undoc-members:
   :show-inheritance:
