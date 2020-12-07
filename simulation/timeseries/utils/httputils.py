import base64

'''
    Criação de chave
    POST /_security/api_key
    {
      "name": "my-api-key"
    }

    key = {
        "id": "KHn-d3MBymALMAq3ILJz",
        "name": "my-api-key",
        "api_key": "TMYe_g0IRjSNacE91d-Ojg"
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