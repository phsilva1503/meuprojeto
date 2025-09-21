from flask import render_template, request, redirect, url_for, flash
from models import *
from datetime import date

def routes(app):

    # Inserir produtos fixos se não existirem
    def criar_produtos_fixos():
        produtos_fixos = ["Produto A", "Produto B", "Produto C"]
        for nome in produtos_fixos:
            if not Produto.query.filter_by(nome=nome).first():
                db.session.add(Produto(nome=nome))
        db.session.commit()

    @app.route("/", methods=["GET", "POST"])
    def index():
        # Garantir que os produtos fixos existam
        criar_produtos_fixos()

        produtos = Produto.query.all()  # produtos fixos para exibir no formulário

        if request.method == "POST":
            id_producao = request.form.get("id_producao")
            densidade = request.form.get("densidade")

            if id_producao and densidade:
                # Cria a produção
                producao = Producao(id_producao=id_producao, densidade=densidade)
                db.session.add(producao)
                db.session.flush()  # gera o ID sem commitar

                # Para cada produto, cria ComponenteProducao
                for produto in produtos:
                    campo_nome = f"produto_{produto.id}"  # nome do input no form
                    qtd = request.form.get(campo_nome, 0)
                    try:
                        quantidade_valor = float(qtd)
                    except (ValueError, TypeError):
                        quantidade_valor = 0

                    componente = ComponenteProducao(
                        producao_id=producao.id,
                        produto_id=produto.id,
                        quantidade_usada=quantidade_valor
                    )
                    db.session.add(componente)

                db.session.commit()  # commit único após salvar produção e componentes
                flash(f"Produção '{id_producao}' cadastrada com sucesso!", "success")
                return redirect(url_for("index"))

        producoes = Producao.query.all()
        return render_template("form.html", producoes=producoes, produtos=produtos)

    @app.route("/producao/<int:producao_id>/componentes")
    def ver_componentes(producao_id):
        producao = Producao.query.get_or_404(producao_id)
        componentes = ComponenteProducao.query.filter_by(producao_id=producao.id).all()
        produtos = Produto.query.all()  # para mostrar todos os produtos no relatório
        return render_template("componentes.html", producao=producao, componentes=componentes, produtos=produtos)
