from stream import put_elastic
from stream import loaddata
from utils import dateutils, hashutils, numutils
from ml import PushModel
from datetime import datetime
import pandas as pd
import random
import threading
import json

class TaskHistorico(threading.Thread):

    def __init__(self, _dados, _json, _intervalo, _index, _historico_em_dias, _amplitude):
        threading.Thread.__init__(self)
        self._dados             = _dados
        self._json              = _json
        self._intervalo         = _intervalo
        self._index             = _index
        self._historico_em_dias = _historico_em_dias
        self._amplitude         = _amplitude
        self._key_model         = PushModel.key_model(self._json)
        self._key_entity        = hashutils.gerarHash(json.dumps(self._json))
        threading.Thread.name   = self._key_model
        print("Loading old data - " + str(self._json) + " - " + str(self._historico_em_dias))

    def run(self):

        randVal = numutils.calcRandom(self._amplitude)
        freqCalc = str(self._intervalo) + 'S'

        envio = ''
        count = 1

        metrics = []
        datas = []

        for new_date in pd.date_range(end=dateutils.dataAtual(), periods=(self._historico_em_dias*24*60), freq=freqCalc):
            valor = loaddata.getValor(self._dados, new_date)
            self._json["metric"] = valor + randVal
            self._json["data"] = new_date.strftime("%Y-%m-%dT%H:%M:%SZ")

            metrics.append(self._json["metric"])
            datas.append(self._json["data"])

            envio += '{ "index" : { "_index" : "' + self._index + '" } }\n'
            envio += json.dumps(self._json) + '\n'

            if count > 300:
                print("Envio do historico -> " + new_date.strftime("%Y-%m-%d"))
                put_elastic.sendBulkElastic(envio)
                randVal = numutils.calcRandom(self._amplitude)
                envio = ''
                count = 0

            count += 1

        put_elastic.sendBulkElastic(envio)

        print('Fim do processo de geracao do historico...')

        print('Envio do modelo para o ML Flow...')

        print("Chave do modelo - " + self._key_model + " - Key : " + self._key_entity)

        ds = pd.DataFrame(data={"ds":[datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ') for d in datas],
                                "y":metrics})

        PushModel.train_model(ds, self._key_model, self._key_entity)