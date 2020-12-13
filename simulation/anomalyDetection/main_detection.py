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

from kafka import KafkaConsumer
from json import loads
import sqlite3

def getOutlier(hash_chave, index):
    c = sqlite3.connect('../outlier.db')
    # Insert a row of data
    tuplaDados = c.execute("SELECT hash_chave FROM outlier WHERE hash_chave = ? and ind = ?", [hash_chave, index]).fetchone()
    if tuplaDados == None:
        return None
    else:
        return tuplaDados[0]
    c.close()

import json
import hashlib

def gerarHash(jsonstr):
    h = hashlib.new('ripemd160')
    h.update(jsonstr.encode())
    return h.hexdigest()

consumer = KafkaConsumer(
    'topic_test',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group-2',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    message = message.value
    key = message

    key.pop('metric', None)
    key.pop('data', None)
    key = gerarHash(key)

    #a4cea65946fc4adf8cbfc223ef9db371

    print('Body: {}'.format(key))