import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

class RandomForestModel:
    def __init__(self):
        self.__model = None
        self.__df = None

    def treinar_modelo(self, csv_local):
        print("""\n\n\n
            Treinando o modelo Random Forest
        \n\n\n""")

        df_csv = pd.read_csv(csv_local, parse_dates=["Data"]).drop('Unnamed: 2', axis=1)

        df_csv = df_csv[(df_csv['Data'] > '2000-04-01') & (df_csv['Data'] <= '2025-08-01')]

        df_csv["vendas_lag1"] = df_csv["vendas_roupas"].shift(1)
        df_csv["vendas_ano_passado"] = df_csv["vendas_roupas"].shift(12)

        df_csv["mes"] = df_csv["Data"].dt.month
        df_csv["ano"] = df_csv["Data"].dt.year

        self.__df = df_csv.copy()

        self.__df = self.__df.dropna()

        X = self.__df[[
            "vendas_lag1", "vendas_ano_passado", "mes", "ano"
        ]]
        y = self.__df["vendas_roupas"]

        split = int(len(self.__df) * 0.90)
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        self.__model = RandomForestRegressor(
            n_estimators=1000,
            max_depth=6,
            min_samples_leaf=3,
            random_state=42
        )
        self.__model.fit(X_train, y_train)
        y_pred = self.__model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"\n\nMAE: {mae:.2f}")
        print(f"R²: {r2:.3f}\n\n")

        return self.__df, self.__model


    def prever(self, mes, ano):
        try:
            mes_passado_num = mes
            ano_passado_num = ano

            if mes-1 == 0:
                mes_passado_num = 12
                ano_passado_num = ano-1
                
            ano_passado = self.__df[(self.__df["mes"] == mes) & (self.__df["ano"] == ano-1)]
            
            mes_passado = self.__df[(self.__df["mes"] == mes_passado_num) & (self.__df["ano"] == ano_passado_num)]

            key = "vendas_roupas"
            if mes_passado.empty:
                mes_passado = ano_passado
                key = "vendas_lag1"

            proxima = pd.DataFrame([{
                "vendas_lag1": mes_passado[key],
                "vendas_ano_passado": ano_passado["vendas_roupas"],
                
                "mes": mes,
                "ano": ano
            }])

            return self.__model.predict(proxima)[0]
        except:
            raise ValueError("Insira um valor dentro do esperado!")



if __name__ == "__main__":
    random_forest = RandomForestModel()
    random_forest.treinar_modelo("./data/vendas_roupas.csv")
    random_forest.prever(12, 2025)