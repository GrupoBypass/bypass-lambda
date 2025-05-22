import boto3
import json
import csv
from io import StringIO
import os

s3 = boto3.client('s3')

BUCKET_DESTINO = 'trusted-bypass'

def lambda_handler(event, context):
    bucket_origem = event['Records'][0]['s3']['bucket']['name']
    chave_entrada = event['Records'][0]['s3']['object']['key']
    
    print(f'Novo arquivo recebido: {chave_entrada} do bucket {bucket_origem}')
    
    try:
        response = s3.get_object(Bucket=bucket_origem, Key=chave_entrada)
        conteudo_json = json.loads(response['Body'].read().decode('utf-8'))

        if not conteudo_json:
            print("JSON está vazio")
            return {'statusCode': 204, 'body': 'JSON vazio'}

        nome_base = os.path.basename(chave_entrada).replace('.json', '.csv')
        chave_csv_destino = f'saidas/{nome_base}'

        csv_buffer = StringIO()
        campos = conteudo_json[0].keys()
        writer = csv.DictWriter(csv_buffer, fieldnames=campos)
        writer.writeheader()
        writer.writerows(conteudo_json)

        s3.put_object(
            Bucket=BUCKET_DESTINO,
            Key=chave_csv_destino,
            Body=csv_buffer.getvalue()
        )

        print(f"CSV salvo no bucket {BUCKET_DESTINO} com chave {chave_csv_destino}")
        return {
            'statusCode': 200,
            'body': f'Arquivo tratado salvo como: {chave_csv_destino}'
        }

    except Exception as e:
        print(f"Erro : {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Erro : {str(e)}'
        }
