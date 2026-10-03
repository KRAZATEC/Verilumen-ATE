"""
Verilumen ATE Intelligence Platform - High-Fidelity Synthetic ATE Dataset Generator
Generates realistic semiconductor automated test equipment data with:
- Multiple lots, wafers, devices, and 12 distinct test types
- Electrical & thermal conditions (VDD_V, Temperature_C)
- Measurement distributions, spec limits, and realistic PASS/FAIL margins
- Controlled data quality artifacts: exact duplicates, missing values, extreme statistical outliers
- Diverse failure modes: TIMING_VIOLATION, VOLTAGE_MARGIN, THERMAL_STRESS, SIGNAL_INTEGRITY, SCAN_CHAIN, POWER_ANOMALY
- Multi-lot and wafer spatial variations
- Retest count tracking
"""

import argparse
import random
import numpy as np
import pandas as pd
from pathlib import Path


TEST_DEFINITIONS = [
    {
        "test_id": "T101_LEAKAGE",
        "test_name": "Standby Leakage Current",
        "unit": "uA",
        "nominal_vdd": 1.2,
        "nominal_temp": 25.0,
        "lower_limit": 0.05,
        "upper_limit": 5.00,
        "base_mean": 1.8,
        "base_std": 0.6,
        "failure_mode": "POWER_ANOMALY",
        "temp_coef": 0.04,  # leakage increases with temp
        "vdd_coef": 0.8,
    },
    {
        "test_id": "T102_IDD_ACTIVE",
        "test_name": "Active Core Current",
        "unit": "mA",
        "nominal_vdd": 1.2,
        "nominal_temp": 25.0,
        "lower_limit": 40.0,
        "upper_limit": 120.0,
        "base_mean": 75.0,
        "base_std": 10.0,
        "failure_mode": "POWER_ANOMALY",
        "temp_coef": 0.15,
        "vdd_coef": 25.0,
    },
    {
        "test_id": "T201_VOLTAGE_REF",
        "test_name": "Internal Bandgap Reference",
        "unit": "V",
        "nominal_vdd": 1.2,
        "nominal_temp": 25.0,
        "lower_limit": 1.14,
        "upper_limit": 1.26,
        "base_mean": 1.201,
        "base_std": 0.015,
        "failure_mode": "VOLTAGE_MARGIN",
        "temp_coef": -0.0001,
        "vdd_coef": 0.01,
    },
    {
        "test_id": "T202_LDO_OUTPUT",
        "test_name": "Low-Dropout Regulator Output",
        "unit": "V",
        "nominal_vdd": 1.8,
        "nominal_temp": 25.0,
        "lower_limit": 1.71,
        "upper_limit": 1.89,
        "base_mean": 1.802,
        "base_std": 0.025,
        "failure_mode": "VOLTAGE_MARGIN",
        "temp_coef": -0.0002,
        "vdd_coef": 0.02,
    },
    {
        "test_id": "T301_PLL_FREQ",
        "test_name": "Phase-Locked Loop Lock Frequency",
        "unit": "MHz",
        "nominal_vdd": 1.2,
        "nominal_temp": 25.0,
        "lower_limit": 980.0,
        "upper_limit": 1020.0,
        "base_mean": 1000.2,
        "base_std": 4.5,
        "failure_mode": "TIMING_VIOLATION",
        "temp_coef": -0.05,
        "vdd_coef": 5.0,
    },
    {
        "test_id": "T302_PROP_DELAY",
        "test_name": "Critical Path Propagation Delay",
        "unit": "ps",
        "nominal_vdd": 1.2,
        "nominal_temp": 85.0,
        "lower_limit": 150.0,
        "upper_limit": 380.0,
        "base_mean": 270.0,
        "base_std": 30.0,
        "failure_mode": "TIMING_VIOLATION",
        "temp_coef": 0.6,   # slower at high temp
        "vdd_coef": -40.0,  # faster at higher VDD
    },
    {
        "test_id": "T401_SCAN_CHAIN_0",
        "test_name": "Digital Logic Scan Chain Primary",
        "unit": "BER_log",
        "nominal_vdd": 1.2,
        "nominal_temp": 25.0,
        "lower_limit": 0.0,
        "upper_limit": 0.05,
        "base_mean": 0.001,
        "base_std": 0.005,
        "failure_mode": "SCAN_CHAIN",
        "temp_coef": 0.0001,
        "vdd_coef": -0.002,
    },
    {
        "test_id": "T402_SCAN_CHAIN_FAST",
        "test_name": "High-Speed At-Speed Scan Test",
        "unit": "BER_log",
        "nominal_vdd": 1.08,  # low corner
        "nominal_temp": 105.0, # high temp stress
        "lower_limit": 0.0,
        "upper_limit": 0.08,
        "base_mean": 0.012,
        "base_std": 0.015,
        "failure_mode": "SCAN_CHAIN",
        "temp_coef": 0.0003,
        "vdd_coef": -0.01,
    },
    {
        "test_id": "T501_JITTER_RMS",
        "test_name": "High-Speed Clock RMS Jitter",
        "unit": "ps",
        "nominal_vdd": 1.2,
        "nominal_temp": 25.0,
        "lower_limit": 0.5,
        "upper_limit": 3.2,
        "base_mean": 1.6,
        "base_std": 0.35,
        "failure_mode": "SIGNAL_INTEGRITY",
        "temp_coef": 0.005,
        "vdd_coef": -0.2,
    },
    {
        "test_id": "T502_EYE_HEIGHT",
        "test_name": "SerDes Receiver Eye Height",
        "unit": "mV",
        "nominal_vdd": 1.2,
        "nominal_temp": 25.0,
        "lower_limit": 140.0,
        "upper_limit": 450.0,
        "base_mean": 280.0,
        "base_std": 35.0,
        "failure_mode": "SIGNAL_INTEGRITY",
        "temp_coef": -0.3,
        "vdd_coef": 30.0,
    },
    {
        "test_id": "T601_THERMAL_SENSOR",
        "test_name": "On-Die Temperature Diode Voltage",
        "unit": "mV",
        "nominal_vdd": 1.2,
        "nominal_temp": 85.0,
        "lower_limit": 560.0,
        "upper_limit": 680.0,
        "base_mean": 620.0,
        "base_std": 12.0,
        "failure_mode": "THERMAL_STRESS",
        "temp_coef": -1.8,  # mV / C typical diode drop
        "vdd_coef": 1.0,
    },
    {
        "test_id": "T602_THERMAL_JUNCTION",
        "test_name": "Thermal Throttling Threshold Trip",
        "unit": "degC",
        "nominal_vdd": 1.32,  # high corner
        "nominal_temp": 105.0,
        "lower_limit": 100.0,
        "upper_limit": 130.0,
        "base_mean": 114.0,
        "base_std": 3.5,
        "failure_mode": "THERMAL_STRESS",
        "temp_coef": 0.05,
        "vdd_coef": 4.0,
    },
]


