# vai p um lambda na aws -> responsavel por atualizar os csvs do bucket

import requests
import pandas as pd
import boto3

cod_series = [
    "PMC12_VNVESTN12",
    "PMC12_VRSUPN12",
    "PMC12_VRFARMN12",
    "PMC12_VRELETRN12"
]

def send_bucket(file_name, bucket, object_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_name, bucket, object_name)

for cod_serie in cod_series:
    response = requests.get(f"https://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{cod_serie}')").json()

    data = {
        "Data": [],
        "vendas": []
    }

    for value in response["value"]:
        data["Data"].append(value["VALDATA"])
        data["vendas"].append(value["VALVALOR"])

    pd.DataFrame(data=data).to_csv(f"data_ipea/{cod_serie}.csv", index=False)
    send_bucket(f"data_ipea/{cod_serie}.csv", "raw-paymetrics", f"bruno/ipea/{cod_serie}.csv")
