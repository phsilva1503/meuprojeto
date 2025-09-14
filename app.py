from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo do Usuário
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    cor = db.Column(db.String(20))

# Cria o banco e as tabelas (se não existirem)
with app.app_context():
    db.create_all()

# Rota principal com formulário
@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = None  # inicializa a variável
    if request.method == "POST":
        nome = request.form.get("nome")
        idade = request.form.get("idade")
        cor = request.form.get("cor")

        if nome and idade:
            usuario = Users(nome=nome, idade=int(idade),  cor=cor)
            db.session.add(usuario)
            db.session.commit()
            mensagem = f"Usuário {nome} cadastrado com sucesso!"
    
    usuarios = Users.query.all()
    return render_template("form.html", mensagem=mensagem, usuarios=usuarios)

    

if __name__ == "__main__":
    app.run(debug=True)
