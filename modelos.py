# Biblioteca padrão do Python:
from datetime import (datetime, timedelta)
from unittest import (TestCase)
from pprint import (pprint as PPrint)

def cadastro_e_valido(cadastro: dict) -> bool:
    """
    Como o cadastro é um dicionário, e o polimorfismo do Python aceita qualquer coisa
    esta função cuida de validar apenas dicionário que representam um cadastro de fato.
    """
    # Atribuição da chave nome, supostamente a única chave no dicionário passado.
    for chave in cadastro:
        nome = chave

    CHAVES = cadastro[nome].keys()
    subdicio = cadastro[nome]
    # Há uma chave(o nome), e quatro chave-valor no dicionário desta chave.
    sem_excesso = (len(subdicio) == 4 and len(cadastro) == 1)
    
    if (not sem_excesso):
        return False
    
    tem_todos_campos = (
        # Verifica se há as chaves específicas aqui.
        "idade"        in CHAVES  and
        "estado"       in CHAVES  and
        "criação"      in CHAVES  and
        "modificação"  in CHAVES
    )
    sao_dos_tipos_correspondentes = (
        # Elas são dos tipos atestados. 
        isinstance(subdicio["idade"], int)              and
        isinstance(subdicio["estado"], int)             and
        isinstance(subdicio["criação"], datetime)       and
        isinstance(subdicio["modificação"], datetime)   
    )
    
    
    return tem_todos_campos and sao_dos_tipos_correspondentes

def cria_cadastro(nome: str, idade: int, nivel: int, criacao: datetime, modificacao: datetime) -> dict:
    "Cria uma instância do que será amarzenado no banco de dados no final."
    assert isinstance(nome, str)
    assert isinstance(idade, int)
    assert isinstance(nivel, int)
    assert isinstance(criacao, datetime)
    assert isinstance(modificacao, datetime)
    # Não podem referenciar o mesmo objeto.
    assert criacao is not modificacao

    # Retorna um dicionário, sendo este tendo uma única chave 'nome', e valor 
    # desta chave será um dicionário com cinco campos(talvez mais no futuro),
    # bem definidos.
    return {
        nome: {
            "idade":       idade,
            "criação":     criacao,
            "modificação": modificacao,
            "estado":      nivel
          }
    }

def igualdade_cadastro(a: dict, b: dict) -> bool:
    "Verifica se os cadastros 'a' e 'b' são iguais, nos termos deste programa, obviamente."
    pass
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
#                                Testes Unitários                                           #
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
class ValidadeDeUmCadastro(TestCase):
    def runTest(self):
        hoje = datetime.today()
        entradas = [
            {
                "André Marcos": {
                    "idade": 15,
                    "criação": hoje - timedelta(hours=5, days=7),
                    "modificação": hoje - timedelta(hours=3),
                    "estado": 3
                }
            },
            # Tem um campo a mais no sub-dicionário.
            {
                "Júlia Marques Ducá": {
                    "não-existe": "nada",
                    "idade": 55,
                    "criação": hoje - timedelta(hours=3, days=1),
                    "modificação": hoje - timedelta(hours=2),
                    "estado": 4
                }
            },
            # Tem uma chave a mais no dicionário.
            {
                "André Leão Albuquerque": {
                    "idade": 2,
                    "criação": hoje - timedelta(hours=13, days=12),
                    "modificação": hoje - timedelta(hours=12),
                    "estado": 1
                },
                "Preferências": {
                    "fruta": "Morango",
                    "objeto": "Caneta"
                }
            },
            {
                "André Leão Albuquerque": {
                    "idade": 2,
                    "criação": hoje - timedelta(hours=13, days=12),
                    "modificação": hoje - timedelta(hours=12),
                    "estado": 1
                },
                "Cor": "Branca"
            },
        ]
        
        PPrint(entradas)
        self.assertTrue(cadastro_e_valido(entradas[0]))
        self.assertFalse(cadastro_e_valido(entradas[1]))
        self.assertFalse(cadastro_e_valido(entradas[2]))
        self.assertFalse(cadastro_e_valido(entradas[3]))