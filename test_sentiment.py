# test_sentiment.py
import pytest
from sentiment import score, classify


def test_score_positive():
    assert score("Eu amo este otimo e excelente produto") > 0


def test_score_negative():
    assert score("Este é o pior e terrivel serviço") < 0


def test_score_neutral():
    assert score("Esta é apenas uma mesa") == 0


def test_negation_inversion():
    assert score("Eu nao amo este filme") < 0


def test_classify_positive():
    assert classify("otimo excelente bom") == "positive"
