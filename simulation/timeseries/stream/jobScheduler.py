import threading
from stream import loaddata
from stream import put_elastic
from stream import db_mem
from utils import hashutils, dateutils, numutils
import json
from kafka import KafkaProducer

class process():
    def __init__(self, _dados, intervalo, body, amplitude, index):
        self._dados     = _dados
        self.intervalo  = intervalo
        self.body       = body
        self.amplitude  = amplitude
        self.index      = index

    def run(self):
        if self.body != None:
            self.body.pop('metric', None)
            self.body.pop('data', None)
            self.body.pop('index', None)

            outlier, indice_aplicado = db_mem.getOutlier(hashutils.gerarHash(json.dumps(self.body)), self.index)
            agora = dateutils.dateutils().dataAtual()
            valor = loaddata.getValor(self._dados, agora)
            if outlier != None:
                print('Processando outlier.... >>>><<<<< ' + json.dumps(self.body))
                db_mem.removerOutlier(hashutils.gerarHash(json.dumps(self.body)), self.index)
                self.body["metric"] = valor * indice_aplicado
            else:
                self.body["metric"] = valor + numutils.calcRandom(self.amplitude, 0.05)

            self.body["data"] = agora.strftime("%Y-%m-%dT%H:%M:%SZ")
            elk = put_elastic.ManagerElastic()
            res = elk.sendDataElastic(self.body, self.index)

            self.body["index"] = self.index

            producer = KafkaProducer(bootstrap_servers='localhost:9092', \
                                     value_serializer=lambda v: json.dumps(self.body).encode('utf-8'))
            producer.send('topic_test', self.body)
            producer.close()

            print('Status do Elasticsearch -> ' + res['result'] + json.dumps(self.body))

def startEvent(_dados, intervalo, body, amplitude, index):
    threading.Timer(intervalo, startEvent, [_dados, intervalo, body, amplitude, index]).start() #Executa a cada um minuto
    process(_dados, intervalo, body, amplitude, index).run()