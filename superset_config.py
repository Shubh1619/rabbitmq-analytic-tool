# ---------------------------------------
# BASIC SUPERSET CONFIG
# ---------------------------------------

SECRET_KEY = "my_superset_secret"

# Main Superset DB
SQLALCHEMY_DATABASE_URI = "sqlite:////app/superset_home/superset.db"

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

WTF_CSRF_ENABLED = True


# ---------------------------------------
# CLICKHOUSE CONNECT DRIVER (MODERN)
# ---------------------------------------
# Superset recognizes clickhouse-connect only via this name:
#   clickhousedb+connect://
# ---------------------------------------

# EXAMPLE CONNECTION URI (You paste this inside Superset UI)
CLICKHOUSE_URI = (
    "clickhousedb+connect://default:w3uqO75Wq_29r@"
    "zvx41wbk0r.asia-northeast1.gcp.clickhouse.cloud:8443/default"
    "?secure=true"
)


# Optional: Make Superset auto-detect this driver
AVAILABLE_DRIVERS = {
    "clickhousedb+connect": ["clickhousedb+connect://"]
}


# Increase metadata cache performance for large ClickHouse tables
CACHE_CONFIG = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
}
