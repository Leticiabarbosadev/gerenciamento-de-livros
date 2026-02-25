from dataclasses import dataclass
from typing import Optional


@dataclass
class Livro:
    titulo: str
    autor: str
    paginas: int
    quantidade: int
    emprestados: int = 0


@dataclass
class Usuario:
    nome: str
    sobrenome: str
    cpf: str
    telefone: str


@dataclass
class Emprestimo:
    livro: str
    usuario: str
    data_emprestimo: str
    devolvido: bool = False
    data_devolucao: Optional[str] = None