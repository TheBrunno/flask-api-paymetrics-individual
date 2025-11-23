from flask import Flask

from random_forest import RandomForestModel
from get_bucket import obterCSVsDoS3
from csv_reader import CsvReader
from datetime import datetime
from flask_cors import CORS

arquivos_do_bucket = [
    "PMC12_VNVESTN12",
    "PMC12_VRSUPN12",
    "PMC12_VRFARMN12",
    "PMC12_VRELETRN12"
]

obterCSVsDoS3(arquivos_do_bucket)

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

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/health")
def health():
    return "Server OK!"

@app.route("/obter/previsao/ano/roupas/<anos>/<meses>")
def previsao_roupas_ano(anos, meses):
    if anos == "-":
        hist = csv_reader_roupas.obter_meses_json("-")
    else:
        hist = csv_reader_roupas.obter_meses_json((int(anos)*12)-int(meses))
    prev = []
    last_hist_date = hist[len(hist)-1]["data"]

    mes_comp = last_hist_date.month
    ano_comp = last_hist_date.year

    for _ in range(int(meses)):
        mes_comp+=1

        if mes_comp > 12:
            mes_comp = 1
            ano_comp += 1

        nova_data = datetime(ano_comp, mes_comp, 1)

        prev.append(
            {
                "vendas": model_roupas.prever(mes_comp, ano_comp),
                "previsao": True,
                "data": nova_data,
                "mae": model_roupas.mae
            }
        )
    
    return hist+prev

@app.route("/obter/previsao/ano/alimentos/<anos>/<meses>")
def previsao_alimentos_ano(anos, meses):
    if anos == "-":
        hist = csv_reader_alimentos.obter_meses_json("-")
    else:
        hist = csv_reader_alimentos.obter_meses_json((int(anos)*12)-int(meses))
    prev = []
    last_hist_date = hist[len(hist)-1]["data"]

    mes_comp = last_hist_date.month
    ano_comp = last_hist_date.year

    for _ in range(int(meses)):
        mes_comp+=1

        if mes_comp > 12:
            mes_comp = 1
            ano_comp += 1

        nova_data = datetime(ano_comp, mes_comp, 1)

        prev.append(
            {
                "vendas": model_alimentos.prever(mes_comp, ano_comp),
                "previsao": True,
                "data": nova_data,
                "mae": model_alimentos.mae
            }
        )
    
    return hist+prev

@app.route("/obter/previsao/ano/farmacia/<anos>/<meses>")
def previsao_farmacia_ano(anos, meses):
    if anos == "-":
        hist = csv_reader_farmacia.obter_meses_json("-")
    else:
        hist = csv_reader_farmacia.obter_meses_json((int(anos)*12)-int(meses))
    prev = []
    last_hist_date = hist[len(hist)-1]["data"]

    mes_comp = last_hist_date.month
    ano_comp = last_hist_date.year

    for _ in range(int(meses)):
        mes_comp+=1

        if mes_comp > 12:
            mes_comp = 1
            ano_comp += 1

        nova_data = datetime(ano_comp, mes_comp, 1)

        prev.append(
            {
                "vendas": model_farmacia.prever(mes_comp, ano_comp),
                "previsao": True,
                "data": nova_data,
                "mae": model_farmacia.mae
            }
        )
    
    return hist+prev

@app.route("/obter/previsao/ano/moveis/<anos>/<meses>")
def previsao_moveis_ano(anos, meses):
    if anos == "-":
        hist = csv_reader_moveis.obter_meses_json("-")
    else:
        hist = csv_reader_moveis.obter_meses_json((int(anos)*12)-int(meses))
    prev = []
    last_hist_date = hist[len(hist)-1]["data"]

    mes_comp = last_hist_date.month
    ano_comp = last_hist_date.year

    for _ in range(int(meses)):
        mes_comp+=1

        if mes_comp > 12:
            mes_comp = 1
            ano_comp += 1

        nova_data = datetime(ano_comp, mes_comp, 1)

        prev.append(
            {
                "vendas": model_moveis.prever(mes_comp, ano_comp),
                "previsao": True,
                "data": nova_data,
                "mae": model_moveis.mae
            }
        )
    
    return hist+prev

# obter historico anos
@app.route("/obter/historico/roupas/anual/<anos>")
def historico_roupas_semestre_anual(anos):
    return csv_reader_roupas.obter_anual_json(anos)

@app.route("/obter/historico/alimentos/anual/<anos>")
def historico_alimentos_semestre_anual(anos):
    return csv_reader_alimentos.obter_anual_json(anos)

@app.route("/obter/historico/farmacia/anual/<anos>")
def historico_farmacia_semestre_anual(anos):
    return csv_reader_farmacia.obter_anual_json(anos)

@app.route("/obter/historico/moveis/anual/<anos>")
def historico_moveis_semestre_anual(anos):
    return csv_reader_moveis.obter_anual_json(anos)

# obter ultimo semestre
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

# prever passando ano e mes
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
    
@app.route("/obter/previsao/prox/roupas")
def previsao_roupas_prox():
    try:
        month = datetime.now().month
        year = datetime.now().year

        if month == 12:
            month = 1
            year+=1
        else:
            month+=1

        previsao = model_roupas.prever(month, year)
        variacao = model_roupas.variacao(previsao)
        return { "previsao": previsao, "variacao": variacao }
    except Exception as e:
        return e.args[0]

# prox mes
@app.route("/obter/previsao/prox/alimentos")
def previsao_alimentos_prox():
    try:
        month = datetime.now().month
        year = datetime.now().year

        if month == 12:
            month = 1
            year+=1
        else:
            month+=1

        previsao = model_alimentos.prever(month, year)
        variacao = model_alimentos.variacao(previsao)
        return { "previsao": previsao, "variacao": variacao }
    except Exception as e:
        return e.args[0]
        
@app.route("/obter/previsao/prox/farmacia")
def previsao_farmacia_prox():
    try:
        month = datetime.now().month
        year = datetime.now().year

        if month == 12:
            month = 1
            year+=1
        else:
            month+=1

        previsao = model_farmacia.prever(month, year)
        variacao = model_farmacia.variacao(previsao)
        return { "previsao": previsao, "variacao": variacao }
    except Exception as e:
        return e.args[0]
    
@app.route("/obter/previsao/prox/moveis")
def previsao_moveis_prox():
    try:
        month = datetime.now().month
        year = datetime.now().year

        if month == 12:
            month = 1
            year+=1
        else:
            month+=1

        previsao = model_moveis.prever(month, year)
        variacao = model_moveis.variacao(previsao)
        return { "previsao": previsao, "variacao": variacao }
    except Exception as e:
        return e.args[0]
    

@app.route("/obter/limites/data")
def obter_limites():
    roupas = csv_reader_roupas.obter_limites()
    roupas["type"] = "roupas"
    alimentos = csv_reader_alimentos.obter_limites()
    alimentos["type"] = "alimentos"
    farmacia = csv_reader_farmacia.obter_limites()
    farmacia["type"] = "farmacia"
    moveis = csv_reader_moveis.obter_limites()
    moveis["type"] = "moveis"

    return [roupas, alimentos, farmacia, moveis]