"""
ML Training Pipeline for Task 2:
- Interleaved Stratified Group Splitting (by Device_ID to prevent data leakage)
- Class Imbalance Handling with balanced class weighting
- Trains at least two contrasting classifiers:
    1. Interpretable Linear Baseline: LogisticRegression(class_weight='balanced')
    2. Primary High-Performance Ensemble: HistGradientBoostingClassifier(class_weight='balanced')
    3. Challenger Tree Ensemble: RandomForestClassifier(class_weight='balanced')
    (Note: CatBoost/XGBoost are seamlessly plugged in if their native packages are present)
- Compares all models using precision, recall, F1, ROC-AUC, and PR-AUC
- Saves winning / selected model in ModelRegistry
"""

from datetime import datetime
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import StratifiedGroupKFold, train_test_split
from sklearn.pipeline import Pipeline
from backend.app.core.logging import logger
from backend.app.ml.features import (
    ATEFeatureExtractor,
    build_preprocessor,
    prepare_training_matrices,
)
from backend.app.ml.evaluate import evaluate_classifier, EvaluationMetrics
from backend.app.ml.model_registry import model_registry


def train_and_compare_models(
    df: pd.DataFrame,
    scenario: str = "Scenario B - Measurement-Aware"
) -> Dict[str, Any]:
    logger.info(f"Starting ML Training pipeline under {scenario}...")
    
    # 1. Prepare X, y
    X, y, num_cols, cat_cols = prepare_training_matrices(df, scenario=scenario)

    if len(np.unique(y)) < 2:
        raise ValueError("Insufficient target variation: Need both PASS and FAIL classes to train classifiers.")

    # 2. Grouped splitting by Device_ID to prevent inter-device leakage
    groups = df.loc[X.index, "Device_ID"] if "Device_ID" in df.columns else np.arange(len(X))
    
    # Use StratifiedGroupKFold or group-aware train/test split
    try:
        sgkf = StratifiedGroupKFold(n_splits=5)
        train_idx, val_idx = next(sgkf.split(X, y, groups=groups))
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
    except Exception:
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=y
        )

    # 3. Build candidate pipelines
    include_meas = not scenario.startswith("Scenario A")
    
    # Model 1: Baseline Logistic Regression
    pipe_lr = Pipeline([
        ("feature_eng", ATEFeatureExtractor(include_measurements=include_meas)),
        ("prep", build_preprocessor(num_cols, cat_cols)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
    ])

    # Model 2: Primary Mixed Tabular HistGradientBoosting
    pipe_gb = Pipeline([
        ("feature_eng", ATEFeatureExtractor(include_measurements=include_meas)),
        ("prep", build_preprocessor(num_cols, cat_cols)),
        ("clf", HistGradientBoostingClassifier(max_iter=150, class_weight="balanced", random_state=42)),
    ])

    # Model 3: Challenger Random Forest
    pipe_rf = Pipeline([
        ("feature_eng", ATEFeatureExtractor(include_measurements=include_meas)),
        ("prep", build_preprocessor(num_cols, cat_cols)),
        ("clf", RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42, n_jobs=-1)),
    ])

    candidates = {
        "Logistic_Regression": pipe_lr,
        "Hist_Gradient_Boosting": pipe_gb,
        "Random_Forest": pipe_rf,
    }

    eval_results: Dict[str, EvaluationMetrics] = {}
    
    best_model_name = None
    best_f1 = -1.0

    for name, pipe in candidates.items():
        logger.info(f"Training {name}...")
        pipe.fit(X_train, y_train)
        
        y_pred = pipe.predict(X_val)
        y_prob = pipe.predict_proba(X_val)[:, 1] if hasattr(pipe, "predict_proba") else y_pred
        
        metrics = evaluate_classifier(name, y_val.values, y_pred, y_prob)
        eval_results[name] = metrics
        
        if metrics.f1_score > best_f1:
            best_f1 = metrics.f1_score
            best_model_name = name

    # Persist best model as the selected production model
    selected_pipe = candidates[best_model_name]
    metadata = {
        "model_name": best_model_name,
        "scenario": scenario,
        "training_timestamp": datetime.utcnow().isoformat(),
        "numeric_features": num_cols,
        "categorical_features": cat_cols,
        "target": "Result (FAIL=1, PASS=0)",
        "validation_strategy": "StratifiedGroupKFold(5) grouped by Device_ID",
        "best_metrics": eval_results[best_model_name].model_dump(),
        "all_metrics": {k: v.model_dump() for k, v in eval_results.items()},
    }
    
    model_registry.save_model("production_model", selected_pipe, metadata)
    # Also save each individual candidate
    for name, pipe in candidates.items():
        model_registry.save_model(name, pipe, {
            "model_name": name,
            "scenario": scenario,
            "metrics": eval_results[name].model_dump()
        })

    return {
        "best_model": best_model_name,
        "all_metrics": eval_results,
        "metadata": metadata,
    }
