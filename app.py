from flask import Flask, render_template,request

app = Flask(__name__)

@app.get("/")
def index():
    return render_template('index.html')

@app.get("/formulario")
def form():
    return render_template("formulario.html")

@app.route("/cardapio", methods=["Post"]) 
 def cardapio() 
  restricoes= request.form.getlist
  ("restricoes")

  pratos = [
     {
      "nome": "feijoada" 
      "image" : "feijoada.jpg"
      "restricoes" : []
      },
      {
         "nome" : "salada"
         "image" : "salada.jpg"
         "restricoes" : ["Vegano", "Vegetariano", "Leite", "Gluten"]
      },
      {
         "nome" : ""
      }
  ]

if __name__ == '__main__':
    app.run(debug=True)