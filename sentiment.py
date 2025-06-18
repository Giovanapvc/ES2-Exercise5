# sentiment.py
import re
import os
import unicodedata
from typing import List, Dict

# Conjunto de negações em português (normalizados para sem acentos)
NEGATIONS = {"nao", "nunca", "jamais", "sem"}

# Valor mínimo absoluto para considerar como sentimento
threshold = 1.0


def normalize_word(word: str) -> str:
    nfkd = unicodedata.normalize('NFKD', word)
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).lower()


def tokenize(text: str) -> List[str]:
    return re.findall(r"\b[\wçãõáéíóúü]+\b", text.lower())


def load_lexicon(path: str = "lexicons") -> Dict[str, float]:
    lex: Dict[str, float] = {}
    possible_paths = [path, os.path.join(os.path.dirname(__file__), path)]
    if not path.endswith('.txt'):
        possible_paths += [path + '.txt', os.path.join(os.path.dirname(__file__), path + '.txt')]

    files: List[str] = []
    for p in possible_paths:
        if os.path.isdir(p):
            for f in os.listdir(p):
                full = os.path.join(p, f)
                if os.path.isfile(full):
                    files.append(full)
            break
        elif os.path.isfile(p):
            files.append(p)
            break

    if not files:
        raise FileNotFoundError(f"Léxico não encontrado em: {possible_paths}")

    for fpath in files:
        with open(fpath, encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    key = normalize_word(parts[0])
                    try:
                        score_val = float(parts[1])
                    except ValueError:
                        continue
                    lex[key] = score_val
    return lex

# Carrega léxico global na importação do módulo
LEXICON = load_lexicon()


def score(text: str) -> float:
    tokens = tokenize(text)
    total = 0.0
    negate = False
    for token in tokens:
        norm = normalize_word(token)
        if norm in NEGATIONS:
            negate = True
            continue
        val = LEXICON.get(norm)
        if val is None and norm.endswith(('o', 'a')):
            val = LEXICON.get(norm + 'r')
        if val is None:
            val = 0.0
        if abs(val) < threshold:
            val = 0.0
        if negate:
            val = -val
            negate = False
        total += val
    return total


def classify(text: str) -> str:
    s = score(text)
    if s > 0:
        return "positive"
    elif s < 0:
        return "negative"
    else:
        return "neutral"