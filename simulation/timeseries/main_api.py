from flask import Flask
from flask import request
from stream import jobScheduler
from stream import loaddata
from stream import historico
from stream import db_mem
from utils import hashutils
import json
import random

app = Flask(__name__)

@app.route('/')
def index():
    return "Job de envio de dados - Elastic!"


@app.route('/', methods=['POST'])
def incluirElemento():
    requisicao = request.get_json(force=True)

    intervalo = 60.0
    try:
        intervalo = float(requisicao['intervalo'])
    except:
        intervalo = 60.0

    amplitude = 10.0
    try:
        amplitude = float(requisicao['amplitude'])
    except:
        amplitude = 10.0

    dados = loaddata.getDados(amplitude=amplitude)

    index = None
    try:
        index = requisicao['index']
    except:
        # Indice nao informado
        index = 'dados'

    try:
        # Execução em paralelo - Envio para o elastic do historico
        thread = historico.TaskHistorico(dados, requisicao['chave'], intervalo, index,
                                         int(requisicao['historico_em_dias']))
        thread.start()
    except:
        # Nao sera processado historico
        pass

    jobScheduler.startEvent(dados, intervalo, requisicao['chave'], random.uniform(-10, 10), index)
    return "Job enviado para o Elasticsearch!"


@app.route('/', methods=['PUT'])
def gerarOutlier():
    requisicao = request.get_json(force=True)
    chave = json.dumps(requisicao['chave'])
    db_mem.gerarOutlier(hashutils.gerarHash(chave))
    return "Outlier registrado: " + chave


if __name__ == '__main__':
    db_mem.initDb()
    app.run(host="0.0.0.0", port=5001)
