import json
import urllib3

http = urllib3.PoolManager()

def lambda_handler(event, context):
    try:
        # --- Extrair o nome do arquivo e o bucket do evento S3 ---
        record = event['Records'][0]
        bucket_name = record['s3']['bucket']['name']
        file_key = record['s3']['object']['key']

        # --- Montar o payload do POST ---
        payload = {
            "key": file_key
        }

        # --- Fazer o POST para sua EC2 ---
        url = "http://ip-da-minha-ec/sensor-omron"  # substitua pelo IP público ou DNS da sua EC2
        headers = {"Content-Type": "application/json"}

        response = http.request(
            "POST",
            url,
            body=json.dumps(payload).encode("utf-8"),
            headers=headers
        )

        # --- Retornar resposta ---
        return {
            "statusCode": response.status,
            "body": response.data.decode("utf-8")
        }

    except Exception as e:
        print("Erro ao processar evento:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"erro": str(e)})
        }
