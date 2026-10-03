from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List, Union


class Settings(BaseSettings):
    PROJECT_NAME: str = "Verilumen ATE Intelligence Platform"
    API_V1_STR: str = "/api"
    DEBUG: Union[bool, str] = False
    
    # Base paths (config.py is in backend/app/core -> 3 parents up is root)
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "models"
    REPORTS_DIR: Path = BASE_DIR / "reports"
    
    # Upload limits
    MAX_UPLOAD_SIZE_MB: int = 100
    
    # Anomaly settings
    DEFAULT_CONTAMINATION: float = 0.05
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
