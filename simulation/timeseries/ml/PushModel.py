import warnings
import sys

import pandas as pd
import numpy as np

import mlflow
import mlflow.pyfunc

import fbprophet
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics

from stream import db_mem

mlflow.set_tracking_uri("http://localhost:5000")

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

class FbProphetWrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, model):
        self.model = model
        super().__init__()

    def load_context(self, context):
        from fbprophet import Prophet
        return

    def predict(self, context, model_input):
        return self.model.predict(model_input)

def key_model(data):
    ret = 'model'
    for key, value in data.items():
        ret = ret + '_' + key + '_' + value

    return ret

def train_model(df, _name, _entity):
        warnings.filterwarnings("ignore")
        np.random.seed(40)

        # Useful for multiple runs (only doing one run in this sample notebook)
        with mlflow.start_run():
            m = Prophet()
            m.fit(df)

            # Evaluate Metrics
            print("Executando a validação cruzada...")
            df_cv = cross_validation(m, initial='10 days', horizon="4 days", period="2 days")
            print("Processando a performance do dados...")
            df_p = performance_metrics(df_cv)

            # Print out metrics
            print("Prophet model :")
            print("  CV: \n%s" % df_cv.head())
            print("  Perf: \n%s" % df_p.head())

            # Log parameter, metrics, and model to MLflow
            df_p_mean = df_p.groupby(pd.Grouper(key='horizon', freq='D')).mean()
            for index, row in df_p_mean.iterrows():
                mlflow.log_metric("rmse", row.rmse)
                mlflow.log_metric("mape", row.mape)
                mlflow.log_metric("mse", row.mse)
                mlflow.log_metric("mae", row.mae)

            mlflow.pyfunc.log_model(_name, python_model=FbProphetWrapper(m))

            model_uri = "runs:/{run_id}/{key}".format(run_id=mlflow.active_run().info.run_id, key=_name)

            print("Logged model with URI: {uri}".format(uri=model_uri))

            db_mem.gerarModel(_entity, model_uri)
