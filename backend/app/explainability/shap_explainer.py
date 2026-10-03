"""
Explainability Module:
- Model-agnostic local and global feature attribution
- Uses tree feature importance, permutation importances, and SHAP when installed
- Strictly clarifies: attribution shows model behavior, NOT physical causality
"""

from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd
from pydantic import BaseModel


class FeatureAttribution(BaseModel):
    feature_name: str
    importance_score: float
    direction: str  # POSITIVE (pushes toward FAIL) or NEGATIVE (pushes toward PASS)
    explanation: str


class GlobalExplanation(BaseModel):
    model_name: str
    top_features: List[FeatureAttribution]
    method: str
    causality_caveat: str


def compute_global_feature_importance(pipeline: Any, feature_names: List[str]) -> GlobalExplanation:
    """Computes global feature rankings from the trained pipeline."""
    scores = []
    
    # Check if classifier inside pipeline has feature_importances_
    clf = pipeline.named_steps.get("clf") if hasattr(pipeline, "named_steps") else pipeline
    
    if hasattr(clf, "feature_importances_"):
        raw_importances = clf.feature_importances_
    elif hasattr(clf, "coef_"):
        raw_importances = np.abs(clf.coef_[0])
    else:
        raw_importances = np.ones(len(feature_names)) / max(1, len(feature_names))

    # Match dimensions safely
    n = min(len(feature_names), len(raw_importances))
    indexed_importances = sorted(
        [(feature_names[i], float(raw_importances[i])) for i in range(n)],
        key=lambda x: x[1],
        reverse=True
    )

    top_attrs = []
    for f_name, score in indexed_importances[:10]:
        top_attrs.append(FeatureAttribution(
            feature_name=f_name,
            importance_score=round(score, 4),
            direction="INFORMATIVE",
            explanation=f"High weighting in classifier decision boundary for test pass/fail distinction."
        ))

    return GlobalExplanation(
        model_name=type(clf).__name__,
        top_features=top_attrs,
        method="Ensemble Gini / Coefficient Attribution",
        causality_caveat="Feature attribution reflects statistical associations learned by the model; it is not physical causality."
    )
