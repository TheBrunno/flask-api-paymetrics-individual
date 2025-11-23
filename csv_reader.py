import pandas as pd
from datetime import datetime

class CsvReader:
    def __init__(self, csv_local):
        self.__csv_local = csv_local
        self.__df_csv = pd.read_csv(csv_local, parse_dates=["Data"])

    def obter_meses(self, meses):
        if meses == "-":
            return self.__df_csv
        return self.__df_csv.tail(meses)

    def obter_meses_json(self, meses):
        dados = self.obter_meses(meses).to_dict()

        json = []
        dados["Data"] = list(dados["Data"].values())
        dados["vendas"] = list(dados["vendas"].values())

        for i in range(len(dados["Data"])):
            json.append({
                "data":dados["Data"][i],
                "vendas":dados["vendas"][i],
                "previsao": False
            })
        return json


    def obter_semestre(self):
        return self.__df_csv.tail(6)

    def obter_anual(self, anos):
        return self.__df_csv.tail(int(anos)*12)

    def obter_anual_json(self, anos):
        dados = self.obter_anual(anos).to_dict()
        
        json = []

        dados["Data"] = list(dados["Data"].values())
        dados["vendas"] = list(dados["vendas"].values())
        print(dados)

        for i in range(len(dados["Data"])):
            json.append({
                "data":dados["Data"][i],
                "vendas":dados["vendas"][i],
            })

        return json

    def obter_semestre_json(self):
        dados = self.obter_semestre().to_dict()
        
        json = []

        dados["Data"] = list(dados["Data"].values())
        dados["vendas"] = list(dados["vendas"].values())
        print(dados)

        for i in range(6):
            json.append({
                "data":dados["Data"][i],
                "vendas":dados["vendas"][i],
            })

        return json

    def getCsv(self):
        return self.__df_csv
    
    def obter_limites(self):
        ultima_data = self.__df_csv.tail(1)["Data"].iloc[0]

        year = ultima_data.year + 1
        month = ultima_data.month
        return { "month": month, "year": year }

if __name__ == "__main__":
    csv = CsvReader("data/vendas_roupas_bucket.csv", ["2020-04-01", "2025-08-01"])
    print(csv.obter_semestre())