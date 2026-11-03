Configuration & Journalisation (iatos_core.config & logger)
=============================================================

Configuration Centralisée (iatos_core.config)
---------------------------------------------
Le module ``config`` centralise les chemins des fichiers et les variables d'environnement.

Variables d'Environnement Reconnues :
* ``OLLAMA_BASE_URL`` : URL du serveur Ollama (défaut : ``http://localhost:11434``).
* ``OLLAMA_MODEL`` : Nom du modèle Ollama (défaut : ``qwen2.5:7b``).
* ``FASTAPI_BACKEND_URL`` : URL cible pour les clients HTTP (défaut : ``http://localhost:8000``).
* ``API_PORT`` : Port d'écoute de l'API (défaut : ``8000``).

Journalisation Industrielle (iatos_core.logger)
-----------------------------------------------
Le module ``logger`` configure une instance unifiée de **Loguru** avec deux puits de sortie (*sinks*) :

1. **Sortie Console (stderr)** : Format compact, horodaté et coloré par niveau d'importance (``INFO``, ``SUCCESS``, ``WARNING``, ``ERROR``).
2. **Sortie Fichier Rotatif** : Écriture dans ``logs/iatos_service.log`` avec rotation automatique à **10 Mo** et rétention de **14 jours**.

Exemple d'Utilisation :

.. code-block:: python

   from iatos_core.logger import logger

   logger.info("Traitement de la requête initié.")
   logger.success("Modèle exécuté avec succès.")
   logger.error("Échec de la connexion à la base.")
