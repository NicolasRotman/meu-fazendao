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

@app.route("/deletar_expense", methods=['POST'])
def deletar_expense():
    item_id = request.form["id"]
    '''
    remoção de dados no banco
    '''
    return redirect(request.referrer)

@app.route("/deletar_harvest", methods=['POST'])
def deletar_harvest():
    item_id = request.form["id"]
    '''
    remoção de dados no banco
    '''
    return redirect(request.referrer)

@app.route("/deletar_machine", methods=['POST'])
def deletar_machine():
    item_id = request.form["id"]
    
    '''
    remoção de dados no banco
    '''
    return redirect(request.referrer)

@app.route("/deletar_product", methods=['POST'])
def deletar_product():
    item_id = request.form["id"]
    
    '''
    remoção de dados no banco
    '''
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

    return redirect(url_for("products"))

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
    expenses = [
        {"id": 1, "nome": "Compra de sementes", "categoria": "Seeds", "valor": 150.75, "data": "2023-10-20"},
        {"id": 2, "nome": "Troca de óleo do trator", "categoria": "Maintenance", "valor": 320.00, "data": "2023-10-25"},
        {"id": 3, "nome": "Combustível", "categoria": "Fuel", "valor": 120.50, "data": "2023-10-27"},
    ]

    machinery = [3,4,7]
    harvestD = [
        {"id": 1, "nome": "trigo", "categoria": "fruta", "unidade": "kg", "porcentagem":20, "quantidade": "45"},
        {"id": 2, "nome": "uva", "categoria": "fruta", "unidade": "ton","porcentagem":40, "quantidade": "1.2"},
        {"id": 3, "nome": "melancia", "categoria": "fruta", "unidade": "kg","porcentagem":80, "quantidade": "13"},
    ]

    expenses_lista = sum([10000, 20000, 5000])
    expenses_total = [expenses_lista]

    monthly_expenses = [1200, 1800, 1500, 2200, 1900, 35000]

    return render_template('dashboard.html', expenses=expenses, machinery=machinery, harvestD=harvestD,  expenses_total=expenses_total, monthly_expenses=monthly_expenses)

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        if "expense_name" in request.form:
            expense_name = request.form.get("expense_name")
            categoria = request.form.get("categoria")
            machine = request.form.get("machine")
            valor = request.form.get("valor")
            data = request.form.get("date")
            '''
            inserção dos dados das despesas no banco
            '''
            return redirect(url_for("expenses"))
    else:
        expenses = [
            {"id": 1, "nome": "Compra de sementes", "categoria": "Seeds", "valor": 150.75, "data": "2023-10-20", "machine": "--"},
            {"id": 2, "nome": "Troca de óleo do trator", "categoria": "Maintenance", "valor": 320.00, "data": "2023-10-25", "machine": "Jhonson"},
            {"id": 3, "nome": "Combustível", "categoria": "Fuel", "valor": 120.50, "data": "2023-10-27", "machine":"--"},
        ]

        return render_template('expenses.html', expenses=expenses)

@app.route('/machinery', methods=['GET', 'POST'])
def machinery():
    if request.method == 'POST':
        machine_name = request.form.get("machine_name")
        categoria = request.form.get("categoria")
        date = request.form.get('date')
        valor = request.form.get("valor")
        machine_id = request.form.get('machine_id')
        status = request.form.get('status')

        random_image = f"tractors/{random.randint(1,3)}.jpg"
        photo_url = url_for('static', filename=random_image)

        '''
        inserção dos dados das maquinas no banco
        '''
        return redirect(url_for("machinery"))
    else:

        machines = [
                {
            'id': 1,
            'name': 'Trator John Deere',
            'valor': '150000',
            'status': 'Active', 
            'data': '2024-01-15',
            'type': 'tractor',
            'serial': 'JD12345',
            'img_url': 'http://localhost:5000/static/tractors/1.jpg',
            'horas_w': '250',
            'prox_w': '2024-12-01'
        },
        {
            'id': 2,
            'name': 'Colheitadeira Case',
            'valor': '350000',
            'status': 'Maintenance',
            'data': '2023-08-20',
            'type': 'harvester',
            'serial': 'CS67890',
            'img_url': 'http://localhost:5000/static/tractors/2.jpg',
            'horas_w': '180',
            'prox_w': '2024-11-15'
        }
        ]

        return render_template('machinery.html', machines=machines)

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        product_name = request.form.get("product_name")
        categoria = request.form.get("categoria")
        quantidade = request.form.get("quantidade")
        unidade_medida = request.form.get("unidade_medida")
        storage_location = request.form.get("storage_location")
        '''
        inserção dos dados das despesas no banco
        '''
    else:
        products = [
            {
                "id": 1,
               "name": 'Organic Wheat Seed',
                "type": 'Seed',
                "location": 'Warehouse B, Section 3',
                "quantity": 250,
                "unit": 'kg',
                "value": 15.50
            }
        ]
            
        return render_template('products.html', products=products)

@app.route('/harvest', methods=['GET', 'POST'])
def harvest():
    if request.method == 'POST':
        if 'crop_name' in request.form:
            crop_name = request.form.get("crop_name")
            date = request.form.get("date")
            expected_date = request.form.get("expected_date")
            estimated_yield = request.form.get("estimated_yield")
            unidade_medida = request.form.get("unidade_medida")
            initial_cost = request.form.get("initial_cost")

            random_image = f"harvest/{random.randint(1,3)}.jpg"
            photo_url = url_for('static', filename=random_image)
            '''
            inserção dos dados das despesas no banco
            '''
            return redirect(url_for("harvest"))
    else:

        harvest = [
            {
                "id":1,
                "crop_name": "corn",
                "planting_date": "12 / 11 / 2024",
                "harvest_date": "04 / 02 / 2025",
                "estimated_yield": "10",
                "unit": "kg",
                "cost": "1200",
                "url_photo" : "http://localhost:5000/static/harvest/2.jpg",

                #dados que serao calculados
                "porcentagem":"60",
                "status": "crescendo"
            }
        ]
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
