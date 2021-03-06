# Ambiente de teste - ML Flow

Este repositório apresenta uma forma simplificada de como subir o ambiente em uma máquina local e testar o processo de MLOps completo.

## Subir o ambiente

Para subir o ambiente basta ter o Docker 19.03.

```
docker-compose up -d --build
```

## Executar o modelo no ML Flow

Para este teste simples é importante que o ambiente do python possua todos os pacotes necessários.

Para criar um ambiente python com os pacotes necessários.

Criar o ambiente no Anaconda
```
conda create -n mlflow_env
conda activate mlflow_env
```

Instalar os pacotes
```
conda install python
pip install mlflow
pip install sklearn
```

Configuração da variável do ambiente para ser usado na execução do script e na geração do REST.

```
export MLFLOW_TRACKING_URI=http://localhost:5000
```

Publicação do modelo no ML Flow.

```
python examples/sklearn_logistic_regression/train.py
```

Para visualizar o desempenho do modelo acesse a URL: http://localhost:5000/.

## Criar e testar o serviço REST do modelo publicado

Gerar um microserviço do modelo.

```
mlflow models serve -m runs:/<ID_GERADO>/model --port 1234
```

Testando o serviço do modelo.

```
curl -d '{"columns":["x"], "data":[[1], [-1]]}' -H 'Content-Type: application/json; format=pandas-split' -X POST localhost:1234/invocations
```