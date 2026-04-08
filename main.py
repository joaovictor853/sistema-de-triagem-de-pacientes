'''
    O objetivo do trabalho é fazer um sistema de triagem de pacientes. As instruções serão as seguintes:
  Usuário cadastra pacientes com nome, idade e nivel de dor (1 a 5). O programa exibe a lista ordenada
  pela gravidade.
'''

"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
							Módulo do Banco de Dados
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
"""
from unittest import (TestCase)
import json
from random import (choice, randint)
from datetime import (timedelta, datetime)
from pprint import (pprint)
from copy import (copy as CopiaObjeto)

# O banco de dados dele é uma lista que contém todas pessoas já cadastradas pelo programa. Dentro dele,
# cada cadastro será um dicionário do tipo 'string' e 'tupla'. A string é equivalente ao nome do 
# paciente, já a tupla algumas informações adicionais, como: data e hora do cadastro; o nível de 
# gravidade; e a idade dele.
CAMINHO_DO_BANCO = "dados/cadastros.json"
LISTA_DE_NOMES = "dados/testes/lista-de-nomes.txt"
BANCO_DE_DADOS_CADASTROS = []


def adiciona_cadastro(registro: dict) -> None:
    "Apenas adiciona um 'cadastro' dado no banco de dados carregado na memória."
    assert isinstance(registro, dict)
    global BANCO_DE_DADOS_CADASTROS

    BANCO_DE_DADOS_CADASTROS.append(registro)

def salva_banco_de_dados() -> None:
    """
      Salva todas modificações ou inserções no 'banco de cadastros' em disco.
    Antes disso, ele modifica o tipo de dado 'datetime' no seu 'timestamp', este
    que é um 'float', já que o JSON não é capaz inicialmente de armazenar tal tipo
    de dado estruturado. Nada será retornado.
    """
    global BANCO_DE_DADOS_CADASTROS
    # Clone da lista com dicionários atuais. Assim, não modificará o que está
    # rodando na memória. Se não fizess isso, causaria um problema de 'datarace'.
    lista_de_cadastros_ajustados = CopiaObjeto(BANCO_DE_DADOS_CADASTROS)

    # Transformando cada 'datetime' no seu 'timestamp'(um decimal).
    for dicio in lista_de_cadastros_ajustados:
        for nome in dicio:
            criacao = dicio[nome]["criação"]
            modificado = dicio[nome]["modificação"]

            dicio[nome]["criação"] = criacao.timestamp()
            dicio[nome]["modificação"] = modificado.timestamp()

    # Gravando a lista de dados no respectivo caminho que foi dado.
    arquivo = open(CAMINHO_DO_BANCO, "wt", encoding="utf8")
    json.dump(lista_de_cadastros_ajustados, arquivo, indent=4)
    arquivo.close()
    print("Os cadastros foram salvos com sucesso.")

def carrega_banco_de_dados() -> None:
    """
      Carrega o banco de dados no disco(um arquivo JSON), para a variável global
    'BANCO_DE_DADOS_CADASTROS', que está rodando na memória. É bom chamar esta função
    apenas uma vez por execução, se não, irá causar conflitos ou duplicação de
    dados. Observe que o algoritmo não apaga as outras já carregadas, apenas adiciona 
    novas.
    """
    global BANCO_DE_DADOS_CADASTROS

    # Abre o arquivo do caminho específicado. Então atribui a lista decodificada
    # na variável global que registra os cadastros em tempo de execução.
    arquivo = open(CAMINHO_DO_BANCO, "rt", encoding="utf8")
    lista_resultado = json.load(arquivo)
    arquivo.close()

    # Modifica novamente o 'timestamp' para um 'datetime'.
    for dicio in lista_resultado:
        for nome in dicio:
            criacao = dicio[nome]["criação"]
            modificado = dicio[nome]["modificação"]

            dicio[nome]["criação"] = datetime.fromtimestamp(criacao)
            dicio[nome]["modificação"] = datetime.fromtimestamp(modificado)
            BANCO_DE_DADOS_CADASTROS.append(dicio)
    print("O banco de dados foi carregado com sucesso.")

class SalvandoAlgunsRegistros(TestCase):
    def setUp(self):
        global LISTA_DE_NOMES

        self.nomes_arquivo = open(LISTA_DE_NOMES, "rt", encoding="utf8")
        self.conteudo = self.nomes_arquivo.read().split('\n')
        self.nomes_arquivo.close()

    def tearDown(self):
        pass

    def seleciona_nome_aleatorio(self) -> str:
        return choice(self.conteudo).rstrip('\n')

    def datetime_aleatorio(self) -> datetime:
        return datetime(
            hour=randint(0, 23),
            minute=randint(0, 60),
            second=randint(0, 60),
            # O hospital existe desde a década de 80.
            year=randint(1980, 2026),
            month=randint(1, 12),
            day=randint(1, 28)
        )
    def cria_cadastro_aleatorio(self) -> dict:
        nome = self.seleciona_nome_aleatorio()
        criacao = self.datetime_aleatorio()
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

    def runTest(self):
        pprint(BANCO_DE_DADOS_CADASTROS)
        for _ in range(4):
            instancia = self.cria_cadastro_aleatorio()
            adiciona_cadastro(instancia)

        pprint(BANCO_DE_DADOS_CADASTROS)
        salva_banco_de_dados()

class CarregandoBancoDeDados(TestCase):
    def runTest(self):
        global BANCO_DE_DADOS_CADASTROS

        carrega_banco_de_dados()
        pprint(BANCO_DE_DADOS_CADASTROS)

class MexendoComJSON(TestCase):
    def runTest(self):
        with open(CAMINHO_DO_BANCO, "wt") as database:
            amostras = [
                {'nada': 'alguma coisa'},
                {'amanda': [15, 27]},
                {"vitor": datetime.today().timestamp()}
            ]
            json.dump(amostras, database, indent=5)

"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
							Módulo Específico a Interface
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
"""
import shutil

