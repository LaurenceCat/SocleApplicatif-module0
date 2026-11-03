Scoring de Crédit (iatos_core.ml.scoring)
=========================================

Présentation & Contexte Métier
------------------------------
Le module ``iatos_core.ml.scoring`` implémente la classe :class:`CreditScoringPredictor`, chargée d'évaluer le risque d'octroi de crédit à partir d'un modèle de régression linéaire Scikit-Learn.

.. note::
   **Raison d'être de la baseline M0 :**
   Ce modèle est volontairement bridé à trois variables financières neutres. Le dataset d'origine (``data/credit_risk_dataset.csv``) comporte 17 colonnes dont des attributs sensibles (âge, sexe, nationalité, statut marital). Ces colonnes sont réservées pour le **Module 2**, où les apprenants réaliseront un audit d'équité algorithmique, calculeront le **Disparate Impact** et mettront en œuvre des techniques de mitigation des biais et d'anonymisation RGPD.

Variables d'Entrée (Features)
-----------------------------
Le modèle n'accepte strictement que 3 caractéristiques numériques :

1. ``montant_demande`` (*float*) : Montant sollicité en euros (ex: 15 000 €).
2. ``duree_mois`` (*int*) : Durée de remboursement en mois (ex: 36 mois).
3. ``revenu_mensuel`` (*float*) : Revenu mensuel net de l'emprunteur (ex: 3 200 €).

Échelle du Score & Règles de Décision
-------------------------------------
Le score brut prédit par la régression linéaire est automatiquement borné entre **300.0** et **850.0** points (échelle standard de solvabilité bancaire type FICO) :

* **Score >= 650.0 points** : Décision **Favorable** (profil solide, solvabilité satisfaisante).
* **550.0 <= Score < 650.0 points** : Décision **Ajourné / Examen Approfondi** (profil intermédiaire nécessitant des pièces complémentaires).
* **Score < 550.0 points** : Décision **Défavorable** (tension financière avérée).

Exemple d'Utilisation
---------------------

.. code-block:: python

   from iatos_core.ml.scoring import CreditScoringPredictor

   # Instanciation (chargement unique du fichier .joblib)
   predictor = CreditScoringPredictor()

   # Prédiction
   result = predictor.predict(
       montant_demande=12000.0,
       duree_mois=24,
       revenu_mensuel=3500.0,
   )

   print(result)
   # {
   #     'score': 685.4,
   #     'decision': 'Favorable',
   #     'motif': 'Profil solide avec capacite de remboursement estimee satisfaisante.',
   #     'features_utilisees': {'montant_demande': 12000.0, 'duree_mois': 24, 'revenu_mensuel': 3500.0},
   #     'type_modele': 'Regression Lineaire Scikit-Learn (Baseline M0)'
   # }

Référence de l'API
------------------

.. automodule:: iatos_core.ml.scoring
   :members:
   :undoc-members:
   :show-inheritance:
