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

# ----------------------------
# ⭐ ADD YOUR UI CUSTOMIZATION
# ----------------------------

# Create styles & images directories
RUN mkdir -p /app/superset/static/assets/styles
RUN mkdir -p /app/superset/static/assets/images

# Copy custom CSS
COPY styles/custom.css /app/superset/static/assets/styles/custom.css

# Copy branding images
COPY images/logo.png /app/superset/static/assets/images/baap_logo.png
COPY images/favicon.png /app/superset/static/assets/images/baap_favicon.png

# Copy superset_config.py to correct PYTHONPATH
COPY superset_config.py /app/pythonpath/superset_config.py

# Fix permissions
RUN chown -R superset:superset /app/superset/static/assets \
    && chown -R superset:superset /app/pythonpath/superset_config.py

USER superset
