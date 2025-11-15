import boto3

def obterCSVsDoS3(arquivos:list):
    s3 = boto3.client('s3')

    for arquivo in arquivos:
        s3.download_file('raw-paymetrics', f'bruno/ipea/{arquivo}.csv', f'data/{arquivo}_bucket.csv')