def generate_ate_dataset(
    n_rows: int = 12000,
    seed: int = 42,
    output_path: str = "data/demo_ate_data.csv",
    missing_rate: float = 0.02,
    duplicate_rate: float = 0.015,
    outlier_rate: float = 0.012,
) -> pd.DataFrame:
    np.random.seed(seed)
    random.seed(seed)

    lots = ["LOT_2026A", "LOT_2026B", "LOT_2026C", "LOT_2026D", "LOT_2026E"]
    # Wafer IDs per lot
    wafers = [f"W{i:02d}" for i in range(1, 13)]
    
    # Lot failure propensity multiplier (e.g., Lot D had an etching variation)
    lot_bias = {
        "LOT_2026A": 0.95,
        "LOT_2026B": 1.0,
        "LOT_2026C": 1.05,
        "LOT_2026D": 1.45,  # troubled lot
        "LOT_2026E": 0.90,
    }

    # Estimate number of devices needed
    avg_tests_per_device = 6
    num_devices = int((n_rows * 1.1) / avg_tests_per_device)
    
    records = []
    
    # Pre-generate devices with their lot and wafer
    devices = []
    for d_idx in range(1, num_devices + 1):
        lot = random.choice(lots)
        wafer = random.choice(wafers)
        dev_id = f"DEV_{lot}_{wafer}_{d_idx:05d}"
        # Some devices have inherent flaw rate
        is_bad_silicon = (np.random.rand() < (0.05 * lot_bias[lot]))
        devices.append((dev_id, lot, wafer, is_bad_silicon))

    row_count = 0
    dev_cursor = 0

    while row_count < n_rows:
        dev_id, lot, wafer, is_bad_silicon = devices[dev_cursor % len(devices)]
        dev_cursor += 1

        # Select a random subset of tests for this device
        k_tests = random.randint(4, 9)
        selected_tests = random.sample(TEST_DEFINITIONS, k_tests)

        for test_def in selected_tests:
            if row_count >= n_rows:
                break

            # Electrical & Thermal variations around nominal
            vdd = round(test_def["nominal_vdd"] + np.random.normal(0, 0.02), 3)
            temp = round(test_def["nominal_temp"] + np.random.normal(0, 2.0), 1)

            # Measurement calculation
            delta_temp = temp - test_def["nominal_temp"]
            delta_vdd = vdd - test_def["nominal_vdd"]

            meas = (
                test_def["base_mean"]
                + delta_temp * test_def["temp_coef"]
                + delta_vdd * test_def["vdd_coef"]
                + np.random.normal(0, test_def["base_std"])
            )

            lower_lim = test_def["lower_limit"]
            upper_lim = test_def["upper_limit"]

            # If bad silicon or troubled lot, shift or widen measurement towards failure
            if is_bad_silicon:
                shift_dir = 1 if np.random.rand() > 0.5 else -1
                meas += shift_dir * test_def["base_std"] * np.random.uniform(1.8, 3.5)

            # Check specification limits
            is_fail = (meas < lower_lim) or (meas > upper_lim)
            
            # Subtle edge cases: marginal fails or noisy borderline passes
            if is_fail:
                result = "FAIL"
                failure_mode = test_def["failure_mode"]
                # Bad silicon might trigger secondary root causes
                if np.random.rand() < 0.15:
                    failure_mode = random.choice(["UNKNOWN", "VOLTAGE_MARGIN", "TIMING_VIOLATION"])
                retest_count = int(np.random.choice([0, 1, 2, 3], p=[0.4, 0.4, 0.15, 0.05]))
            else:
                result = "PASS"
                failure_mode = "NONE"
                retest_count = int(np.random.choice([0, 1], p=[0.92, 0.08]))

            # Round measurement cleanly
            meas = round(float(meas), 4)

            records.append({
                "Device_ID": dev_id,
                "Test_ID": test_def["test_id"],
                "Test_Name": test_def["test_name"],
                "Lot_ID": lot,
                "Wafer_ID": wafer,
                "VDD_V": vdd,
                "Temperature_C": temp,
                "Measured_Value": meas,
                "Lower_Limit": lower_lim,
                "Upper_Limit": upper_lim,
                "Result": result,
                "Failure_Mode": failure_mode,
                "Retest_Count": retest_count,
            })
            row_count += 1

    df = pd.DataFrame(records)

    # 1. Inject deliberate Outliers (statistically anomalous values that may blow past normal distributions)
    n_outliers = int(len(df) * outlier_rate)
    outlier_indices = np.random.choice(df.index, size=n_outliers, replace=False)
    for idx in outlier_indices:
        span = df.loc[idx, "Upper_Limit"] - df.loc[idx, "Lower_Limit"]
        mult = np.random.choice([-1, 1]) * np.random.uniform(2.5, 6.0)
        df.loc[idx, "Measured_Value"] = round(df.loc[idx, "Measured_Value"] + mult * span, 4)
        # Often marked as FAIL with POWER_ANOMALY or THERMAL_STRESS
        if df.loc[idx, "Measured_Value"] < df.loc[idx, "Lower_Limit"] or df.loc[idx, "Measured_Value"] > df.loc[idx, "Upper_Limit"]:
            df.loc[idx, "Result"] = "FAIL"
            if df.loc[idx, "Failure_Mode"] == "NONE":
                df.loc[idx, "Failure_Mode"] = "POWER_ANOMALY"

    # 2. Inject Missing Values (controlled across various columns)
    cols_to_null = ["VDD_V", "Temperature_C", "Measured_Value", "Failure_Mode", "Retest_Count"]
    for col in cols_to_null:
        n_miss = int(len(df) * missing_rate * np.random.uniform(0.5, 1.2))
        miss_indices = np.random.choice(df.index, size=n_miss, replace=False)
        if col in ["VDD_V", "Temperature_C", "Measured_Value"]:
            df.loc[miss_indices, col] = np.nan
        elif col == "Failure_Mode":
            # Only nullify some failures or some passes
            df.loc[miss_indices, col] = np.nan
        elif col == "Retest_Count":
            df.loc[miss_indices, col] = np.nan

    # 3. Inject Exact Duplicates (test re-transmission or logging glitch)
    n_duplicates = int(len(df) * duplicate_rate)
    dup_indices = np.random.choice(df.index, size=n_duplicates, replace=False)
    dup_rows = df.loc[dup_indices].copy()
    df = pd.concat([df, dup_rows], ignore_index=True)

    # Save to output path
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_file, index=False)
    print(f"[Synthetic ATE Generator] Successfully generated {len(df)} records into '{out_file}'")
    print(f"  - Lots: {df['Lot_ID'].nunique()}")
    print(f"  - Wafers: {df['Wafer_ID'].nunique()}")
    print(f"  - Devices: {df['Device_ID'].nunique()}")
    print(f"  - Tests: {df['Test_ID'].nunique()}")
    print(f"  - Overall PASS yield: {(df['Result'] == 'PASS').mean()*100:.2f}%")
    print(f"  - Total Exact Duplicates: {df.duplicated().sum()}")
    print(f"  - Total Missing cells: {df.isna().sum().sum()}")
    
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic ATE dataset")
    parser.add_argument("--rows", type=int, default=12000, help="Number of records to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--output", type=str, default="data/demo_ate_data.csv", help="Output CSV path")
    args = parser.parse_args()

    generate_ate_dataset(n_rows=args.rows, seed=args.seed, output_path=args.output)
