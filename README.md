## Exercício 5 - Engenharia de Software 2

O código sentiment.py implementa um analisador de sentimento simplificado em português, baseado em um léxico de palavras com pontuações reais carregado de um arquivo ou pasta chamada lexicons, diretamente utilizada a partir dos léxicos de análise de uma versão em português brasileiro da técnica VADER, disponível em: https://github.com/rafjaa/LeIA

O código carrega automaticamente o arquivo lexicons, normaliza e tokeniza o texto removendo acentos e pontuação, aplica negações (“nao”, “sem” etc.) e um fallback morfológico simples (ex.: “amo” para “amor”) para computar um score numérico, e finalmente classifica o resultado em “positive”, “negative” ou “neutral”. Os cinco testes em pytest cobrem os casos de frases com polaridade positiva, negativa, sem termos de sentimento e checam se a negação inverte corretamente o valor, além de validar a saída da função classify.
