"""
Application configuration for the RFM Analysis backend.

Settings
--------
DATASET_PATH : str
    Path to the CSV dataset file (absolute or relative to the working directory).
    Defaults to "data/online_retail.csv".
    Override by setting the DATASET_PATH environment variable before starting the server.

CORS_ORIGINS : list[str]
    List of allowed CORS origins for the FastAPI CORSMiddleware.
    Defaults to ["*"] (allow all origins — suitable for local development).
    Override by setting the CORS_ORIGINS environment variable as a comma-separated
    list of origins, e.g. "http://localhost:3000,http://127.0.0.1:5500".
"""

import os

# ---------------------------------------------------------------------------
# DATASET_PATH
# The location of the CSV file that the backend will load on startup.
# Falls back to the bundled sample dataset when no env var is set.
# ---------------------------------------------------------------------------
DATASET_PATH: str = os.getenv("DATASET_PATH", "data/online_retail.csv")

# ---------------------------------------------------------------------------
# CORS_ORIGINS
# Controls which browser origins are permitted to call the API.
# The env var is parsed as a comma-separated string so it can be set easily
# in shell environments without JSON quoting issues.
# Example: CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:5500"
# ---------------------------------------------------------------------------
_cors_env: str = os.getenv("CORS_ORIGINS", "")
CORS_ORIGINS: list[str] = (
    [origin.strip() for origin in _cors_env.split(",") if origin.strip()]
    if _cors_env
    else ["*"]  # default: allow all origins (fine for local dev / evaluation)
)
