"""Tests unitaires pour l'outil mathematique 'calculer'."""

from iatos_core.tools.math_tool import calculer


def test_calculer_addition():
    res = calculer.invoke({"operation": "add", "a": 12.0, "b": 8.0})
    assert "20.0" in res or "20" in res
    assert "resultat" in res.lower()


def test_calculer_soustraction():
    res = calculer.invoke({"operation": "sub", "a": 50.0, "b": 15.0})
    assert "35.0" in res or "35" in res


def test_calculer_multiplication():
    res = calculer.invoke({"operation": "mul", "a": 7.0, "b": 6.0})
    assert "42.0" in res or "42" in res


def test_calculer_division():
    res = calculer.invoke({"operation": "div", "a": 100.0, "b": 4.0})
    assert "25.0" in res or "25" in res


def test_calculer_division_par_zero():
    res = calculer.invoke({"operation": "div", "a": 10.0, "b": 0.0})
    assert "division par zero impossible" in res.lower()


def test_calculer_operation_invalide():
    res = calculer.invoke({"operation": "puissance", "a": 2.0, "b": 3.0})
    assert "non reconnue" in res.lower()
