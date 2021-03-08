# IClinic Prescriptions API - Backend Python Challenge

## Objetivo:
  - Criar um endpoint que recebe algumas informações, complementa essas informações com consultas em outras API, e envia este dado completo pra uma outra API.


## Ferramentas Utilizadas:
 - Python 3+
 - Fast API
 - Pydantic
 - SQL Alchemy
 - AWS SAM
 - AWS Dynamodb
 - AWS Lambda
 - AWS RDS(MySQL)
 - AWS API Gateway
 - AWS SSM
 - Docker Compose

## Como rodar:
 - Por se tratar de uma aplicação serverless, não tem necessidade de subir um servidor. Ao bater no endpoint o lambda já será invocado.
 - cURL exemplo:
   - ``` 
        curl --request POST \
            --url https://rc5jwobush.execute-api.us-east-1.amazonaws.com/Api/v1/prescriptions \
            --header 'Content-Type: application/json' \
            --data '{
            "clinic": {
                "id": 2
            },
            "physician": {
                "id": 3
            },
            "patient": {
                "id": 5
            },
            "text": "Prescricao medica"
        }'

## Cache:
 - Por se tratar de uma aplicação serverless foi necessário um cache de duas partes.
 - Primeiro tento extrair o cache da memória. Caso não consiga encontrar, tento extrair do DynamoDB. 
 - Caso nenhum desses tenha sucesso, consultamos as APIs

## Testes
 - A cobertura dos testes está em 99%
 - comando `make build` para montar o container
 - comando `make test` se quiser apenas rodar os testes e ver o coverage
