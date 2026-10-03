"""
Verilumen ATE Intelligence Platform - Streamlit Operational Engineering Console
Provides a responsive, production-grade interactive dashboard directly on top of the backend API & pipeline:
- Ingestion & CSV Upload
- Data Quality & Imputation Audit
- Yield Analytics by Lot, Wafer, Test, and Failure Mode
- Multi-Layer Anomaly Detection (Statistical + Isolation Forest)
- Device & Test Deep-Dive Failure Investigation
- Grounded Evidence Engine & AI Narrative
- Machine Learning Failure Prediction & Model Comparison Benchmarks
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path so 'backend' package is always resolvable
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

# Setup page configuration
st.set_page_config(
    page_title="Verilumen ATE Semiconductor Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for Semiconductor Engineering Theme
st.markdown("""
<style>
    .reportview-container {
        background: #090d16;
        color: #f8fafc;
    }
    .metric-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #38bdf8;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #0f172a;
        border-radius: 4px;
        color: #94a3b8;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Imports from backend pipeline
from backend.app.services.session import session_store
from backend.app.services.pipeline import process_dataset
from backend.app.core.config import settings
from backend.app.ml.predict import predict_record, PredictionRequest
from backend.app.explainability.evidence_engine import build_evidence_analysis
from backend.app.explainability.narrative import generate_narrative_text

# Sidebar - Dataset Control
st.sidebar.title("⚡ Verilumen ATE")
st.sidebar.caption("Semiconductor Test Intelligence")

# Check if session is loaded, otherwise offer demo or upload
if not session_store.is_loaded():
    demo_file = settings.DATA_DIR / "demo_ate_data.csv"
    if demo_file.exists():
        with st.spinner("Initializing high-fidelity synthetic ATE dataset..."):
            process_dataset(str(demo_file), filename="demo_ate_data.csv")

st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("Upload New ATE CSV", type=["csv"])
if uploaded_file is not None:
    if st.sidebar.button("Ingest Uploaded CSV", use_container_width=True):
        with st.spinner("Processing uploaded dataset..."):
            content = uploaded_file.getvalue()
            res = process_dataset(content, filename=uploaded_file.name)
            st.sidebar.success(f"Loaded: {uploaded_file.name}")
            st.rerun()

st.sidebar.markdown(f"**Active Session:**")
st.sidebar.text(f"File: {session_store.filename or 'None'}")
st.sidebar.text(f"Rows: {len(session_store.clean_df) if session_store.clean_df is not None else 0:,}")

# Navigation
tabs = st.tabs([
    "📊 Overview", 
    "🛡️ Data Quality", 
    "📈 Yield & Failures", 
    "⚠️ Anomalies", 
    "🔍 Investigation", 
    "🤖 AI Evidence", 
    "🔥 ML Prediction",
    "🧠 Model Comparison"
])

# ----------------- 1. OVERVIEW -----------------
with tabs[0]:
    st.subheader("Automated Test Equipment Intelligence Overview")
    ys = session_store.yield_summary
    qr = session_store.quality_report
    an = session_store.anomaly_summary
    es = session_store.engineering_summary

    if ys:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Overall PASS Yield", f"{ys.pass_yield_pct}%", f"{ys.pass_count:,} units")
        c2.metric("FAIL Rate", f"{ys.fail_rate_pct}%", f"{ys.fail_count:,} failures", delta_color="inverse")
        c3.metric("Data Health Score", f"{qr.overall_health_score}/100", "Schema & Cleanliness")
        c4.metric("Flagged Anomalies", f"{an.total_anomalies_flagged}", f"{an.anomaly_rate_pct}% rate", delta_color="inverse")

        st.markdown("---")
        st.markdown("### 📋 Automated Engineering Synthesis")
        col_obs, col_lim = st.columns(2)
        with col_obs:
            st.markdown("**Key Observed Findings**")
            for obs in es.key_observations:
                st.info(obs)
        with col_lim:
            st.markdown("**Limitations & Causal Boundaries**")
            for lim in es.limitations_and_caveats:
                st.warning(lim)

# ----------------- 2. DATA QUALITY -----------------
with tabs[1]:
    st.subheader("Schema Integrity & Data Quality Profiling")
    if qr and session_store.schema_report:
        sr = session_store.schema_report
        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric("Schema Validity", "VALID" if sr.is_valid else "ISSUES")
        col_s2.metric("Exact Duplicates Filtered", f"{qr.duplicate_summary.total_duplicate_rows}", f"{qr.duplicate_summary.duplicate_percentage}%")
        col_s3.metric("Quality Health Score", f"{qr.overall_health_score}/100")

        st.markdown("#### Missing Values & Imputation Audit")
        missing_df = pd.DataFrame([m.model_dump() for m in qr.missing_records_summary])
        st.dataframe(missing_df, use_container_width=True)

        st.markdown("#### Statistical Outliers & Specification Violations")
        outliers_df = pd.DataFrame([o.model_dump() for o in qr.outlier_summaries])
        st.dataframe(outliers_df, use_container_width=True)

