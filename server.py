from flask import Flask

from random_forest import RandomForestModel
from get_bucket import obterCSVsDoS3

arquivos = [
    "vendas_roupas", "hipermercado", "farmacia_cosmeticos", "moveis_eletrodomesticos"
]

obterCSVsDoS3(arquivos)

model_roupas = RandomForestModel()
model_alimentos = RandomForestModel()
model_farmacia = RandomForestModel()
model_moveis = RandomForestModel()

model_roupas.treinar_modelo(f"data/{arquivos[0]}_bucket.csv")
model_alimentos.treinar_modelo(f"data/{arquivos[1]}_bucket.csv", "2014")
model_farmacia.treinar_modelo(f"data/{arquivos[2]}_bucket.csv", "2018")
model_moveis.treinar_modelo(f"data/{arquivos[3]}_bucket.csv", "2008")

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
    
@app.route("/obter_previsao/moveis/<ano>/<mes>")
def previsao_moveis(ano, mes):
    try:
        mes = int(mes)
        ano = int(ano)

        previsao = str(model_moveis.prever(mes, ano))
    except Exception as e:
        return e.args[0]
    else:
        return previsao