# Nome genérico que "inventei". Na verdade, pedir para o 'Gemini' criar tal, mas baseado no seguinte
# prompt: "Pode sugerir-me um nome de hospital, um que remeta a uma instituição antiga e respeitada."
# A resposta dele foi a seguinte lista, e mais paragrafos e paragros de explicação porque estas escolhas:
#
#    Hospital Memorial Cândido Ferreira
#    Centro Hospitalar Acadêmico Silva Brandão
#    Real Beneficência da Colina
#    Hospital da Santa Perseverança
#    Sociedade Hospitalar Dom Pedro II
#    Hospital Sancta Vita
#    Hospital Magnus Curatio
#    Instituto Salus
NOME_DO_HOSPITAL = "Centro Hospitalar Acadêmico Silva Brandão"

def barra_do_tamanho_da_tela(componente: str) -> str:
    LARGURA_TELA = shutil.get_terminal_size().columns - 5
    
    return componente * LARGURA_TELA

def mostrar_cabecalho_em_caixa(titulo: str) -> None:
    """
    Está função formata e imprime um cabeçalho qualquer, dado a string que você colocou como argumento.
    O mesmo que a função 'mostrar_cabecalho', entretanto, este a formatação dela é diferente, ele faz
    a string ficar centralizado entre as barras.
    """
    # Apenas aceita argumentos do tipo string.
    assert isinstance(titulo, str)
    
    comprimento = len(titulo)
    LARGURA_TELA = shutil.get_terminal_size().columns - 5
    qtd_tracos = (LARGURA_TELA - comprimento) // 2
    barra = '-' * LARGURA_TELA
    recuo = ' ' * qtd_tracos
    
    print(f"\n{barra}\n{recuo}{titulo}\n{barra}\n")

def mostrar_cabecalho(titulo: str) -> None:
    """
    Está função formata e imprime um cabeçalho qualquer, dado a string que você colocou como argumento.
    """
    # Apenas aceita argumentos do tipo string.
    assert isinstance(titulo, str)
    import shutil
    
    comprimento = len(titulo)
    LARGURA_TELA = shutil.get_terminal_size().columns - 5
    qtd_tracos = (LARGURA_TELA - comprimento) // 2
    barra = '-' * qtd_tracos
    
    print(f"\n{barra} {titulo} {barra}\n")

