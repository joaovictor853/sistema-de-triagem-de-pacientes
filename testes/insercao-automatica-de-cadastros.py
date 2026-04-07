"""
   Irá fazer inserção de cadastros de forma automatizada. É um teste integral, então 
 usa a inserção é a mais crua possível.
"""
from subprocess import (Popen, PIPE, DEVNULL)
from os import (popen)
from sys import (executable as CAMINHO_DO_INTERPLETADOR_PYTHON)
from pprint import (pprint)
from random import (choice, randint)
from datetime import (datetime)

def lista_de_nomes() -> list[str]:
    "Retorna uma liista de nomes, estes que estão no arquivo de amostra."
    CAMINHO_AOS_NOMES = "dados/testes/lista-de-nomes.txt"
    nomes_arquivo = open(CAMINHO_AOS_NOMES, "rt", encoding="utf8")
    conteudo = nomes_arquivo.read().split('\n')
    
    nomes_arquivo.close()
    return conteudo
    
def seleciona_nome_aleatorio(nomes: list[str]) -> str:
    "Seleciona um nome, na lista de nome, de forma randomica."
    return choice(nomes).rstrip('\n')

def datetime_aleatorio() -> datetime:
    "Cria um 'datetime' aleatório. O período da data em específico vária de 1980 à o ano atual."
    ANO_ATUAL = datetime.today().year 
    
    return datetime(
        hour=randint(0, 23),
        minute=randint(0, 59),
        second=randint(0, 59),
        # O hospital existe desde a década de 80.
        year=randint(1980, ANO_ATUAL),
        month=randint(1, 12),
        day=randint(1, 28)
    )

def cria_cadastro_aleatorio() -> dict:
    """
    Cria todo um cadastro de forma aleatórios, tanto o nome, idade, nível de dor e data 
    de criação, assim como as vezes, modificações também.
    """
    nome = seleciona_nome_aleatorio(lista_de_nomes())
    criacao = datetime_aleatorio()
    modificacao = criacao 
    idade = randint(1, 70)
    nivel = randint(1, 5)

    return {
        f"{nome}": {
            "idade": idade,
            "estado": nivel,
            "criação": criacao,
            "modificação": modificacao
        }
    }

def executa_programa_e_adiciona_um_cadastro_no_momento(cadastro: dict) -> None:
    # Extraindo partes específicas ...
    tupla       = list(cadastro.items())[0]
    nome        = tupla[0]
    outros      = tupla[1]
    idade       = outros["idade"]
    nivel       = outros["estado"]
    # Valores desnecessários para este tipo de inserção. Entretanto, ficará aqui
    # para dizer que, estamos reutilizando a função que gera o um cadastro 
    # aleatório.
    criacao     = outros["criação"]
    modificacao = outros["modificação"]
    # Criando lista de argumentos para a inserção seriada, onde é preciso
    # transformar em string e formatar algumas variáveis. Como mostrado acima,
    # nem todos valores dado pelo dício serão usados. Este tipo de inserção cria  os 
    # selos de tempo no momento.
    ARGUMENTOS_COM_FIM_DE_LINHA = ["adicionar\n", f"{nome}\n", f"{idade}\n", f"{nivel}\n" ]
    processo = Popen(
        [CAMINHO_DO_INTERPLETADOR_PYTHON, "-OO", "-B", "main.py"], 
        stdin=PIPE, text=True, stdout=DEVNULL
    )
    
    for argumento in ARGUMENTOS_COM_FIM_DE_LINHA:
        processo.stdin.write(argumento)
        processo.stdin.flush()
    

# Cria um cadastro agora, inserindo nome, idade e nível de dor apenas.
executa_programa_e_adiciona_um_cadastro_no_momento(cria_cadastro_aleatorio())