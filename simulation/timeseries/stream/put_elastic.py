from utils import httputils
from elasticsearch import Elasticsearch
import http.client
import os

url     = os.environ.get('URL_ELK', 'localhost:9200')     #export URL_ELK=localhost:9200
user    = os.environ.get('USER_ELK')    #export USER_ELK=None
senha   = os.environ.get('PWD_ELK')     #export PWD_ELK=None

def sendDataElastic(envio, index):
    es = None
    if(user and senha):
        es = Elasticsearch(['https://'+url], http_auth=(user, senha))
    else:
        es = Elasticsearch(['http://' + url])

    res = es.index(index=index, body=envio)
    return res

def sendBulkElastic(envio):
    params = envio
    headers = httputils.setHeaders(user, senha, "application/x-ndjson")

    conn = None
    if (user and senha):
        conn = http.client.HTTPSConnection(url)
    else:
        conn = http.client.HTTPConnection(url)

    conn.request("POST", "/_bulk", params, headers)

    response = conn.getresponse()

    print('Status do Elasticsearch -> ' + str(response.status) + ' - ' + response.reason)

    conn.close()