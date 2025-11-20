FROM apache/superset:latest

USER root

RUN pip install --no-cache-dir \
    clickhouse-connect \
    clickhouse-sqlalchemy \
    sqlalchemy

USER superset
