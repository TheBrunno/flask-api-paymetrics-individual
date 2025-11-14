from flask import Flask

from random_forest import RandomForestModel
from get_bucket import obterCSVsDoS3
from csv_reader import CsvReader

arquivos_do_bucket = [
    "vendas_roupas", "hipermercado", "farmacia_cosmeticos", "moveis_eletrodomesticos"
]

# obterCSVsDoS3(arquivos_do_bucket)

model_roupas = RandomForestModel()
model_alimentos = RandomForestModel()
model_farmacia = RandomForestModel()
model_moveis = RandomForestModel()

csv_reader_roupas = CsvReader(f"data/{arquivos_do_bucket[0]}_bucket.csv")
csv_reader_alimentos = CsvReader(f"data/{arquivos_do_bucket[1]}_bucket.csv")
csv_reader_farmacia = CsvReader(f"data/{arquivos_do_bucket[2]}_bucket.csv")
csv_reader_moveis = CsvReader(f"data/{arquivos_do_bucket[3]}_bucket.csv")

model_roupas.treinar_modelo(f"data/{arquivos_do_bucket[0]}_bucket.csv")
model_alimentos.treinar_modelo(f"data/{arquivos_do_bucket[1]}_bucket.csv", "2014")
model_farmacia.treinar_modelo(f"data/{arquivos_do_bucket[2]}_bucket.csv", "2018")
model_moveis.treinar_modelo(f"data/{arquivos_do_bucket[3]}_bucket.csv", "2008")

app = Flask(__name__)


@app.route("/health")
def health():
    return "Server OK!"

@app.route("/obter/historico/roupas/semestre")
def historico_roupas_semestre():
    return csv_reader_roupas.obter_semestre_json()

@app.route("/obter/historico/alimentos/semestre")
def historico_alimentos_semestre():
    return csv_reader_alimentos.obter_semestre_json()

@app.route("/obter/historico/farmacia/semestre")
def historico_farmacia_semestre():
    return csv_reader_farmacia.obter_semestre_json()

@app.route("/obter/historico/moveis/semestre")
def historico_moveis_semestre():
    return csv_reader_moveis.obter_semestre_json()

@app.route("/obter/previsao/roupas/<ano>/<mes>")
def previsao_roupas(ano, mes):
    try:
        mes = int(mes)
        ano = int(ano)

        previsao = str(model_roupas.prever(mes, ano))
    except Exception as e:
        return e.args[0]
    else:
        return previsao
    
@app.route("/obter/previsao/alimentos/<ano>/<mes>")
def previsao_alimentos(ano, mes):
    try:
        mes = int(mes)
        ano = int(ano)

        previsao = str(model_alimentos.prever(mes, ano))
    except Exception as e:
        return e.args[0]
    else:
        return previsao
    
@app.route("/obter/previsao/farmacia/<ano>/<mes>")
def previsao_farmacia(ano, mes):
    try:
        mes = int(mes)
        ano = int(ano)

        previsao = str(model_farmacia.prever(mes, ano))
    except Exception as e:
        return e.args[0]
    else:
        return previsao
    
@app.route("/obter/previsao/moveis/<ano>/<mes>")
def previsao_moveis(ano, mes):
    try:
        mes = int(mes)
        ano = int(ano)

        previsao = str(model_moveis.prever(mes, ano))
    except Exception as e:
        return e.args[0]
    else:
        return previsao