from flask import Flask, render_template, request, g
import sqlite3

DATABASE = 'restaurantes.db'
app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Optional: for dict-like row access
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        criacao_de_tabela = """
            CREATE TABLE IF NOT EXISTS restaurantes (
                id_restaurante INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                email TEXT,
                senha TEXT,
                imagem_principal BLOB
            )
        """

        tabela_filha = """
            CREATE TABLE IF NOT EXISTS comidas_restaurantes (
                id INTEGER PRIMARY KEY,
                restaurante_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                carne INTEGER NOT NULL,
                ovo INTEGER NOT NULL,
                leite INTEGER NOT NULL,
                gluten INTEGER NOT NULL,
                frutosdomar INTEGER NOT NULL,
                alcool INTEGER NOT NULL,
                amendoim INTEGER NOT NULL,
                soja INTEGER NOT NULL,
                nozesoucastanhas INTEGER NOT NULL,
                acucar INTEGER NOT NULL,
                foto BLOB,
                FOREIGN KEY (restaurante_id) REFERENCES restaurantes (id_restaurante)
            )
        """

        cursor.execute(criacao_de_tabela)
        cursor.execute(tabela_filha)

        # Check if the default user exists before inserting
        cursor.execute("SELECT * FROM restaurantes WHERE email = ?", ("batata",))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO restaurantes (email, senha) VALUES (?, ?)", ("batata", "batata"))

        conn.commit()

init_db()

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/<restaurante>/cardapio", methods=["POST"])
def get_data(restaurante):
    # You'll want to add functionality here later
    return f"Cardápio for {restaurante}"

@app.route("/adicionar_restricoes")
def print_data():
    return render_template("formulario.html")


@app.route("/pegar_comidas", methods=["POST"])
def pegar_comidas():
    vegano = request.form.get("vegano")
    lactose = request.form.get("lactose")
    gluten = request.form.get("gluten")
    vegetariano = request.form.get("vegetariano")
    restrictions = list()
    if vegano:
        restrictions.append(1)
    else:
        restrictions.append(0)
    if lactose:
        restrictions.append(1)
    else:
        restrictions.append(0)
    if gluten:
        restrictions.append(1)
    else:
        restrictions.append(0)
    if vegetariano:
        restrictions.append(1)
    else:
        restrictions.append(0)

    return render_template("cardapio.html", restricoes = restrictions)


@app.route("/login")
def login():
    return render_template("create_account.html")

@app.route("/process_form", methods=["POST"])
def get_coisas():
    email = request.form.get("email")
    senha = request.form.get("senha")

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM restaurantes WHERE email = ?", (email,))
    results = cursor.fetchall()

    print(results)

    if (results[0]["senha"] == senha):
        print("olha la ta certo!")

    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)
