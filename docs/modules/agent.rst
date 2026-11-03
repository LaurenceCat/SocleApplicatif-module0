Agent LangGraph (iatos_core.agent)
===================================

Architecture de l'Agent Conversationnel
---------------------------------------
Le module ``iatos_core.agent`` orchestre un agent ReAct sous **LangGraph** connecté au LLM open-weights **Qwen 2.5 (7B)** via l'instance locale **Ollama**.

L'agent dispose d'une invite système (*system prompt*) lui ordonnant de déléguer systématiquement tout calcul arithmétique (addition, soustraction, multiplication, division) au tool déterministe dédié :func:`iatos_core.tools.math_tool.calculer`.

Structure de l'Historique de Discussion (``history``)
-----------------------------------------------------
La fonction principale :func:`iatos_core.agent.graph.run_agent_message` accepte l'historique conversationnel sous forme d'une liste de dictionnaires standards :

.. code-block:: python

   history = [
       {"role": "user", "content": "Bonjour !"},
       {"role": "assistant", "content": "Bonjour, comment puis-je vous aider ?"},
   ]

.. tip::
   **Conversion depuis Pydantic dans FastAPI :**
   Si votre route FastAPI reçoit un payload contenant une liste d'objets Pydantic (ex: ``payload.history`` avec chaque objet ayant ``m.role`` et ``m.content``), vous devez simplement la convertir en liste de dictionnaires avec une compréhension de liste :
   
   .. code-block:: python

      history_dicts = [{"role": m.role, "content": m.content} for m in payload.history]

Format du Résultat Retourné
---------------------------
La fonction retourne un dictionnaire contenant les clés suivantes :

* ``success`` (*bool*) : Vaut ``True`` si la génération s'est déroulée normalement, ``False`` si Ollama est indisponible ou en erreur.
* ``response`` (*str*) : Le texte final généré par le modèle en langage naturel.
* ``tool_called`` (*bool*) : Vaut ``True`` si l'agent a invoqué un outil externe lors de son tour de parole, ``False`` sinon.
* ``tool_results`` (*list[str]*) : Liste des sorties brutes retournées par les outils exécutés.

Exemple d'Utilisation
---------------------

.. code-block:: python

   from iatos_core.agent import run_agent_message

   res = run_agent_message(
       user_message="Combien font 4500 divisé par 12 ?",
       history=[],
   )

   print(res["response"])
   # 'Le résultat de 4500 divisé par 12 est 375.'

   print(res["tool_called"])
   # True

   print(res["tool_results"])
   # ['Le resultat de 4500.0 / 12.0 est 375.0']

Référence de l'API
------------------

.. automodule:: iatos_core.agent.graph
   :members:
   :undoc-members:
   :show-inheritance:
