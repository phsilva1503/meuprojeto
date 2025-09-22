from flask import render_template, request, redirect, url_for, flash
from models import *
from datetime import date

def routes(app):

    # --- Função para criar produtos fixos ---
    def criar_produtos_fixos():
        produtos_fixos = ["Produto A", "Produto B", "Produto C"]
        for nome in produtos_fixos:
            if not Produto.query.filter_by(nome=nome).first():  # só insere se não existir
                db.session.add(Produto(nome=nome))
        db.session.commit()

    # --- Função para calcular saldo de estoque ---
    def calcular_saldo(produto_id):
        entradas = db.session.query(db.func.sum(Movimentacao.quantidade))\
            .filter_by(produto_id=produto_id, tipo='entrada').scalar() or 0
        saidas = db.session.query(db.func.sum(Movimentacao.quantidade))\
            .filter_by(produto_id=produto_id, tipo='saida').scalar() or 0
        return entradas - saidas

    # --- Cadastro de novos produtos ---
    @app.route("/cadastro_produto", methods=["GET", "POST"])
    def cadastro_produto():
        if request.method == "POST":
            nome = request.form.get("nome")
            if nome and not Produto.query.filter_by(nome=nome).first():
                db.session.add(Produto(nome=nome))
                db.session.commit()
                flash(f"Produto '{nome}' cadastrado com sucesso!", "success")
            else:
                flash("Produto já existe ou nome inválido!", "danger")
            return redirect(url_for("cadastro_produto"))

        produtos = Produto.query.all()
        return render_template("CadastroProduto.html", produtos=produtos)

    # --- Página principal: cadastro de produção ---
    @app.route("/", methods=["GET", "POST"])
    def index():
        produtos = Produto.query.all()

        if request.method == "POST":
            id_producao = request.form.get("id_producao")
            densidade = request.form.get("densidade")

            if id_producao and densidade:
                producao = Producao(id_producao=id_producao, densidade=densidade, data=date.today())
                db.session.add(producao)
                db.session.flush()  # gera o ID sem commitar

                for produto in produtos:
                    campo_nome = f"produto_{produto.id}"
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

                    if quantidade_valor > 0:
                        db.session.add(Movimentacao(
                            produto_id=produto.id,
                            quantidade=quantidade_valor,
                            tipo='saida',
                            data=date.today(),
                            producao_id=producao.id
                        ))

                db.session.commit()
                flash(f"Produção '{id_producao}' cadastrada com sucesso!", "success")
                return redirect(url_for("index"))

        producoes = Producao.query.all()
        return render_template("form.html", producoes=producoes, produtos=produtos)

    # --- Visualizar componentes de uma produção ---
    @app.route("/producao/<int:producao_id>/componentes")
    def ver_componentes(producao_id):
        producao = Producao.query.get_or_404(producao_id)
        componentes = ComponenteProducao.query.filter_by(producao_id=producao.id).all()
        produtos = Produto.query.all()
        return render_template("componentes.html", producao=producao, componentes=componentes, produtos=produtos)

    # --- Página de estoque ---
    @app.route("/estoque")
    def estoque():
        produtos = Produto.query.all()
        saldos = {p.id: calcular_saldo(p.id) for p in produtos}
        return render_template("estoque.html", produtos=produtos, saldos=saldos)


    @app.route("/movimentacoes/<int:produto_id>")
    def movimentacoes(produto_id):
        produto = Produto.query.get_or_404(produto_id)
        movimentacoes = Movimentacao.query.filter_by(produto_id=produto.id).all()
        return render_template("movimentacoes.html", produto=produto, movimentacoes=movimentacoes)

    # --- Adicionar saldo ao estoque ---
    @app.route("/estoque/adicionar/<int:produto_id>", methods=["GET", "POST"])
    def AdicionarSaldo(produto_id):
        produto = Produto.query.get_or_404(produto_id)

        if request.method == "POST":
            try:
                quantidade = float(request.form.get("quantidade", 0))
                if quantidade <= 0:
                    flash("Informe uma quantidade válida maior que zero!", "danger")
                    return redirect(url_for("AdicionarSaldo", produto_id=produto.id))

                mov = Movimentacao(
                    produto_id=produto.id,
                    quantidade=quantidade,
                    tipo="entrada",
                    data=date.today()
                )
                db.session.add(mov)
                db.session.commit()
                flash(f"{quantidade} unidades adicionadas ao estoque do produto '{produto.nome}'", "success")
                return redirect(url_for("estoque"))
            except ValueError:
                flash("Quantidade inválida!", "danger")
                return redirect(url_for("AdicionarSaldo", produto_id=produto.id))

        return render_template("AdicionarSaldo.html", produto=produto)

    # --- Inicialização: criar produtos fixos dentro do app context ---
    with app.app_context():
        criar_produtos_fixos()
