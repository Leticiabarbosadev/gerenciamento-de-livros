import json
from dataclasses import asdict
from pathlib import Path
from datetime import datetime
from models import Livro, Usuario, Emprestimo

ARQUIVO = "database.json"


class Biblioteca:

    def __init__(self):
        self.livros = []
        self.usuarios = []
        self.emprestimos = []
        self.carregar()

    # ---------------- LIVROS
    def adicionar_livro(self, titulo, autor, paginas, quantidade):

        livro = Livro(
            titulo.strip(),
            autor.strip(),
            int(paginas),
            int(quantidade)
        )

        self.livros.append(livro)
        self.salvar()

    def listar_livros(self):
        return self.livros

    # ---------------- USUARIOS
    def adicionar_usuario(self, nome, sobrenome, cpf, telefone):

        usuario = Usuario(
            nome.strip(),
            sobrenome.strip(),
            cpf.strip(),
            telefone.strip()
        )

        self.usuarios.append(usuario)
        self.salvar()

    def listar_usuarios(self):
        return self.usuarios

    # ---------------- EMPRESTIMO
    def emprestar(self, livro, usuario):

        livro_digitado = livro.strip().lower()
        usuario_digitado = usuario.strip()

        for l in self.livros:

            if l.titulo.strip().lower() == livro_digitado:

                disponivel = l.quantidade - l.emprestados

                if disponivel > 0:

                    l.emprestados += 1

                    self.emprestimos.append(
                        Emprestimo(
                            l.titulo,
                            usuario_digitado,
                            datetime.now().strftime("%d/%m/%Y %H:%M"),
                            False,
                            None
                        )
                    )

                    self.salvar()

                    return "Livro emprestado com sucesso ✅"

                return "Livro indisponível ❌"

        return "Livro não encontrado ❌"

    # ---------------- DEVOLUÇÃO
    def devolver(self, livro, usuario):

        livro_digitado = livro.strip().lower()
        usuario_digitado = usuario.strip().lower()

        for emp in self.emprestimos:

            if (
                emp.livro.strip().lower() == livro_digitado
                and emp.usuario.strip().lower() == usuario_digitado
                and not emp.devolvido
            ):

                emp.devolvido = True
                emp.data_devolucao = datetime.now().strftime("%d/%m/%Y %H:%M")

                for l in self.livros:
                    if l.titulo.strip().lower() == livro_digitado:
                        if l.emprestados > 0:
                            l.emprestados -= 1

                self.salvar()

                return "Livro devolvido com sucesso ✅"

        return "Empréstimo não encontrado ❌"

    def listar_emprestimos(self):
        return self.emprestimos

    # ---------------- SALVAR
    def salvar(self):

        dados = {
            "livros": [asdict(l) for l in self.livros],
            "usuarios": [asdict(u) for u in self.usuarios],
            "emprestimos": [asdict(e) for e in self.emprestimos]
        }

        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    # ---------------- CARREGAR
    def carregar(self):

        if not Path(ARQUIVO).exists():
            return

        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)

        self.livros = [Livro(**l) for l in dados.get("livros", [])]
        self.usuarios = [Usuario(**u) for u in dados.get("usuarios", [])]
        self.emprestimos = [Emprestimo(**e) for e in dados.get("emprestimos", [])]