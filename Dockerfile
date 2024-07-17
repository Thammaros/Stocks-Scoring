FROM apache/airflow
USER root

ADD requirements.txt .
USER airflow
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt