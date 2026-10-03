"""
Preprocessing & Cleaning pipeline.
Ensures:
- Raw dataframe is never mutated
- Clean layer is created with clear audit tracking
- Explicit handling of duplicates and missing values
"""

from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
from backend.app.core.logging import logger
from backend.app.data.schema import EXPECTED_NUMERIC_COLUMNS, EXPECTED_CATEGORICAL_COLUMNS


def clean_dataset(raw_df: pd.DataFrame, drop_exact_duplicates: bool = True) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Cleans raw DataFrame into a production-ready cleaned DataFrame without mutating raw_df.
    Returns: (cleaned_df, cleaning_audit_log)
    """
    cleaned = raw_df.copy()
    initial_rows = len(cleaned)
    audit = {
        "initial_rows": initial_rows,
        "duplicates_removed": 0,
        "missing_imputations": {},
        "type_conversions": {},
    }

    # 1. Duplicates
    if drop_exact_duplicates:
        dups = int(cleaned.duplicated().sum())
        if dups > 0:
            cleaned = cleaned.drop_duplicates(keep="first").reset_index(drop=True)
            audit["duplicates_removed"] = dups
            logger.info(f"Deduplicated dataset: removed {dups} exact duplicate records.")

    # 2. Type conversions for expected numerics
    for col in EXPECTED_NUMERIC_COLUMNS:
        if col in cleaned.columns:
            if not pd.api.types.is_numeric_dtype(cleaned[col]):
                cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")
                audit["type_conversions"][col] = "Converted to numeric float"

    # 3. Missing Value Imputation
    for col in cleaned.columns:
        null_cnt = int(cleaned[col].isna().sum())
        if null_cnt > 0:
            if pd.api.types.is_numeric_dtype(cleaned[col]):
                med = float(cleaned[col].median()) if null_cnt < len(cleaned) else 0.0
                cleaned[col] = cleaned[col].fillna(med)
                audit["missing_imputations"][col] = {
                    "count": null_cnt,
                    "strategy": "median",
                    "imputed_val": round(med, 4),
                }
            else:
                # For categorical, Result must NEVER be imputed randomly
                if col == "Result":
                    # If Result is missing, label as UNKNOWN
                    cleaned[col] = cleaned[col].fillna("UNKNOWN")
                    audit["missing_imputations"][col] = {"count": null_cnt, "strategy": "explicit_UNKNOWN"}
                elif col == "Failure_Mode":
                    cleaned[col] = cleaned[col].fillna("NONE")
                    audit["missing_imputations"][col] = {"count": null_cnt, "strategy": "explicit_NONE"}
                else:
                    mode_val = cleaned[col].mode()
                    val = str(mode_val[0]) if not mode_val.empty else "UNKNOWN"
                    cleaned[col] = cleaned[col].fillna(val)
                    audit["missing_imputations"][col] = {"count": null_cnt, "strategy": "mode", "imputed_val": val}

    audit["final_rows"] = len(cleaned)
    return cleaned, audit