# ----------------- 3. YIELD & FAILURES -----------------
with tabs[2]:
    st.subheader("Yield Breakdown & Failure Mode Analytics")
    if session_store.lot_yields:
        y_opt = st.radio("Group Yield By:", ["Lot_ID", "Wafer_ID", "Test_ID"], horizontal=True)
        if y_opt == "Lot_ID":
            records = [y.model_dump() for y in session_store.lot_yields]
        elif y_opt == "Wafer_ID":
            records = [y.model_dump() for y in session_store.wafer_yields]
        else:
            records = [y.model_dump() for y in session_store.test_yields]

        gdf = pd.DataFrame(records)
        st.dataframe(gdf, use_container_width=True)

        # Plot Pareto of Top Failing Tests & Failure Modes
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("#### Top Failing Tests (Pareto Volume)")
            top_f_df = pd.DataFrame([t.model_dump() for t in session_store.top_failing_tests])
            st.bar_chart(top_f_df.set_index("test_name")["fail_count"])

        with col_f2:
            st.markdown("#### Common Failure Modes")
            fm_df = pd.DataFrame([m.model_dump() for m in session_store.failure_modes])
            st.bar_chart(fm_df.set_index("failure_mode")["count"])

# ----------------- 4. ANOMALIES -----------------
with tabs[3]:
    st.subheader("Multi-Layer Anomaly Detection (Statistical + Isolation Forest)")
    if an:
        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Flagged Anomalies", an.total_anomalies_flagged)
        a2.metric("Anomaly Rate", f"{an.anomaly_rate_pct}%")
        a3.metric("Max Anomaly Score", f"{an.max_anomaly_score}/100")
        a4.metric("Suspicious Golden PASS", an.anomaly_vs_fail_matrix.get("Anomaly_PASS", 0))

        st.markdown("#### Top Ranked Suspicious Records")
        anom_rows = []
        for r in an.top_suspicious_records:
            anom_rows.append({
                "Rank": r.rank,
                "Device_ID": r.device_id,
                "Test_ID": r.test_id,
                "Lot": r.lot_id,
                "Wafer": r.wafer_id,
                "Measured": r.measured_value,
                "Limits": f"[{r.lower_limit}, {r.upper_limit}]",
                "Score": r.anomaly_score,
                "Result": r.result,
                "Evidence": " | ".join(r.detector_evidence),
            })
        st.dataframe(pd.DataFrame(anom_rows), use_container_width=True)

# ----------------- 5. INVESTIGATION -----------------
with tabs[4]:
    st.subheader("Deep-Dive Device & Test Investigation")
    if session_store.annotated_df is not None:
        devices = session_store.annotated_df["Device_ID"].dropna().unique().tolist()
        sel_dev = st.selectbox("Select Device Under Test (DUT):", devices[:100])
        
        dev_tests = session_store.annotated_df[session_store.annotated_df["Device_ID"] == sel_dev]
        st.markdown(f"**Execution Log for `{sel_dev}` ({len(dev_tests)} tests executed):**")
        st.dataframe(dev_tests[["Test_ID", "Test_Name", "VDD_V", "Temperature_C", "Measured_Value", "Lower_Limit", "Upper_Limit", "Result", "Failure_Mode", "Retest_Count", "anomaly_score"]], use_container_width=True)

# ----------------- 6. AI EVIDENCE ENGINE -----------------
with tabs[5]:
    st.subheader("Deterministic Evidence Synthesis & Explainability")
    if session_store.annotated_df is not None:
        c_dev, c_test = st.columns(2)
        dev_pick = c_dev.selectbox("Select DUT:", devices[:50], key="ai_dev")
        sub_tests = session_store.annotated_df[session_store.annotated_df["Device_ID"] == dev_pick]["Test_ID"].unique()
        test_pick = c_test.selectbox("Select Test:", sub_tests, key="ai_test")

        rec_match = session_store.annotated_df[(session_store.annotated_df["Device_ID"] == dev_pick) & (session_store.annotated_df["Test_ID"] == test_pick)]
        if not rec_match.empty:
            rec_dict = rec_match.iloc[0].to_dict()
            report = build_evidence_analysis(rec_dict, overall_yield_fail_rate=ys.fail_rate_pct if ys else 7.0, anomaly_score=float(rec_dict.get("anomaly_score", 0.0)))
            narrative = generate_narrative_text(report)

            col_fact, col_hyp = st.columns(2)
            with col_fact:
                st.markdown("### 🟢 Observed Physical Evidence (Facts)")
                for ev in report.observed_evidence:
                    st.success(f"**{ev.category}**: {ev.finding}")
            with col_hyp:
                st.markdown("### 🔵 Inferred Hypotheses & Possible Causes")
                for interp in report.possible_interpretations:
                    st.info(interp)
                st.markdown("---")
                st.caption(f"**Confidence**: {report.confidence_level}")
                for lim in report.limitations_and_unknowns:
                    st.warning(f"**Boundary**: {lim}")

            st.markdown("#### Technical Report Narrative")
            st.code(narrative, language="markdown")

