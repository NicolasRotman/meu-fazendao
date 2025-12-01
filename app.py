from flask import Flask, render_template, request, redirect, url_for, flash, session
import bcrypt
import os
import sqlite3
from email.message import EmailMessage
import random
from datetime import datetime
import smtplib

app = Flask(__name__)
app.secret_key = "fazendinha123"
tabela = 'meu_fazendao.txt'

conexao = sqlite3.connect("meu_banco.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    categoria TEXT NOT NULL,
    quantidade REAL NOT NULL,
    unidade_medida TEXT NOT NULL,
    storage_location TEXT NOT NULL,
    value REAL NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS harvest (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_name TEXT NOT NULL,
    planting_date DATE NOT NULL,
    harvest_date DATE NOT NULL,
    estimated_yield REAL NOT NULL,
    unit TEXT NOT NULL,
    cost REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS machinery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_name TEXT NOT NULL,
    categoria TEXT NOT NULL,
    date DATE NOT NULL,
    valor REAL NOT NULL,
    machine_id TEXT NOT NULL,
    status TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_name TEXT NOT NULL,
    categoria TEXT NOT NULL,
    machine TEXT NOT NULL,
    valor REAL NOT NULL,
    data DATE NOT NULL
);
""")

conexao.commit()
conexao.close()
def enviar_email(destinatario, assunto, corpo):
    email_remetente = 'meufazendao@gmail.com'
    senha = 'wdfu pgrd ubqn tmaa'

    # Criar mensagem
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = email_remetente
    msg['To'] = destinatario
    msg.set_content(corpo)  # Corpo em texto puro


    # Enviar e-mail pelo servidor SMTP do Gmail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_remetente, senha)
        smtp.send_message(msg)
        print("Email enviado com sucesso!")


# Garante que o arquivo existe
if not os.path.exists(tabela):
    with open(tabela, "w") as f:
        pass

# DELETES FUNCIONANDO 29/11 20:55
@app.route("/deletar_expense", methods=['POST'])
def deletar_expense():

    item_id = request.form["id"]
    conexao = sqlite3.connect("meu_banco.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (item_id,))
    conexao.commit()
    conexao.close()

    return redirect(request.referrer)

@app.route("/deletar_harvest", methods=['POST'])
def deletar_harvest():

    item_id = request.form["id"]
    conexao = sqlite3.connect("meu_banco.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM harvest WHERE id = ?", (item_id,))
    conexao.commit()
    conexao.close()

    return redirect(request.referrer)

@app.route("/deletar_machine", methods=['POST'])
def deletar_machine():
    item_id = request.form["id"]

    conexao = sqlite3.connect("meu_banco.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM machinery WHERE id = ?", (item_id,))
    conexao.commit()
    conexao.close()

    return redirect(request.referrer)

@app.route("/deletar_product", methods=['POST'])
def deletar_product():
    item_id = request.form["id"]

    conexao = sqlite3.connect("meu_banco.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (item_id,))
    conexao.commit()
    conexao.close()

    return redirect(request.referrer)

@app.route("/edit_expense", methods=['POST'])
def edit_expense():
    id = request.form.get("id")
    name = request.form.get("name")
    categoria = request.form.get("categoria")
    valor = request.form.get("valor")
    data = request.form.get("date")
    machine = request.form.get("machine")
    '''
    atualização dos dados no banco
    '''

    return redirect(url_for("expenses"))

@app.route("/edit_harvest", methods=['POST'])
def edit_harvest():
    harvest_id = request.form.get("id")
    crop_name = request.form.get("crop_name")
    planting_date = request.form.get("planting_date")
    harvest_date = request.form.get("harvest_date")
    estimated_yield = request.form.get("estimated_yield")
    unit = request.form.get("unit")
    cost = request.form.get("cost", 0)
    '''
    atualização dos dados no banco
    '''

    return redirect(url_for("harvest"))

@app.route("/edit_machine", methods=['POST'])
def edit_machine():
    id = request.form.get("id")
    name = request.form.get("name")
    categoria = request.form.get("categoria")
    valor = request.form.get("valor")
    data = request.form.get("date")
    machine = request.form.get("machine")

    '''
    atualização dos dados no banco
    '''

    return redirect(url_for("machinery"))

@app.route("/edit_products", methods=['POST'])
def edit_products():
    name = request.form.get("name")
    product_type = request.form.get("type")
    location = request.form.get("location")
    quantity = request.form.get("quantity")
    unit = request.form.get("unit")
    value = request.form.get("value")

    '''
    atualização dos dados no banco
    '''
    
@app.route("/edit_employees", methods=['POST'])
def edit_employees():
    name = request.form.get("name")
    employee_function = request.form.get("fuction")
    area = request.form.get("area")
    status = request.form.get("status")
    wage = request.form.get("wage")

    return redirect(url_for("employees"))

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
                        return redirect(url_for("dashboard"))
                    else:
                        flash("❌ Senha incorreta!", "erro")
                        return redirect(url_for("login"))

        flash("📭 Email não encontrado. Cadastre-se primeiro!")
        return redirect(url_for("cadastro"))

    return render_template("login.html")

@app.route("/Login")
def cadastro_pas():
    return render_template('cadastro.html')

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

@app.route('/dashboard')
def dashboard():

    conexao = sqlite3.connect("meu_banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, expense_name, categoria, machine, valor, data
        FROM expenses
    """)
    expensess = cursor.fetchall()
    conexao.close()

    expenseslista = []
    for m in expensess:
        expenseslista.append({
            "id": m[0],
            "nome": m[1],
            "categoria": m[2],
            "valor": m[4],
            "data": m[5],
        })

    machinery = [3,4,7]

    conexao = sqlite3.connect("meu_banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, crop_name, planting_date, harvest_date, estimated_yield, unit, cost
        FROM harvest
    """)
    harvests = cursor.fetchall()
    conexao.close()

    harvest = []
    for h in harvests:
        harvest.append({
            "id": h[0],
            "nome": h[1],
            "categoria": "fruta",
            "unidade": h[5],
            "porcentagem":"60",
            "quantidade": h[4],
        })

    expenses_lista = sum([10000, 20000, 5000])
    expenses_total = [expenses_lista]

    monthly_expenses = [1200, 1800, 1500, 2200, 1900, 35000]

    return render_template('dashboard.html', expenses=expenseslista, machinery=machinery, harvestD=harvest,  expenses_total=expenses_total, monthly_expenses=monthly_expenses)

@app.route('/expenses', methods=['GET', 'POST'])
def expenses(): # FUNCIONANDO 29/11 19:46
    if request.method == 'POST':
        if "expense_name" in request.form:
            expense_name = request.form.get("expense_name")
            categoria = request.form.get("categoria")
            machine = request.form.get("machine")
            valor = request.form.get("valor")
            data = request.form.get("date")

        conexao = sqlite3.connect("meu_banco.db")
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO expenses 
            (expense_name, categoria, machine, valor, data)
            VALUES (?, ?, ?, ?, ?)
        """, (expense_name, categoria, machine, valor, data))

        conexao.commit()
        conexao.close()

        return redirect('/expenses')

    conexao = sqlite3.connect("meu_banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, expense_name, categoria, machine, valor, data
        FROM expenses
    """)
    expensess = cursor.fetchall()
    conexao.close()

    expenseslista = []
    for m in expensess:
        expenseslista.append({
            "id": m[0],
            "nome": m[1],
            "categoria": m[2],
            "valor": m[4],
            "data": m[5],
            "machine": m[3],
        })
    return render_template('expenses.html', expenses=expenseslista)

@app.route('/machinery', methods=['GET', 'POST'])
def machinery(): # FUNCIONANDO 29/11 19:09
    if request.method == 'POST':
        machine_name = request.form.get("machine_name")
        categoria = request.form.get("categoria")
        date = request.form.get('date')
        valor = request.form.get("valor")
        machine_id = request.form.get('machine_id')
        status = request.form.get('status')

        random_image = f"tractors/{random.randint(1,3)}.jpg"
        photo_url = url_for('static', filename=random_image)

        conexao = sqlite3.connect("meu_banco.db")
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO machinery 
            (machine_name, categoria, date, valor, machine_id, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (machine_name, categoria, date, valor, machine_id, status))

        conexao.commit()
        conexao.close()

        return redirect('/machinery')

    conexao = sqlite3.connect("meu_banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, machine_name, categoria, date, valor, machine_id, status
        FROM machinery
    """)
    machinerys = cursor.fetchall()
    conexao.close()

    machinerylista = []
    for m in machinerys:
        machinerylista.append({
            "id": m[0],
            "name": m[1],
            "valor": m[4],
            "status": "Active",
            "data": m[3],
            "type": m[2],
            "serial": m[5],  
            "img_url": "https://brasil.agrofystatic.com/media/catalog/product/cache/850x600/T/r/Trator-Agr_cola-John-Deere-6190J---Novo-agrofy-0-20231010123645.jpg",
            "horas_w": "1500",
            "pros_w": "2026-01-15",
        })

    return render_template('machinery.html', machines=machinerylista)

