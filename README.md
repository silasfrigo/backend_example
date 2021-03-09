# IClinic Prescriptions API - Backend Python Challenge

## Objetivo:
  - Criar um endpoint que recebe algumas informações, complementa essas informações com consultas em outras API, e envia este dado completo pra uma outra API.

## Informações Importantes:
 - Após alguns testes a API de Métricas não está mais funcionando corretamente. Retorna apenas -> Bad Request "Max number of elements reached for this resource!"


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

## Infra:
  - A montagem da infra estrutura do projeto é toda feita a partir do template SAM(template.yaml).

  - Ao rodar o comando `sam build --use-container` o stack é montado
  - Após ter o stack, executando o comando `sam deploy --config-env=dev --profile=SEU_PROFILE_AWS` toda a infra estrutura será "deployada", criando ou atualizando os serviços conforme necessidade. 
## Cache:
 - Por se tratar de uma aplicação serverless foi necessário um cache de duas partes.
 - Primeiro tento extrair o cache da memória. Caso não consiga encontrar, tento extrair do DynamoDB. 
 - Caso nenhum desses tenha sucesso, consultamos as APIs
 - Exemplo de um caso do cache não estar na memória mas estar no DynamoDB. (Logs do CloudWatch)
![cache_from_dynamo_to_file](https://user-images.githubusercontent.com/47428195/110357616-3b759a00-801a-11eb-9fc1-47bbad3fe125.png)


## Testes
 - A cobertura dos testes está em 99%
 - comando `make build` para montar o container
 - comando `make test` se quiser apenas rodar os testes e ver o coverage
![coverage](https://user-images.githubusercontent.com/47428195/110357418-049f8400-801a-11eb-868b-b2278223c7b0.png)

## Possiveis melhorias:
 - Pelo que conferi a autenticação dos serviços dependentes não estão funcionando. Não é validado o jwt enviado no headers. 
 - Uma melhoria possivel para esse sistemas seria fazer a chamada para os serviços complementares de maneira async.
 - Fazer com que não salve o clinics id no banco, quando o mesmo não obteve retorno da api dependente.