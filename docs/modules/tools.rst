Outils Déterministes (iatos_core.tools)
========================================

Présentation
------------
Le module ``iatos_core.tools`` contient les outils structurés déclarés avec le décorateur ``@tool`` de LangChain/LangGraph.

Outil Arithmétique : ``calculer``
---------------------------------
L'outil :func:`iatos_core.tools.math_tool.calculer` garantit une résolution mathématique exacte sans hallucination du LLM.

Opérations supportées :
* **Addition** : ``add``, ``addition``, ``+``
* **Soustraction** : ``sub``, ``soustraction``, ``-``
* **Multiplication** : ``mul``, ``multiplication``, ``*``
* **Division** : ``div``, ``division``, ``/`` (avec gestion sécurisée de la division par zéro)

Exemple d'Invocation Directe
----------------------------

.. code-block:: python

   from iatos_core.tools import calculer

   # Invocation via la méthode invoke() de LangChain
   result = calculer.invoke({"operation": "mul", "a": 150.0, "b": 4.0})
   print(result)
   # 'Le resultat de 150.0 * 4.0 est 600.0'

Référence de l'API
------------------

.. automodule:: iatos_core.tools.math_tool
   :members:
   :undoc-members:
   :show-inheritance:
