FROM python:3.7-slim-buster
# Install python packages
RUN pip install mlflow sklearn boto3 pymysql

RUN useradd -ms /bin/bash mlflow

ENV MLFLOW_HOME /opt/mlflow
ENV SERVER_PORT 5000
ENV SERVER_HOST 0.0.0.0
ENV FILE_STORE ${MLFLOW_HOME}/fileStore
ENV ARTIFACT_STORE ${MLFLOW_HOME}/artifactStore

RUN mkdir -p ${MLFLOW_HOME}/scripts && \
    mkdir -p ${FILE_STORE} && \
    mkdir -p ${ARTIFACT_STORE}

RUN chown -R mlflow:mlflow ${MLFLOW_HOME}

EXPOSE ${SERVER_PORT}/tcp

VOLUME ["${MLFLOW_HOME}/scripts/", "${FILE_STORE}", "${ARTIFACT_STORE}"]

WORKDIR ${MLFLOW_HOME}

USER root

ENTRYPOINT mlflow server --backend-store-uri mysql+pymysql://mlflow_db_user:mlflow_db_user@db:3306/mlflow_db --default-artifact-root ftp://ftp_user:pwd@!234@ftp_server:21/ftp/ftp_user --host ${SERVER_HOST} --port ${SERVER_PORT}