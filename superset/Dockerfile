FROM apache/superset:latest

USER root

# Install system packages (optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
    coreutils python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip inside Superset venv
RUN /app/.venv/bin/python -m ensurepip --upgrade || true
RUN /app/.venv/bin/python -m pip install --upgrade pip

# Install required Python packages INSIDE Superset venv
RUN /app/.venv/bin/python -m pip install flask-cors
RUN /app/.venv/bin/python -m pip install "sqlalchemy==1.4.48"
RUN /app/.venv/bin/python -m pip install clickhouse-connect clickhouse-sqlalchemy==0.2.1

USER superset
