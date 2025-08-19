"""应用配置模块"""

import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用设置类"""

    # 应用基本配置
    app_name: str = "FastAPI 服务模板"
    app_version: str = "1.0.0"
    debug: bool = False

    # 服务器配置
    port: int = 8000
    host: str = "127.0.0.1"
    reload: bool = True

    # JWT配置
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    # 数据库配置
    database_url: Optional[str] = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://fastapi_user:fastapi_password@localhost:5432/fastapi_db",
    )

    # 数据库连接池配置
    db_pool_size: int = int(os.getenv("DB_POOL_SIZE", "10"))
    db_max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    db_pool_timeout: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))

    # 数据库测试配置
    test_database_url: Optional[str] = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql+asyncpg://fastapi_user:fastapi_password@localhost:5432/fastapi_test_db",
    )

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, extra="ignore"  # 忽略额外的环境变量
    )


# 创建全局设置实例
settings = Settings()
