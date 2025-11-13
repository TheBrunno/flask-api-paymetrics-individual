from flask import Flask
from random_forest import RandomForestModel

model_roupas = RandomForestModel()
model_roupas.treinar_modelo("data/vendas_roupas.csv")

app = Flask(__name__)


@app.route("/health")
def health():
    return "Server OK!"

@app.route("/obter_previsao/roupas/<ano>/<mes>")
def previsao(ano, mes):
    try:
        mes = int(mes)
        ano = int(ano)

        previsao = str(model_roupas.prever(mes, ano))
    except Exception as e:
        return e.args[0]
    else:
        return previsao