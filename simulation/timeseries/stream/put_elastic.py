from utils import httputils
from elasticsearch import Elasticsearch
import http.client
import os

class ManagerElastic():

    def __init__(self):
        self.url     = os.environ.get('URL_ELK', 'localhost:9200')     #export URL_ELK=localhost:9200
        self.user    = os.environ.get('USER_ELK')    #export USER_ELK=None
        self.senha   = os.environ.get('PWD_ELK')     #export PWD_ELK=None

    def sendDataElastic(self, envio, index):
        es = None
        if(self.user and self.senha):
            es = Elasticsearch(['https://'+ self.url], http_auth=(self.user, self.senha))
        else:
            es = Elasticsearch(['http://' + self.url])

        res = es.index(index=index, body=envio)
        return res

    def sendBulkElastic(self, envio):
        params = envio
        headers = httputils.setHeaders("application/x-ndjson")

        conn = None
        if (self.user and self.senha):
            conn = http.client.HTTPSConnection(self.url)
        else:
            conn = http.client.HTTPConnection(self.url)

        conn.request("POST", "/_bulk", params, headers)

        response = conn.getresponse()

        print('Status do Elasticsearch -> ' + str(response.status) + ' - ' + response.reason)

        conn.close()