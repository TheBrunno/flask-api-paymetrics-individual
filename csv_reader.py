import pandas as pd

class CsvReader:
    def __init__(self, csv_local):
        self.__csv_local = csv_local
        self.__df_csv = pd.read_csv(csv_local, parse_dates=["Data"]).drop('Unnamed: 2', axis=1)

    def obter_semestre(self):
        last_date = self.__df_csv.iloc[-1, 0]
        inicio_semestre = last_date.month - 6
        ano = last_date.year

        if inicio_semestre <= 0:
            ano -= 1
            inicio_semestre = 12+inicio_semestre

        return self.__df_csv[(self.__df_csv['Data'] > f'{ano}-{inicio_semestre}-01') & (self.__df_csv['Data'] <= last_date)]
    
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

if __name__ == "__main__":
    csv = CsvReader("data/vendas_roupas_bucket.csv", ["2020-04-01", "2025-08-01"])
    print(csv.obter_semestre())