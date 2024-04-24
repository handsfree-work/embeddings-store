import os
from pydantic_settings import BaseSettings, SettingsConfigDict

env = os.getenv("ENVIRONMENT", "dev")
env = env.lower()
env_files = ('.env', f'.env.{env}')


class BasicSettings(BaseSettings, case_sensitive=True):
    model_config = SettingsConfigDict(env_file=env_files, env_file_encoding='utf-8', extra="allow", env_prefix='basic_')

    environment: str = "dev"
    title: str = "embeddings store service"
    version: str = "0.1.0"
    timezone: str = "UTC"
    description: str | None = None
    debug: bool = False

    server_host: str = ""  # type: ignore
    server_port: int = 8006  # type: ignore
    server_workers: int = 4
    api_prefix: str = "/api"
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    openapi_prefix: str = ""

    db_postgres_db: str = ""
    db_postgres_host: str = ""
    db_max_pool_con: int | None = None
    db_postgres_username: str = ""
    db_postgres_password: str = ""
    db_pool_size: int | None = None
    db_pool_overflow: int | None = None
    db_postgres_port: int | None = None
    db_postgres_schema: str = ""
    db_timeout: int | None = None
    db_postgres_uri: str = ""
    db_migrations_dir: str = "src/repository/migrations"

    is_db_echo_log: bool = True
    is_db_force_rollback: bool = False
    is_db_expire_on_commit: bool = False

    jwt_token_prefix: str = ""
    jwt_secret_key: str = ""
    jwt_subject: str = ""
    jwt_min: int = 60
    jwt_access_token_expiration_time: int = 60 * 24 * 30 * 60

    is_allowed_credentials: bool = True
    allowed_origins: list[str] = [
        # "http://localhost:3000",  # react default port
        # "http://0.0.0.0:3000",
        # "http://127.0.0.1:3000",  # react docker port
        # "http://127.0.0.1:3001",
        # "http://localhost:5173",  # qwik default port
        # "http://0.0.0.0:5173",
        # "http://127.0.0.1:5173",  # qwik docker port
        # "http://127.0.0.1:5174",
        "*"
    ]
    allowed_methods: list[str] = ["*"]
    allowed_headers: list[str] = ["*"]

    logging_level: int = 20
    loggers: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    hashing_algorithm_layer_1: str = ""
    hashing_algorithm_layer_2: str = ""
    hashing_salt: str = ""
    jwt_algorithm: str = ""

    codecov_token: str = ""

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom values defined in `BackendBaseSettings`.
        """
        return {
            "title": self.title,
            "version": self.version,
            "debug": self.debug,
            "description": self.description,
            "docs_url": self.docs_url,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "openapi_prefix": self.openapi_prefix,
            "api_prefix": self.api_prefix,
        }


class OpenAiSettings(BaseSettings, case_sensitive=False):
    model_config = SettingsConfigDict(env_file=env_files, env_file_encoding='utf-8',extra="allow",  env_prefix='openai_')

    api_key: str = ""
    api_base: str = ""
    api_version: str = ""
    api_type: str = "azure"
    api_engine: str = "gpt-35-turbo-0613"
    proxy: str | None = None


class VectorStoreSettings(BaseSettings, case_sensitive=False):
    model_config = SettingsConfigDict(env_file=env_files, env_file_encoding='utf-8',extra="allow", env_prefix='vs_')

    type: str = "pgvector"
    pg_uri: str = "postgresql+psycopg://localhost/pgvector_example"
    pg_migrations_dir: str = ""


class EmbeddingSettings(BaseSettings, case_sensitive=False):
    model_config = SettingsConfigDict(env_file=env_files, env_file_encoding='utf-8', extra="allow", env_prefix='embedding_')

    provider: str = "openai"  # openai or  local


class LocalAiSettings(BaseSettings, case_sensitive=False):
    model_config = SettingsConfigDict(env_file=env_files, env_file_encoding='utf-8', extra="allow", env_prefix='local_ai_')

    embedding_url: str = "http://127.0.0.1:9901/api/embedding"


class Settings:
    openai = OpenAiSettings()
    embedding = EmbeddingSettings()
    localAi = LocalAiSettings()
    vector_store = VectorStoreSettings()
    base = BasicSettings()


settings = Settings()
base_settings = settings.base
