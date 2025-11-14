from flask import Flask
from random_forest import RandomForestModel

model_roupas = RandomForestModel()
model_alimentos = RandomForestModel()
model_farmacia = RandomForestModel()

model_roupas.treinar_modelo("data/vendas_roupas.csv")
model_alimentos.treinar_modelo("data/hipermercado.csv", "2014")
model_farmacia.treinar_modelo("data/farmacia_cosmeticos.csv", "2018")

app = Flask(__name__)


@app.route("/health")
def health():
    return "Server OK!"

@app.route("/obter_previsao/roupas/<ano>/<mes>")
def previsao_roupas(ano, mes):
    try:
        mes = int(mes)
        ano = int(ano)

        previsao = str(model_roupas.prever(mes, ano))
    except Exception as e:
        return e.args[0]
    else:
        return previsao
    
@app.route("/obter_previsao/alimentos/<ano>/<mes>")
def previsao_alimentos(ano, mes):
    try:
        mes = int(mes)
        ano = int(ano)

        previsao = str(model_alimentos.prever(mes, ano))
    except Exception as e:
        return e.args[0]
    else:
        return previsao
    
@app.route("/obter_previsao/farmacia/<ano>/<mes>")
def previsao_farmacia(ano, mes):
    try:
        mes = int(mes)
        ano = int(ano)

        previsao = str(model_farmacia.prever(mes, ano))
    except Exception as e:
        return e.args[0]
    else:
        return previsao