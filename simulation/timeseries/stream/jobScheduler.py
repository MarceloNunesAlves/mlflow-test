import threading
from stream import loaddata
from stream import put_elastic
from stream import db_mem
from utils import hashutils, dateutils
import json
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

def startEvent(_dados, intervalo, body, randVal, index):
    threading.Timer(intervalo, startEvent, [_dados, intervalo, body, randVal, index]).start() #Executa a cada um minuto
    if body != None:
        body.pop('metric', None)
        body.pop('data', None)

        outlier = db_mem.getOutlier(hashutils.gerarHash(json.dumps(body)), index)
        agora = dateutils.dataAtual()
        valor = loaddata.getValor(_dados, agora)
        if outlier != None:
            print('Processando outlier.... >>>><<<<< ' + json.dumps(body))
            db_mem.removerOutlier(hashutils.gerarHash(json.dumps(body)), index)
            body["metric"] = valor * 3
        else:
            body["metric"] = valor + randVal

        body["data"] = agora.strftime("%Y-%m-%dT%H:%M:%SZ")
        res = put_elastic.sendDataElastic(body, index)

        producer = KafkaProducer(value_serializer=lambda v: json.dumps(body).encode('utf-8'))
        producer.send('topic_test', body)

        print('Status do Elasticsearch -> ' + res['result'] + json.dumps(body))