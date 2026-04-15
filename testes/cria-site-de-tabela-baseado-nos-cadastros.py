"""
Script insere entradas do banco no site.
"""
from bancodedados import (carrega_banco_de_dados, todos_cadastros, )
from interface import (NOME_DO_HOSPITAL)
from modelos import (traducao_do_nivel_de_dor, nome_cadastro, idade_cadastro,
                     nivel_de_dor_cadastro)


# Como esta parte é meio que estática, pode ser definida na inicialização.
COMENTARIO_DA_PAGINA = """
<!--  
  Prompt que foi necessário para gerar, ao menos o básico desta página, com o 
  Gemini:

  Por favor, gere uma simples página que mostre um título no formato daqueles 
  de jornais, este separado por uma barra. Abaixo disso tudo vem uma tabela, 
  com os campos necessários do sistema de triagem: nome, idade, nível de dor, 
  criação. O esquema de cores que estou pensando é, algo parecido com o GitHub 
  no modo 'dark'. Eu quero as bordas da tabelas bem amigaveis,... bem 
  redondas. O código tem que ser apenas em HTML puro, nada de CSS ou 
  JavaScript. Também, tente espaçar cada parte importante. Não tenho muito 
  conhecimento dele assim para diferenciar tudo.
 -->
"""
TITULO_DA_PAGINA = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{NOME_DO_HOSPITAL}</title>
</head>
"""
CABECALHO_DA_PAGINA = f"""
    <h1 align="center" style="color: #5ec1df; font-family: 'Times New Roman', serif; letter-spacing: 2px;">
        {NOME_DO_HOSPITAL}
    </h1>
    <hr size="2" color="#30363d" width="90%">
    <br>
"""

def cria_cabecalho_da_tabela() -> str:
    return ("""
       <tr bgcolor="#21262d" style="text-align: left; font-size: 18px; color: #ffffff;">
            <th width="10%">Nome</th>
            <th width="20%", align="center">Idade</th>
            <th width="25%">Nível de Dor</th>
            <th width="15%">Entrada</th>
        </tr>
    """)
    
def cria_linha_da_tabela(cadastro: dict) -> str:
    assert cadastro_e_valido(cadastro)
    
    NOME_DO_PACIENTE = nome_cadastro(cadastro)
    SUA_IDADE = idade_cadastro(cadastro)
    NIVEL = nivel_de_dor_cadastro(cadastro)
    ESTADO_DE_SAUDE = traducao_do_nivel_de_dor(NIVEL)
    DATA_DE_ENTRADA = criacao_cadastro(cadastro).strftime("%d de %b de %Y as %H%p")
    
    return f"""
        <tr>
            <td><b>{NOME_DO_PACIENTE}</b></td>
            <td align="center">{SUA_IDADE}</td>
            <td style='color: yellow'><b>{ESTADO_DE_SAUDE}</b></td>
            <td>{DATA_DE_ENTRADA}</td>
        </tr>
    """

def cria_a_tabela_baseano_nos_cadastros() -> str:
    CONFIGURACAO_DA_TABELA = """
        <table align="center" width="90%" cellpadding="15" cellspacing="0" style="background-color: #161b22; border-radius: 12px; overflow: hidden; border: 1px solid #30363d;">
    """
    
    return f"""
        {CONFIGURACAO_DA_TABELA}
        </table>
    """
carrega_banco_de_dados()
LISTA_DE_CADASTROS = todos_cadastros()
