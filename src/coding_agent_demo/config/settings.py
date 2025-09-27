import sys
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

# try to get a workspace path from the command line argument
cli_workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

# use .env file from workspace, otherwise try the current directory
env_file = ".env"
if cli_workspace and (cli_workspace / ".env").exists():
    env_file = str(cli_workspace / ".env")

class Settings(BaseSettings):
    """
    Using Pydantic's Base Settings: each field is a setting
    within the Config class, we define the settings to be loaded from a .env file
    """
    api_key: str | None = Field(None, env="API_KEY")
    api_base: str = Field("https://openrouter.ai/api/v1") # alternative https://api.openai.com/v1

    model_primary: str = "deepseek/deepseek-v3.1-terminus" #"qwen/qwen3-coder:free"
    model_merge: str   = "deepseek/deepseek-v3.1-terminus"

    workspace_root: Path = Field(cli_workspace)

    @field_validator('workspace_root')
    @classmethod
    def resolve_workspace_root(cls, v):
        # ensure workspace_root is an absolute path
        return v.resolve()

    class Config:
        env_file = env_file
        env_file_encoding = "utf-8"

settings = Settings()
