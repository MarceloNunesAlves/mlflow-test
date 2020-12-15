#Simulação de detecção de anomalia com o prophet

##Configuração

Para executar o simulador é necessario instalar os pre-requisitos.

```
pip install -r requirements.txt
```

Suba a stack de apoio

```
docker-compose up -d --build
```

Para subir a aplicação (Porta: 5001)

```
python main_api.py
```

Para subir a detecção de anomalia

```
python main_detection.py
```

##Exemplos de chamada da API

Inclusão de dados e agendamento do JOB

Metodo: POST

```
{
	"historico_em_dias": "15",
	"intervalo": "60",
	"index": "serie",
	"amplitude": 30,
	"chave":
	{
		"campo_1": "Valor X",
		"campo_2": "Valor Y"
	}
}
```

Inclusão de anomalia

Metodo: PUT

```
{
	"index": "serie",
	"indice_aplicado": 1.5,
	"chave":
	{
		"campo_1": "Valor X",
		"campo_2": "Valor Y"
	}
}
```

Verificar threads em execução

Metodo: GET

```
{}
```