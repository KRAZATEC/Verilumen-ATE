"""
Schema definitions, contracts, and type specifications for ATE semiconductor datasets.
Dataset-agnostic: does not hard-code test names, lots, or specific distributions.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# Canonical Core Columns defined by the Assessment Specification
REQUIRED_COLUMNS: List[str] = [
    "Device_ID",
    "Test_ID",
    "Test_Name",
    "Lot_ID",
    "Wafer_ID",
    "VDD_V",
    "Temperature_C",
    "Measured_Value",
    "Lower_Limit",
    "Upper_Limit",
    "Result",
    "Failure_Mode",
    "Retest_Count",
]

# Legitimate aliases tolerated during ingestion
COLUMN_ALIASES: Dict[str, str] = {
    "device_id": "Device_ID",
    "device": "Device_ID",
    "dut_id": "Device_ID",
    "test_id": "Test_ID",
    "test_num": "Test_ID",
    "test_name": "Test_Name",
    "test": "Test_Name",
    "lot_id": "Lot_ID",
    "lot": "Lot_ID",
    "wafer_id": "Wafer_ID",
    "wafer": "Wafer_ID",
    "vdd_v": "VDD_V",
    "vdd": "VDD_V",
    "voltage": "VDD_V",
    "temperature_c": "Temperature_C",
    "temperature": "Temperature_C",
    "temp": "Temperature_C",
    "temp_c": "Temperature_C",
    "measured_value": "Measured_Value",
    "measured": "Measured_Value",
    "val": "Measured_Value",
    "value": "Measured_Value",
    "lower_limit": "Lower_Limit",
    "lolim": "Lower_Limit",
    "ll": "Lower_Limit",
    "upper_limit": "Upper_Limit",
    "hilim": "Upper_Limit",
    "ul": "Upper_Limit",
    "result": "Result",
    "pass_fail": "Result",
    "failure_mode": "Failure_Mode",
    "fail_mode": "Failure_Mode",
    "retest_count": "Retest_Count",
    "retest": "Retest_Count",
}

EXPECTED_NUMERIC_COLUMNS: List[str] = [
    "VDD_V",
    "Temperature_C",
    "Measured_Value",
    "Lower_Limit",
    "Upper_Limit",
    "Retest_Count",
]

EXPECTED_CATEGORICAL_COLUMNS: List[str] = [
    "Device_ID",
    "Test_ID",
    "Test_Name",
    "Lot_ID",
    "Wafer_ID",
    "Result",
    "Failure_Mode",
]


class ColumnProfile(BaseModel):
    name: str
    inferred_type: str
    non_null_count: int
    null_count: int
    null_percentage: float
    unique_count: int
    sample_values: List[Any] = Field(default_factory=list)


class SchemaValidationReport(BaseModel):
    is_valid: bool
    total_rows: int
    total_columns: int
    required_columns_present: List[str]
    missing_required_columns: List[str]
    unexpected_columns: List[str]
    column_profiles: Dict[str, ColumnProfile]
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)


class ATERecord(BaseModel):
    Device_ID: str
    Test_ID: str
    Test_Name: str
    Lot_ID: str
    Wafer_ID: str
    VDD_V: Optional[float] = None
    Temperature_C: Optional[float] = None
    Measured_Value: Optional[float] = None
    Lower_Limit: Optional[float] = None
    Upper_Limit: Optional[float] = None
    Result: Optional[str] = None
    Failure_Mode: Optional[str] = None
    Retest_Count: Optional[int] = None
