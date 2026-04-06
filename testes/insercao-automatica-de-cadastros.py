"""
   Irá fazer inserção de cadastros de forma automatizada. É um teste integral, então 
 usa a inserção é a mais crua possível.
"""
from subprocess import (Popen, PIPE, DEVNULL)
from sys import (executable as CAMINHO_DO_INTERPLETADOR_PYTHON)

TODAS_ENTRADAS = [
    # Escolha de opção.
    b"adicionar\n"
    # Dados cadastrais.
    b"Gustavo Almeida de Melo\n", b"17\n", b"5\n", 
    # Abandonar o programa.
    b"sair\n"
]
processo = Popen(
    [CAMINHO_DO_INTERPLETADOR_PYTHON, 
     "-OO", "-B", "main.py"], 
    stdin=PIPE
)

for arg in TODAS_ENTRADAS:
    processo.communicate(arg)

print(f"Resultado do comando executado: {processo.returncode}")
