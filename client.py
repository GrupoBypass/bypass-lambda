import boto3
import csv
from io import StringIO
import os
from datetime import datetime

s3 = boto3.client('s3')

BUCKET_ORIGEM = 'trusted-bypass'
BUCKET_DESTINO = 'client-bypass'

def lambda_handler(event, context):
    try:
        bucket_origem = event['Records'][0]['s3']['bucket']['name']
        chave_csv = event['Records'][0]['s3']['object']['key']
        
        print(f'Novo CSV para cliente recebido: {chave_csv}')

        response = s3.get_object(Bucket=bucket_origem, Key=chave_csv)
        conteudo_csv = response['Body'].read().decode('utf-8')
        leitor_csv = csv.DictReader(StringIO(conteudo_csv))
        
        dados_convertidos = []

        novo_cabecalho = {
            'dataHora': 'Data e Hora',
            'statusDPS': 'Status',
            'picoTensao_kV': 'Pico de Tensão (kV)',
            'correnteSurto_kA': 'Corrente de Surto (kA)'
        }

        for linha in leitor_csv:
            data_formatada = datetime.strptime(linha['dataHora'], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")
            
            nova_linha = {
                'Data e Hora': data_formatada,
                'Status': 'Normal' if linha['statusDPS'] == 'OK' else 'Crítico',
                'Pico de Tensão (kV)': linha['picoTensao_kV'],
                'Corrente de Surto (kA)': linha['correnteSurto_kA']
            }
            dados_convertidos.append(nova_linha)

        nome_arquivo = os.path.basename(chave_csv).replace('.csv', '_cliente.csv')
        nova_chave = f'clientes/{nome_arquivo}'

        csv_buffer = StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=list(novo_cabecalho.values()))
        writer.writeheader()
        writer.writerows(dados_convertidos)

        s3.put_object(
            Bucket=BUCKET_DESTINO,
            Key=nova_chave,
            Body=csv_buffer.getvalue()
        )

        print(f"Arquivo pronto para cliente salvo como: {nova_chave}")
        return {
            'statusCode': 200,
            'body': f'Arquivo salvo para cliente: {nova_chave}'
        }

    except Exception as e:
        print(f"Erro: {str(e)}")
        return {
            'statusCode': 500,
            'body': str(e)
        }