@app.route('/products', methods=['GET', 'POST'])
def products(): # FUNCIONANDO 28/11 19:43
    if request.method == 'POST':
        product_name = request.form.get("product_name")
        categoria = request.form.get("categoria")
        quantidade = request.form.get("quantidade")
        unidade_medida = request.form.get("unidade_medida")
        storage_location = request.form.get("storage_location")
        value = request.form.get("value")
        
        conexao = sqlite3.connect("meu_banco.db")
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO products 
            (product_name, categoria, quantidade, unidade_medida, storage_location, value)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (product_name, categoria, quantidade, unidade_medida, storage_location, value))

        conexao.commit()
        conexao.close()

        return redirect('/products')

    conexao = sqlite3.connect("meu_banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, product_name, categoria, quantidade, unidade_medida, storage_location 
        FROM products
    """)
    produtos = cursor.fetchall()
    conexao.close()

    products = []
    for p in produtos:
        products.append({
            "id": p[0],
            "name": p[1],
            "type": p[2],
            "quantity": p[3],
            "unit": p[4],
            "location": p[5],
            "value": 0           
        })

    return render_template('products.html', products=products)

            

@app.route('/harvest', methods=['GET', 'POST']) # FUNCIONANDO 28/11 20:54
def harvest():
    if request.method == 'POST':
        if 'crop_name' in request.form:
            crop_name = request.form.get("crop_name")
            planting_date = request.form.get("planting_date")
            harvest_date = request.form.get("harvest_date")
            estimated_yield = request.form.get("estimated_yield")
            unit = request.form.get("unit")
            cost = request.form.get("initial_cost")

            random_image = f"harvest/{random.randint(1,3)}.jpg"
            photo_url = url_for('static', filename=random_image)

            conexao = sqlite3.connect("meu_banco.db")
            cursor = conexao.cursor()

            cursor.execute("""
            INSERT INTO harvest
            (crop_name, planting_date, harvest_date, estimated_yield, unit, cost)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (crop_name, planting_date, harvest_date, estimated_yield, unit, cost))

            conexao.commit()
            conexao.close()


            return redirect('/harvest')
        
    conexao = sqlite3.connect("meu_banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, crop_name, planting_date, harvest_date, estimated_yield, unit, cost
        FROM harvest
    """)
    harvests = cursor.fetchall()
    conexao.close()

    harvest = []
    for h in harvests:
        harvest.append({
            "id": h[0],
            "crop_name": h[1],
            "planting_date": h[2],
            "harvest_date": h[3],
            "estimated_yield": h[4],
            "unit": h[5],
            "cost": h[6],
            "url_photo": "https://chb.com.br/storage/blog/174577.jpg",
            "porcentagem":"60",
            "status": "crescendo"
        })

    return render_template('harvest.html', harvest=harvest)

@app.route('/verificate_email')
def forgot_pass():
    return render_template('verificate_email.html')

@app.route('/verificate_password' , methods=['GET', 'POST'])
def verificar_email():
    if request.method == "POST":
        email = request.form.get("email").strip()
        codigo = random.randint(100000, 999999)
        session["codigo"] = str(codigo) 
        enviar_email(email, "Redefinir Senha", f"Abaixo segue o codigo para realizar a alteração da senha\n{codigo}")
    return render_template('verificate_pass.html')

@app.route('/reset_password' , methods=['GET', 'POST'])
def verificar_codigo():
    if request.method == 'POST':
        if "d1" in request.form:        
            d1 = request.form.get("d1").strip()
            d2 = request.form.get("d2").strip()
            d3 = request.form.get("d3").strip()
            d4 = request.form.get("d4").strip()
            d5 = request.form.get("d5").strip()
            d6 = request.form.get("d6").strip()
            codigo = f'{d1}{d2}{d3}{d4}{d5}{d6}'
            codigo_c =  session.get("codigo")
            if codigo == codigo_c:
                flash("✅ Código correto")
                return render_template('reset.html')
            else:
                flash("❌ Código incorreto")
                return render_template("verificate_pass.html")
    
        else:
            nova_senha = request.form.get("nova_senha")
            confirm_senha = request.form.get("confirm_senha")
            if nova_senha != confirm_senha:
                flash("⚠️ As senhas digitadas são diferentes.")
            else:
                '''
                atualização das senhas no banco
                '''
                flash('✅ Senhas atualizadas com sucesso')
                return render_template("login.html")
    return render_template("reset.html")

if __name__ == "__main__":
    app.run(debug=True)
