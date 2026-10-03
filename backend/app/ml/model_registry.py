"""
Model Registry & Artifact Persistence:
- Handles saving and loading complete pipelines (preprocessing + classifier)
- Stores metadata: model name, version, training timestamp, features, target, metrics
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import joblib
from backend.app.core.config import settings
from backend.app.core.logging import logger


class ModelRegistry:
    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or settings.MODELS_DIR
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_model(
        self,
        model_name: str,
        pipeline: Any,
        metadata: Dict[str, Any]
    ) -> Path:
        model_path = self.storage_dir / f"{model_name}.joblib"
        meta_path = self.storage_dir / f"{model_name}_metadata.json"

        joblib.dump(pipeline, model_path)
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Saved model pipeline to {model_path} with metadata {meta_path}")
        return model_path

    def load_model(self, model_name: str) -> Optional[Any]:
        model_path = self.storage_dir / f"{model_name}.joblib"
        if not model_path.exists():
            logger.warning(f"Model file not found: {model_path}")
            return None
        return joblib.load(model_path)

    def load_metadata(self, model_name: str) -> Optional[Dict[str, Any]]:
        meta_path = self.storage_dir / f"{model_name}_metadata.json"
        if not meta_path.exists():
            return None
        with open(meta_path, "r") as f:
            return json.load(f)

    def list_models(self) -> Dict[str, Any]:
        models = {}
        for meta_file in self.storage_dir.glob("*_metadata.json"):
            name = meta_file.stem.replace("_metadata", "")
            with open(meta_file, "r") as f:
                models[name] = json.load(f)
        return models


model_registry = ModelRegistry()
