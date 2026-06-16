import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    # DeepSeek API
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_URL: str = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1")

    # Agent 配置
    AGENT_SLUG: str = os.getenv("AGENT_SLUG", "causal-chain-triz")
    CP_API_KEY: str = os.getenv("CP_API_KEY", "")
    CP_BASE_URL: str = os.getenv("CP_BASE_URL", "https://administrator.chmjk67.top")

    # 应用配置
    APP_PORT: int = int(os.getenv("APP_PORT", "3007"))
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    class Config:
        env_file = ".env"


settings = Settings()
