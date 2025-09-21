from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()


class Produto(db.Model):
    __tablename__ = "Produto"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Produto {self.nome}>"


class Producao(db.Model):
    __tablename__ = "Producao"
    id = db.Column(db.Integer, primary_key=True)
    id_producao = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date, default=date.today, nullable=False)
    densidade = db.Column(db.String(20))

    componentes = db.relationship("ComponenteProducao", backref="Producao", lazy=True)

    def __repr__(self):
        return f"<Producao {self.id_producao}>"


class ComponenteProducao(db.Model):
    __tablename__ = "ComponenteProducao"
    id = db.Column(db.Integer, primary_key=True)
    producao_id = db.Column(db.Integer, db.ForeignKey("Producao.id"))
    produto_id = db.Column(db.Integer, db.ForeignKey("Produto.id"))
    quantidade_usada = db.Column(db.Float, nullable=False)

    produto = db.relationship("Produto")

    def __repr__(self):
        return f"<ComponenteProducao Produção={self.producao_id}, Produto={self.produto_id}, Qtd={self.quantidade_usada}>"

__all__ = ["db", "Produto", "Producao", "ComponenteProducao"]
