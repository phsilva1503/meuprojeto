from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class Producao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_producao = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date,default=date.today, nullable=False)
    densidade = db.Column(db.String(20))
    componentes = db.relationship('Componente', backref='producao', lazy=True)

class Componente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comp_a = db.Column(db.Float)
    comp_b = db.Column(db.Float)
    comp_c = db.Column(db.Float)
    producao_id = db.Column(db.Integer, db.ForeignKey('producao.id'))

__all__ = ["db", "Producao", "Componente"]