def visualizacao_do_menu(*menus: list[str]) -> None:
    """
    Pega menus feitas(uma lista), então númera os de 1 à quantia total, e formata 
    eles em colunas. Retorna nada.
    """
    assert all(map(lambda item: isinstance(item, str), menus))
    # Um contador.
    cursor = 1
    # Máximo de colunas permitidas no menu.
    COLUNAS = 4
    ESPACO = ' '
    RECUO = ESPACO * 4
    # Comprimento da maior string entre menus, assim pode espaçar cada um
    # referente a ele.
    maior = len(max(*menus))

    # Se o comprimento da string não for o suficiente, colocar um padrão.
    if maior >= 9:
        maior += 3
    else:
        maior = 7

    # Cria barra e imprime a descrição, neste caso: 'menu'.
    print(barra_do_tamanho_da_tela('+'))
    print("Menu:", end='\n\n')

    for (numeracao, opcao) in enumerate(menus):
        # Condicional pula para uma nova linha, quando bater o limite de colunas
        # pré-determinado, isso pela constante 'COLUNAS'.
        if cursor % COLUNAS == 0:
            print("")

        print(f"{RECUO}{numeracao + 1}) {opcao:<{maior}}", end='')
        cursor += 1
    # Espaçando e colocar a barra de baixo.
    print(''); print(barra_do_tamanho_da_tela('+')); print('')

def cabecalho_padrao_do_hospital() -> None:
    "Cria o cabeçalho inicial do hospital em questão. Retorna nada."
    print(f"""
        \r{barra_do_tamanho_da_tela('=')}
           	\t\tCaadastrario dos Pacientes 
        		\t\tno
			{NOME_DO_HOSPITAL}
        \r{barra_do_tamanho_da_tela('=')}
        """)

def listagem_de_cadastros() -> None:
    global BANCO_DE_DADOS_CADASTROS

    # Pula uma linha para ficar mais organizado(espaçado).
    print("")

    if len(BANCO_DE_DADOS_CADASTROS) == 0:
        print("\nNão há cadastros.", end='\n\n')
    else:
        for dicio in BANCO_DE_DADOS_CADASTROS:
            for nome in dicio:
                print('\t-', nome)
        # Pula uma linha para ficar mais organizado(espaçado).
        print("")

def manual_de_ajuda_do_programa() -> None:
    print("""
        \rVocê pediu por ajuda. Aqui está o manual:

        \r\tAdicionar  - Realiza e adiciona novo cadastro.
        \r\tRemover    - Remove um cadastro do banco.
        \r\tAjuda      - Mostra este manual aqui.
        \r\tListar     - Listagem de cadastros realizados.
        \r\tSair       - Abandonar o programa de forma padrão. Lebrando que
        \r\t             outros métodos de fazer isso, não garante que os
        \r\t             cadastros removidos ou adicionados são salvos.
    """)

class VisualizacaoDoMenu(TestCase):
    def setUp(self):
        self.MENU = ["Info", "Estatísticas", "Adicionar", "Deletar", "Obituário", "Listagem"]

    def runTest(self):
        visualizacao_do_menu(*self.MENU)
