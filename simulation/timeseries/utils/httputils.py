import base64

'''
    Criação de chave no Elastic
    POST /_security/api_key
    {
      "name": "my-api-key"
    }

    key = {
        "id": "XXXXXXXXXXXXXXXXXXXX",
        "name": "my-api-key",
        "api_key": "YYYYYYYYYYYYYYYYY"
    }
'''

def setHeaders(key, contextType):

    senha = "ApiKey " + base64.b64encode((key['id'] + ':' + key['api_key']).encode()).decode("utf-8")

    headers = {
        "Content-type": contextType,
        "Accept": "application/json",
        "Authorization": senha
    }

    return headers