# ----------------- 7. ML PREDICTION -----------------
with tabs[6]:
    st.subheader("Real-Time ML Failure Prediction on Unseen Units")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown("**Enter Unseen Telemetry Record:**")
        p_dev = st.text_input("Device_ID", "DEV_UNSEEN_001")
        p_test = st.selectbox("Test_ID", ["T101_LEAKAGE", "T102_IDD_ACTIVE", "T201_VOLTAGE_REF", "T302_PROP_DELAY", "T401_SCAN_CHAIN_0"])
        p_lot = st.selectbox("Lot_ID", ["LOT_2026A", "LOT_2026B", "LOT_2026C", "LOT_2026D", "LOT_2026E"])
        p_waf = st.selectbox("Wafer_ID", [f"W{i:02d}" for i in range(1, 13)])
        
        c_v, c_t, c_r = st.columns(3)
        p_vdd = c_v.number_input("VDD (V)", value=1.22, step=0.01)
        p_temp = c_t.number_input("Temp (°C)", value=85.0, step=1.0)
        p_retest = c_r.number_input("Retests", value=1, step=1)

        c_m, c_ll, c_ul = st.columns(3)
        p_meas = c_m.number_input("Measured Value", value=4.92, step=0.01)
        p_ll = c_ll.number_input("Lower Limit", value=0.05, step=0.01)
        p_ul = c_ul.number_input("Upper Limit", value=5.00, step=0.01)

        predict_btn = st.button("Execute Inference Pipeline", type="primary", use_container_width=True)

    with p_col2:
        st.markdown("**Model Output & Attribution:**")
        if predict_btn:
            req = PredictionRequest(
                Device_ID=p_dev,
                Test_ID=p_test,
                Test_Name=p_test,
                Lot_ID=p_lot,
                Wafer_ID=p_waf,
                VDD_V=p_vdd,
                Temperature_C=p_temp,
                Measured_Value=p_meas,
                Lower_Limit=p_ll,
                Upper_Limit=p_ul,
                Retest_Count=int(p_retest)
            )
            res = predict_record(req)
            if res.prediction == "FAIL":
                st.error(f"### Predicted Outcome: FAIL ({round(res.probability_of_fail*100, 1)}% Probability)")
            else:
                st.success(f"### Predicted Outcome: PASS ({round(res.probability_of_pass*100, 1)}% Probability)")

            st.caption(f"Evaluated by: `{res.model_name}` ({res.scenario})")
            st.info(res.engineering_summary)

            st.markdown("##### Parametric Feature Contributions:")
            for cont in res.top_contributions:
                st.markdown(f"- **{cont.feature}** ({cont.value}): `{cont.influence}` - {cont.impact_note}")

# ----------------- 8. MODEL COMPARISON -----------------
with tabs[7]:
    st.subheader("Machine Learning Model Comparison & Cross-Validation")
    if session_store.ml_results:
        ml_res = session_store.ml_results
        st.success(f"Selected Production Model: **{ml_res.get('best_model')}**")
        
        metrics_list = []
        for m in ml_res.get("all_metrics", {}).values():
            if hasattr(m, "model_dump"):
                metrics_list.append(m.model_dump())
            elif isinstance(m, dict):
                metrics_list.append(m)
        if metrics_list:
            m_df = pd.DataFrame(metrics_list)
            cols_to_show = [c for c in ["model_name", "f1_score", "precision", "recall", "roc_auc", "pr_auc", "accuracy"] if c in m_df.columns]
            st.dataframe(m_df[cols_to_show], use_container_width=True)

        st.markdown("---")
        st.markdown("#### Class Imbalance & Validation Notes")
        st.markdown("""
        - **Target Imbalance**: PASS is the majority (~93%), FAIL is the minority (~7%). Models are configured with `class_weight='balanced'`.
        - **Validation Strategy**: `StratifiedGroupKFold` grouped by `Device_ID` to strictly eliminate inter-device data leakage.
        - **Metrics**: Evaluated on PR-AUC, F1-Score, and ROC-AUC rather than raw accuracy.
        """)
