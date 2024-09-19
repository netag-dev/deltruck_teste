# config.py

# import redis

from decouple import config


class Config(object):
    """Configurações comuns."""

    SWAGGER = {
        "title": "Deltruck API",
        "uiversion": 3,
        "description": "API documentation for Deltruck application",
        "version": "1.0.0",
    }

    CORS_ORIGINS = config("CORS_ORIGINS")

    SQLALCHEMY_DATABASE_SCHEMA = config("DATABASE_SCHEMA")
    SECRET_KEY = config("SECRET_KEY")
    PORT = config("PORT", default=5000, cast=int)

    BASE_API_URL = config("BASE_API_URL")
    CORS_ORIGINS = config("CORS_ORIGINS")

    JWT_ACCESS_TOKEN_EXPIRES = config("JWT_ACCESS_TOKEN_EXPIRES", default=900, cast=int)
    JWT_REFRESH_TOKEN_EXPIRES = config(
        "JWT_REFRESH_TOKEN_EXPIRES", default=86400, cast=int
    )
    # JWT_SECRET_KEY = config("JWT_SECRET_KEY")
    JWT_PRIVATE_KEY = config("JWT_PRIVATE_KEY")
    JWT_PUBLIC_KEY = config("JWT_PUBLIC_KEY")

    AUTH_CODE_EXPIRATION = config("AUTH_CODE_EXPIRATION", default=900, cast=int)

    # Configura Flask-Caching para usar Redis

    # CACHE_TYPE = "redis"
    # CACHE_DEFAULT_TIMEOUT = config("CACHE_DEFAULT_TIMEOUT", default=600, cast=int)
    # CACHE_TIMEOUT_DAYS = config("CACHE_TIMEOUT_DAYS", default=1, cast=int)
    # REDIS_CLIENT = redis.Redis(
    #     host=config("REDIS_HOST", default="localhost"),
    #    port=int(config("REDIS_PORT", default=6379)),
    #    db=int(config("REDIS_DB", default=0)),
    #    password=config("REDIS_PASSWORD", default=None),
    # )
    # CACHE_REDIS = REDIS_CLIENT

    # Configuração do  serviço de e-mail
    MAIL_SERVER = config("MAIL_SERVER", default="mail.netag.ao")
    MAIL_PORT = config("MAIL_PORT", default=465, cast=int)
    MAIL_USE_TLS = config("MAIL_USE_TLS", default=False, cast=bool)
    MAIL_USE_SSL = config("MAIL_USE_SSL", default=True, cast=bool)
    MAIL_USERNAME = config("MAIL_USERNAME", default="dev.sys@netag.ao")
    MAIL_PASSWORD = config("MAIL_PASSWORD", default="Angola2024#")
    MAIL_DEFAULT_SENDER = config("MAIL_DEFAULT_SENDER", default="dev.sys@netag.ao")


class DevConfig(Config):
    """Configurações de desenvolvimento local, para testes rápidos."""

    FLASK_ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URI_LOCAL_DEV")


class TestConfig(Config):
    """Configurações de teste local, para testes mais abragentes."""

    FLASK_ENV = "testing"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URI_LOCAL_TEST")


class StagingConfig(Config):
    """Configurações de staing , semelhante ao de produção(pré-produção)."""

    FLASK_ENV = "staging"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URI_REMOTE_STAGING")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    """Configurações de produção."""

    FLASK_ENV = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URI_REMOTE_PROD")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def get_config():
    env = config("FLASK_ENV", default="development")
    if env == "testing":
        return "config.TestConfig"
    elif env == "staging":
        return "config.StagingConfig"
    elif env == "production":
        return "config.ProdConfig"
    else:
        return "config.DevConfig"
