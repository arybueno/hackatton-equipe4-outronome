from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def index():
    return "<h1>Olá</h1>"


if __name__ == '__main__':
    app.run(debug=True)