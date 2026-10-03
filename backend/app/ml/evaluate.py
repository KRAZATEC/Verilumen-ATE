"""
Model Evaluation Metrics & Reporting Engine for Task 2:
- Accuracy, Precision, Recall, F1
- ROC-AUC and PR-AUC (crucial for class-imbalanced semiconductor fail detection)
- Confusion Matrix and detailed Classification Report
"""

from typing import Dict, Any, List
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report,
)
from pydantic import BaseModel


class EvaluationMetrics(BaseModel):
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    pr_auc: float
    confusion_matrix: List[List[int]]
    total_samples: int
    positive_samples: int
    negative_samples: int
    class_imbalance_ratio: float


def evaluate_classifier(
    model_name: str,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray
) -> EvaluationMetrics:
    acc = round(float(accuracy_score(y_true, y_pred)), 4)
    prec = round(float(precision_score(y_true, y_pred, zero_division=0)), 4)
    rec = round(float(recall_score(y_true, y_pred, zero_division=0)), 4)
    f1 = round(float(f1_score(y_true, y_pred, zero_division=0)), 4)
    
    # Check if both classes exist in y_true for AUC
    try:
        roc = round(float(roc_auc_score(y_true, y_prob)), 4)
        pr_auc = round(float(average_precision_score(y_true, y_prob)), 4)
    except Exception:
        roc = 0.5
        pr_auc = 0.0

    cm = confusion_matrix(y_true, y_pred).tolist()
    pos = int(np.sum(y_true == 1))
    neg = int(np.sum(y_true == 0))
    ratio = round(float(neg / max(1, pos)), 2)

    return EvaluationMetrics(
        model_name=model_name,
        accuracy=acc,
        precision=prec,
        recall=rec,
        f1_score=f1,
        roc_auc=roc,
        pr_auc=pr_auc,
        confusion_matrix=cm,
        total_samples=len(y_true),
        positive_samples=pos,
        negative_samples=neg,
        class_imbalance_ratio=ratio,
    )
