# ---------------------------------------
# BASIC SUPERSET CONFIG
# ---------------------------------------

SECRET_KEY = "my_superset_secret"

SQLALCHEMY_DATABASE_URI = "sqlite:////app/superset_home/superset.db"

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

WTF_CSRF_ENABLED = True


# ---------------------------------------
# ENABLE IFRAME EMBEDDING (IMPORTANT)
# ---------------------------------------

# Allow other apps (FastAPI frontend) to embed Superset dashboards
HTTP_HEADERS = {
    "X-Frame-Options": "ALLOWALL",         # allow embedding
    "Access-Control-Allow-Origin": "*",     # or restrict to your domain
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
}

ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["*"],
    "origins": ["*"],       # or put your frontend domain here
}


# ---------------------------------------
# CLICKHOUSE CONNECT DRIVER CONFIG
# ---------------------------------------

CLICKHOUSE_URI = (
    "clickhousedb+connect://default:w3uqO75Wq_29r@"
    "zvx41wbk0r.asia-northeast1.gcp.clickhouse.cloud:8443/default"
    "?secure=true"
)

AVAILABLE_DRIVERS = {
    "clickhousedb+connect": ["clickhousedb+connect://"]
}


# ---------------------------------------
# CACHE PERFORMANCE
# ---------------------------------------

CACHE_CONFIG = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
}


# ---------------------------------------
# OPTIONAL: ALLOW DASHBOARD EMBED TOKENS
# ---------------------------------------
# (Useful if later you want secure embed without login)
# ---------------------------------------

FEATURE_FLAGS.update({
    "EMBEDDED_SUPERSET": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "THUMBNAILS": True,
})
