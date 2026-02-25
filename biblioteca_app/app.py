from flask import Flask, render_template, request, redirect
from biblioteca import Biblioteca

app = Flask(__name__)
biblioteca = Biblioteca()


@app.route("/")
def home():
    return redirect("/livros")


@app.route("/livros", methods=["GET", "POST"])
def livros():

    if request.method == "POST":

        biblioteca.adicionar_livro(
            request.form["titulo"],
            request.form["autor"],
            request.form["paginas"],
            request.form["quantidade"]
        )

    return render_template(
        "livros.html",
        livros=biblioteca.listar_livros()
    )


@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():

    if request.method == "POST":

        biblioteca.adicionar_usuario(
            request.form["nome"],
            request.form["sobrenome"],
            request.form["cpf"],
            request.form["telefone"]
        )

    return render_template(
        "usuarios.html",
        usuarios=biblioteca.listar_usuarios()
    )


@app.route("/emprestimo", methods=["GET", "POST"])
def emprestimo():

    mensagem = ""

    if request.method == "POST":

        mensagem = biblioteca.emprestar(
            request.form["livro"],
            request.form["usuario"]
        )

    return render_template(
        "emprestimo.html",
        mensagem=mensagem
    )


@app.route("/devolucao", methods=["GET", "POST"])
def devolucao():

    mensagem = ""

    if request.method == "POST":

        mensagem = biblioteca.devolver(
            request.form["livro"],
            request.form["usuario"]
        )

    return render_template(
        "devolucao.html",
        mensagem=mensagem
    )


@app.route("/historico")
def historico():

    return render_template(
        "historico.html",
        emprestimos=biblioteca.listar_emprestimos()
    )


if __name__ == "__main__":
    app.run(debug=True)