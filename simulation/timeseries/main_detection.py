'''
import json
import random
import faust

app = faust.App('myapp', broker='kafka://localhost:9092')

topic_test = app.topic('topic_test', key_type=str)

@app.agent(topic_test)
async def process_test(topic):
    async for row in topic:
        print(row)
'''

from stream import db_mem, alarm, put_elastic
from utils import hashutils
from kafka import KafkaConsumer
from json import loads
import warnings
import pandas as pd
import mlflow.pyfunc
import json

warnings.filterwarnings("ignore")

mlflow.set_tracking_uri("http://localhost:5000")

# Consumidor da fila
consumer = KafkaConsumer(
    'topic_test',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    message = message.value

    #Prophet não suporta timezone
    data = message.get('data').replace('Z','')
    #Valor recebido no kafka
    metric = message.get('metric')
    #A tabela que foi armazenada
    index = message.get('index')

    #Removendo atributos para gerar a chave
    message.pop('metric', None)
    message.pop('data', None)
    message.pop('index', None)

    model_uri = db_mem.getModel(hashutils.gerarHash(json.dumps(message)), index)

    print('Model: {}'.format(model_uri))

    try:
        model = mlflow.pyfunc.load_model(model_uri)

        serie = pd.DataFrame(data={"ds": [data]})
        out = model.predict(serie)

        valor_esperado = out["yhat"][0]
        limite_inferior = out["yhat_lower"][0]
        limite_superior = out["yhat_upper"][0]

        if(metric < limite_inferior):
            envio = alarm.generateAlarm(metric, valor_esperado, limite_inferior, data, message)
            put_elastic.sendBulkElastic(envio)
            print('Anomolia gerada: {}'.format(envio))

        if(metric > limite_superior):
            envio = alarm.generateAlarm(metric, valor_esperado, limite_superior, data, message)
            put_elastic.sendBulkElastic(envio)
            print('Anomolia gerada: {}'.format(envio))
    except:
        print("Erro na carga do modelo")
