from stream import put_elastic
from stream import loaddata
from utils import dateutils
import pandas as pd
import random
import threading
import json

class TaskHistorico(threading.Thread):

    def __init__(self, _dados, _json, _intervalo, _index, _historico_em_dias):
        threading.Thread.__init__(self)
        self._dados             = _dados
        self._json              = _json
        self._intervalo         = _intervalo
        self._index             = _index
        self._historico_em_dias = _historico_em_dias
        print("Loading old data - " + str(self._json) + " - " + str(self._historico_em_dias))

    def run(self):

        randVal = random.uniform(-10, 30)
        freqCalc = str(self._intervalo) + 'S'

        envio = ''
        count = 1
        for new_date in pd.date_range(end=dateutils.dataAtual(), periods=(self._historico_em_dias*24*60), freq=freqCalc):
            valor = loaddata.getValor(self._dados, new_date)
            self._json["metric"] = valor + randVal
            self._json["data"] = new_date.strftime("%Y-%m-%dT%H:%M:%SZ")

            envio += '{ "index" : { "_index" : "' + self._index + '" } }\n'
            envio += json.dumps(self._json) + '\n'

            if count > 500:
                print("Envio do historico -> " + new_date.strftime("%Y-%m-%d"))
                put_elastic.sendBulkElastic(envio)
                randVal = random.uniform(-10, 50)
                envio = ''
                count = 0

            count += 1

        put_elastic.sendBulkElastic(envio)

        print('Fim do processo de geracao do historico...')