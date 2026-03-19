import pydantic_settings # pyright: ignore[reportMissingImports]


class OpenAIConfig(pydantic_settings.BaseSettings):
    api_key: str
    hostname: str = "localhost"
    port: int = 9804
    model: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

config = OpenAIConfig()