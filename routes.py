from flask import render_template, request, redirect, url_for, flash
from models import *
from datetime import datetime

def routes(app):
    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            # --- Dados da produção ---
            id_producao = request.form.get("id_producao")
            densidade = request.form.get("densidade")
            comp_a = request.form.get("comp_a")
            comp_b = request.form.get("comp_b")
            comp_c = request.form.get("comp_c")

            if id_producao and densidade:
                # Cria produção
                nova_producao = Producao(id_producao=id_producao, densidade=densidade)
                db.session.add(nova_producao)
                db.session.commit()  # gera o nova_producao.id

                # Cria componentes associados
                novo_componente = ComponenteProducao(
                    comp_a=float(comp_a),
                    comp_b=float(comp_b),
                    comp_c=float(comp_c),
                    producao_id=nova_producao.id
                )
                db.session.add(novo_componente)
                db.session.commit()

                flash(f"Produção '{id_producao}' cadastrada com sucesso!", "success")
                return redirect(url_for("index"))

        producoes = Producao.query.all()
        return render_template("form.html", producoes=producoes)

    @app.route("/producao/<int:producao_id>/componentes")
    def ver_componentes(producao_id):
        producao = Producao.query.get_or_404(producao_id)
        return render_template("componentes.html", producao=producao)
