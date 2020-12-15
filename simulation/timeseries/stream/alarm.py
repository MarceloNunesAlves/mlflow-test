import json

def generateAlarm(_valor_atual, _esperado, _margem, _data):
    envio = '{ "index" : { "_index" : "alarm" } }\n'
    envio += json.dumps({"description": "Anomalia detectada, valor esperado: {esperado:.4f} - valor recebido: {valor_atual:.4f} - o valor ultrapassou a margem de {margem:.4f}".format(esperado=_esperado, valor_atual=_valor_atual, margem=_margem),
                         "valor_atual": _valor_atual,
                         "esperado": _esperado,
                         "margem": _margem,
                         "data": _data}) + '\n'
    return envio
