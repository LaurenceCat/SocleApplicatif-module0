"""Outil deterministe de calcul arithmetique pour agent conversationnel."""

from langchain_core.tools import tool
from iatos_core.logger import logger


@tool
def calculer(operation: str, a: float, b: float) -> str:
    """Effectue une operation arithmetique de base entre deux nombres.
    
    Args:
        operation: Type d'operation ('add', 'sub', 'mul', 'div', '+', '-', '*', '/').
        a: Premier nombre operande.
        b: Second nombre operande.
        
    Returns:
        Resultat formate sous forme de chaine explicite.
    """
    logger.info("Execution du tool calculer : op='{op}', a={a}, b={b}", op=operation, a=a, b=b)
    op = operation.strip().lower()

    if op in ("add", "addition", "+"):
        res = a + b
        msg = f"Le resultat de {a} + {b} est {res}"
    elif op in ("sub", "soustraction", "-"):
        res = a - b
        msg = f"Le resultat de {a} - {b} est {res}"
    elif op in ("mul", "multiplication", "*"):
        res = a * b
        msg = f"Le resultat de {a} * {b} est {res}"
    elif op in ("div", "division", "/"):
        if b == 0:
            logger.warning("Tentative de division par zero detectee pour a={a}", a=a)
            return "Erreur : division par zero impossible."
        res = a / b
        msg = f"Le resultat de {a} / {b} est {res}"
    else:
        logger.error("Operation non reconnue recue : '{op}'", op=operation)
        return f"Erreur : operation '{operation}' non reconnue. Choisir parmi add, sub, mul, div."

    logger.success("Calcul termine avec succes : {msg}", msg=msg)
    return msg
