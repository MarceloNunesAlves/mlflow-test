import json
from utils import hashutils

def generateAlarm(_valor_atual, _esperado, _margem, _data, _message):
    envio = '{ "index" : { "_index" : "alarm" } }\n'

    json_alarm = {"description": "Anomalia detectada, valor esperado: {esperado:.4f} - valor recebido: {valor_atual:.4f} - o valor ultrapassou a margem de {margem:.4f} - {what_anomaly}".format(esperado=_esperado, valor_atual=_valor_atual, margem=_margem, what_anomaly=hashutils.what_anomaly(_message)),
                    "valor_atual": _valor_atual,
                    "esperado": _esperado,
                    "margem": _margem,
                    "data": _data}

    for key, value in _message.items():
        json_alarm[key] = value

    envio += json.dumps(json_alarm) + '\n'
    return envio
