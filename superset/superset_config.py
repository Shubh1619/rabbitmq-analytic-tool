SECRET_KEY = "my_superset_secret"

SQLALCHEMY_DATABASE_URI = "sqlite:////app/superset_home/superset.db"

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
    "EMBEDDED_SUPERSET": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "THUMBNAILS": True,
}

WTF_CSRF_ENABLED = False

HTTP_HEADERS = {
    "X-Frame-Options": "ALLOWALL",
    "Content-Security-Policy": "frame-ancestors *;",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "*",
}

ENABLE_CORS = True
CORS_OPTIONS = {"supports_credentials": True, "allow_headers": ["*"], "origins": ["*"]}

CLICKHOUSE_URI = "clickhousedb+connect://default:@clickhouse:8123/default"

AVAILABLE_DRIVERS = {"clickhousedb+connect": ["clickhousedb+connect://"]}

CACHE_CONFIG = {"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300}

PUBLIC_ROLE_LIKE = "Public"
AUTH_ROLE_PUBLIC = "Public"

ENABLE_PROXY_FIX = True
ENABLE_CORS = True

# --------------------------------------------------
# Custom UI configuration
# --------------------------------------------------
APP_NAME = "Baap Analytics"

APP_ICON = "/static/assets/images/baap_logo.png"
APP_ICON_WIDTH = 200

FAVICONS = [{"href": "/static/assets/images/baap_favicon.png"}]

# Correct way to load custom CSS in Superset 2.x+
CUSTOM_CSS = "/static/assets/styles/custom.css"