"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
							Módulo Modelo e Entrada de Dados
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
"""
def cria_cadastro(nome: str, idade: int, nivel: int, criacao: datetime, modificacao: datetime) -> dict:
    "Cria uma instância do que será amarzenado no banco de dados no final."
    assert isinstance(nome, str)
    assert isinstance(idade, int)
    assert isinstance(nivel, int)
    assert isinstance(criacao, datetime)
    assert isinstance(modificacao, datetime)
    # Não podem referenciar o mesmo objeto.
    assert criacao is not modificacao

    return {
        nome: {
            "idade":       idade,
            "criação":     criacao,
            "modificação": modificacao,
            "estado":      nivel
          }
    }

def recuo(n: int) -> str:
    "Retorna string de recuo para dá margem a outras mensagens."
    ESPACO = ' '
    return ESPACO * n

def entrada_de_cadastro_agora() -> dict:
    "Realiza um cadastro agora, então envia o dicionário formado dele."
    nome = input(f"\n{recuo(4)}Nome do paciente: ")
    idade = int(input(f"{recuo(4)}Sua idade: "))
    nivel_de_dor = int(input(f"{recuo(4)}Nível de dor[1 à 5]: "))
    criacao = datetime.today()
    # Jeito de fazer clone da variável 'criação'.
    modificacao = criacao + timedelta(seconds=0)

    # Correção de uma entrada inválida.
    if nivel_de_dor > 5 or nivel_de_dor <= 0:
        print(f"Não aceito 'nível' igual á {nivel_de_dor}. Apenas valores de 1 à 5.")
        if nivel_de_dor > 5:
            nivel_de_dor = 5
        if nivel_de_dor < 0:
            nivel_de_dor = abs(nivel_de_dor) % 6
        if nivel_de_dor == 0:
            nivel_de_dor = 1
        print(f"O nível foi ajustado para {nivel_de_dor}.")

    return cria_cadastro(nome, idade, nivel_de_dor, criacao, modificacao)

def entrada_escolha_do_menu(menus: list[str]) -> int:
    "Pega uma lista com os menus, então retorna o número equivalente de cada opção."
    assert all(map(lambda item: isinstance(item, str), menus))
    visualizacao_do_menu(*menus)

    entrada = input("Escolha uma opção: ")

    if entrada.isdigit():
        valor = int(entrada)

        # Primeiro supõe que digitou o número:
        if 1 <= valor <= len(menus):
            return valor
        else:
            #raise IndexError(f"Não existe está opção {entrada}.")
            print(f"Numeração {entrada} não existe. Programa quebrou!")
            exit(2)
    elif entrada.isalpha():
        # Espera que há retorno.
        for (indice, opcao) in enumerate(menus):
            if entrada.lower() in opcao.lower():
                return (indice + 1)
        #raise ValueError(f"Não existe está opção {entrada}.")
        print(f"Não existe está opção {entrada}. Programa quebrou!")
        exit(2)
    else:
        #raise ValueError(f"Não aceita está entrada {entrada}, apenas 'int' e 'str'.")
        print (f"Não aceita está entrada {entrada}, apenas 'int' e 'str'. Programa quebrou!")
        exit(2)

class EntradaDeCadastroAgora(TestCase):
    def runTest(self):
        instancia = entrada_de_cadastro_agora()

        pprint(instancia, indent='4')

class EntradaEscolhaDoMenu(VisualizacaoDoMenu):
    def runTest(self):
        entrada = entrada_escolha_do_menu(self.MENU)

        print(f"Índice devolvido: {entrada}")

class PrototipoPrograma(TestCase):
    def runTest(self):
        MENU_DE_OPCOES = ["Adicionar", "Remover", "Listar","Ajuda", "Sair"]

        carrega_banco_de_dados()
        cabecalho_padrao_do_hospital()

        while True:
            match entrada_escolha_do_menu(MENU_DE_OPCOES):
                case 1:
                    adiciona_cadastro(entrada_de_cadastro_agora())
                case 2:
                    pass
                case 3:
                    listagem_de_cadastros()
                case 4:
                    manual_de_ajuda_do_programa()
                case 5:
                    print("Você pressionou para sair.")
                    break
                case _:
                    print("Este número e oção não é válido.")

        salva_banco_de_dados()
"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
                                Execução do Programa
  Aqui fica a cópia do testes unitário 'PrototipoPrograma'. Toda vez que for modificado algo
lá, será copiado e colocado aqui.
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
"""
MENU_DE_OPCOES = ["Adicionar", "Remover", "Listar", "Ajuda", "Sair"]

carrega_banco_de_dados()
cabecalho_padrao_do_hospital()

while True:
    match entrada_escolha_do_menu(MENU_DE_OPCOES):
        case 1:
            adiciona_cadastro(entrada_de_cadastro_agora())
        case 2:
            pass
        case 3:
            listagem_de_cadastros()
        case 4:
            manual_de_ajuda_do_programa()
        case 5:
            print("Você pressionou para sair.")
            break
        case _:
            print("Este número e oção não é válido.")

salva_banco_de_dados()
