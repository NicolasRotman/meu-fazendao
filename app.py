from flask import Flask, render_template, request, redirect, url_for, flash
import bcrypt
import os

app = Flask(__name__)
app.secret_key = "segredo123"  # necessário pro flash funcionar
tabela = 'meu_fazendao.txt'

# Garante que o arquivo existe
if not os.path.exists(tabela):
    with open(tabela, "w") as f:
        pass

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email").strip()
        senha = request.form.get("senha").encode('utf-8')

        with open(tabela, "r") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(" : ")
                if len(partes) == 3 and partes[1] == email:
                    senha_correta = partes[2].encode('utf-8')
                    if bcrypt.checkpw(senha, senha_correta):
                        flash("✅ Login bem-sucedido!", "sucesso")
                        return redirect(url_for("login"))
                    else:
                        flash("❌ Senha incorreta!", "erro")
                        return redirect(url_for("login"))

        flash("📭 Email não encontrado. Cadastre-se primeiro!", "erro")
        return redirect(url_for("cadastro"))

    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome").strip()
        email = request.form.get("email").strip()
        senha = request.form.get("senha").encode('utf-8')

        # Verifica se já existe
        with open(tabela, "r") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(" : ")
                if len(partes) == 3 and partes[1] == email:
                    flash("⚠️ Este email já está cadastrado!", "erro")
                    return redirect(url_for("cadastro"))

        # Criptografa e salva
        senha_hash = bcrypt.hashpw(senha, bcrypt.gensalt()).decode('utf-8')
        with open(tabela, "a") as arquivo:
            arquivo.write(f"{nome} : {email} : {senha_hash}\n")

        flash("✅ Cadastro realizado com sucesso! Faça login.", "sucesso")
        return redirect(url_for("login"))

    return render_template("cadastro.html")

if __name__ == "__main__":
    app.run(debug=True)
