"""
Dataset Ingestion, normalization, and profiling.
Ensures raw uploaded data is strictly preserved and non-destructively profiled.
"""

import io
import uuid
from typing import Union, BinaryIO, Tuple
import pandas as pd
from backend.app.core.logging import logger
from backend.app.data.schema import (
    REQUIRED_COLUMNS,
    COLUMN_ALIASES,
    EXPECTED_NUMERIC_COLUMNS,
    ColumnProfile,
    SchemaValidationReport,
)


def load_csv(file_or_path: Union[str, BinaryIO, bytes]) -> pd.DataFrame:
    """Safely loads a CSV file into a pandas DataFrame without mutating the source."""
    try:
        if isinstance(file_or_path, bytes):
            stream = io.BytesIO(file_or_path)
            df = pd.read_csv(stream)
        elif hasattr(file_or_path, "read"):
            df = pd.read_csv(file_or_path)
        else:
            df = pd.read_csv(str(file_or_path))
        return df
    except Exception as e:
        logger.error(f"Failed to load CSV: {str(e)}")
        raise ValueError(f"Unable to parse CSV file: {str(e)}")


def normalize_column_names(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    """
    Normalizes known aliases without silent destruction.
    Returns (normalized_df, applied_renames_dict)
    """
    applied = {}
    rename_map = {}
    
    for col in df.columns:
        cleaned_col = str(col).strip()
        lower_cleaned = cleaned_col.lower()
        if lower_cleaned in COLUMN_ALIASES:
            canonical = COLUMN_ALIASES[lower_cleaned]
            if canonical != cleaned_col:
                rename_map[col] = canonical
                applied[col] = canonical
        elif cleaned_col != col:
            rename_map[col] = cleaned_col

    renamed_df = df.rename(columns=rename_map)
    return renamed_df, applied


def validate_schema(df: pd.DataFrame) -> SchemaValidationReport:
    """
    Validates DataFrame against the assessment canonical schema.
    Returns a comprehensive SchemaValidationReport.
    """
    total_rows, total_cols = df.shape
    cols = list(df.columns)
    
    missing_required = [c for c in REQUIRED_COLUMNS if c not in cols]
    required_present = [c for c in REQUIRED_COLUMNS if c in cols]
    unexpected = [c for c in cols if c not in REQUIRED_COLUMNS]
    
    warnings = []
    errors = []
    
    if total_rows == 0:
        errors.append("Dataset contains 0 rows.")
    
    if missing_required:
        errors.append(f"Missing required columns: {', '.join(missing_required)}")
        
    if unexpected:
        warnings.append(f"Additional columns present (will be tolerated): {', '.join(unexpected)}")
        
    column_profiles = {}
    for col in cols:
        series = df[col]
        non_null = int(series.notna().sum())
        null_count = int(series.isna().sum())
        null_pct = round((null_count / total_rows * 100), 2) if total_rows > 0 else 0.0
        unique_cnt = int(series.nunique(dropna=True))
        
        sample_vals = series.dropna().head(3).tolist()
        
        # Check type anomalies for numeric columns
        if col in EXPECTED_NUMERIC_COLUMNS and non_null > 0:
            if not pd.api.types.is_numeric_dtype(series):
                # Try to see if it's convertible
                converted = pd.to_numeric(series, errors='coerce')
                unparseable = int(converted.isna().sum() - null_count)
                if unparseable > 0:
                    warnings.append(f"Column '{col}' expected numeric but has {unparseable} unparseable values.")
        
        column_profiles[col] = ColumnProfile(
            name=col,
            inferred_type=str(series.dtype),
            non_null_count=non_null,
            null_count=null_count,
            null_percentage=null_pct,
            unique_count=unique_cnt,
            sample_values=sample_vals,
        )

    is_valid = len(errors) == 0

    return SchemaValidationReport(
        is_valid=is_valid,
        total_rows=total_rows,
        total_columns=total_cols,
        required_columns_present=required_present,
        missing_required_columns=missing_required,
        unexpected_columns=unexpected,
        column_profiles=column_profiles,
        warnings=warnings,
        errors=errors,
    )
