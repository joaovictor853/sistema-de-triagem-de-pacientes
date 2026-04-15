"""
  Funções de cunho totalmente de computar valores, e então retornar-los residirão
  neste módulo.
"""
# Módulos pro próprio projeto:
from bancodedados import (
    adiciona_cadastro, carrega_banco_de_dados, salva_banco_de_dados, 
    todos_cadastros, busca_cadastro
    )
from modelos import (criacao_cadastro)


def cadastro_mais_antigo_realizado() -> dict:
    "Encontra o paciente mais velho que frequentou aqui. Esteja ele vivo ou não."
    BANCO = todos_cadastros()
    TOTAL_DE_CADASTROS = len(BANCO)
    assert (TOTAL_DE_CADASTROS > 0)

    maximo = BANCO[0]

    for cadastro in BANCO[1:]:
        a = criacao_cadastro(maximo)
        b = criacao_cadastro(cadastro)

        if b > a:
            maximo = cadastro

    return maximo
        
def cadastro_mais_recente_realizado() -> dict:
    "Acha o paciente mais recente que chegou ao hospital."
    BANCO = todos_cadastros()
    TOTAL_DE_CADASTROS = len(BANCO)
    assert (TOTAL_DE_CADASTROS > 0)

    minimo = BANCO[0]

    for cadastro in BANCO[1:]:
        a = criacao_cadastro(minimo)
        b = criacao_cadastro(cadastro)

        if b < a:
            minimo = cadastro

    return minimo

def computa_a_distribuicao_da_triagem() -> dict:
    "Faz a divisão de frações do estado de cada paciente cadastrado no hospital."
    lista = todos_cadastros()
    distribuicao = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for cadastro in lista:
        indice = nivel_de_dor_cadastro(cadastro)
        distribuicao[indice] += 1
    
    total = sum(distribuicao.values())

    # Convertendo tudo em percentuais.
    for indice in range(1, 5 + 1):
        contagem = distribuicao[indice]
        distribuicao[indice] = contagem / total
    return distribuicao
      
def media_de_idade() -> int:
    "Calcula a média de idade dos pacientes cadastrados."
    lista_completa = todos_cadastros()
    quantidade = len(lista_completa)
    
    return int(sum(map(idade_cadastro, lista_completa)) / quantidade)


