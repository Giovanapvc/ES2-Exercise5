# sentiment.py
import re
import os
import unicodedata

# Conjunto de negações em português (normalizados para sem acentos)
NEGATIONS = {"nao", "nunca", "jamais", "sem"}

# Valor mínimo absoluto para considerar como sentimento
threshold = 1.0


def normalize_word(word: str) -> str:
    """
    Remove acentos e normaliza para lowercase.
    """
    nfkd = unicodedata.normalize('NFKD', word)
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).lower()


def tokenize(text: str) -> list[str]:
    """
    Quebra o texto em tokens de palavras, removendo pontuação.
    """
    return re.findall(r"\b[\wçãõáéíóúü]+\b", text.lower())


def load_lexicon(path: str = "lexicons") -> dict[str, float]:
    """
    Lê um arquivo de léxico ou vários arquivos numa pasta.
    Procura por 'path' na ordem: CWD e diretório do módulo.
    Formato por linha: 'palavra pontuacao ...'.
    Retorna mapa palavra(normalizada)->float(pontuação).
    """
    lex = {}
    possible_paths = [path, os.path.join(os.path.dirname(__file__), path)]
    if not path.endswith('.txt'):
        possible_paths.append(path + '.txt')
        possible_paths.append(os.path.join(os.path.dirname(__file__), path + '.txt'))

    files = []
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
    """
    Soma valores do léxico, invertendo quando precedidos por negação.
    Aplica fallback: se token termina em 'o' ou 'a', tenta + 'r'.
    Ignora valores absolutos abaixo de threshold.
    """
    tokens = tokenize(text)
    total = 0.0
    negate = False
    for token in tokens:
        norm = normalize_word(token)
        if norm in NEGATIONS:
            negate = True
            continue
        # busca direta
        val = LEXICON.get(norm, None)
        # fallback para verbos: amo->amor
        if val is None and norm.endswith(('o', 'a')):
            val = LEXICON.get(norm + 'r', 0.0)
        if val is None:
            val = 0.0
        # threshold
        if abs(val) < threshold:
            val = 0.0
        # aplicação de negação
        if negate:
            val = -val
            negate = False
        total += val
    return total


def classify(text: str) -> str:
    """
    Classifica o texto como 'positive', 'negative' ou 'neutral'.
    """
    s = score(text)
    if s > 0:
        return "positive"
    elif s < 0:
        return "negative"
    else:
        return "neutral"