import os

from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


class Config:
    """
    Base configuration for RailConnect.
    """

    APP_NAME = os.getenv("APP_NAME", "RailConnect")

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "False"
    ).lower() == "true"

    # Flask configuration
    TESTING = False

    # Frontend origins allowed to access the backend
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:5173"
    ).split(",")

    # Backend server configuration
    HOST = os.getenv(
        "HOST",
        "0.0.0.0"
    )

    PORT = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    # API configuration
    API_VERSION = os.getenv(
        "API_VERSION",
        "v1"
    )