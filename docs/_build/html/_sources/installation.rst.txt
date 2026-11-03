Installation & Prise en Main
=============================

Prérequis
---------
* Python 3.12 ou supérieur
* Ollama avec le modèle ``qwen2.5:7b`` (pour l'agent conversationnel)
* Gestionnaire d'environnement virtuel (``venv`` ou ``uv``)

Installation en mode éditable
-----------------------------
Pour installer le package dans votre environnement virtuel afin que toute modification de code soit immédiatement prise en compte :

.. code-block:: bash

   # Cloner le dépôt et se positionner à la racine
   git clone <URL_DU_DEPOT>
   cd 1_brief

   # Activer l'environnement virtuel
   source .venv/bin/activate  # Linux / macOS
   # .venv\Scripts\activate   # Windows

   # Installation en mode éditable
   pip install -e .

Vérification de l'installation
------------------------------
Dans un shell Python :

.. code-block:: python

   import iatos_core
   print(iatos_core.__version__)
   # Sortie attendue : '0.1.0'
