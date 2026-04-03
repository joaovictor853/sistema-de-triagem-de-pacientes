"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
							Módulo dos Modelos
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
"""
from dataclasses import dataclass
from datetime import (datetime as DateTime)

@dataclass
class Cadastro:
	"""
		Claro que este modelo é para o futuro. Como ele ensinou apenas dicionário até o momento, farei
	exatamente assim. Então, cada cadastro feito, será colocado num dicionário, onde a chave é o 'nome',
	e o valor dela será uma tupla com os demais dados.
	"""
    # Campos da instrução do trabalho.
	nome: str
	idade: int
	nivel: int
	# Campos extras que sugiro:
	criado: DateTime
	modificacoes: tuple[int, Datetime]
 
	# Métodos necessários de definir, se não a função/method 'sort' não irá funcionar.
	def __le__(self, outro: Self) -> bool:
		return self.nivel <= outro.nivel
    
	def __ge__(self, outro: Self):
 		return self.nivel >= outro.nivel

	def __lt__(self, outro: Self) -> bool:
    		return self.nivel < outro.nivel
    
	def __gt__(self, outro: Self):
 		return self.nivel > outro.nivel

	# Métodos de serialização dos tipos de dados:
	def serializar(self) -> bytearray:
		pass

	@staticmethod
	def deserializar(dados: bytearray) -> Self:
		pass

