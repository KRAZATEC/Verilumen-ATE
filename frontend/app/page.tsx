"use client";

import { useEffect, useState } from "react";
import { fetchOverview, processDemoDataset, uploadDatasetFile } from "@/lib/api";
import {
  Upload,
  CheckCircle,
  AlertCircle,
  Cpu,
  BarChart,
  Activity,
  Database,
  Layers,
  ArrowRight
} from "lucide-react";
import Link from "next/link";

export default function OverviewPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await fetchOverview();
      setData(res);
    } catch (err: any) {
      setError(err.message || "Failed to connect to backend server.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleDemoClick = async () => {
    try {
      setUploading(true);
      await processDemoDataset();
      await loadData();
    } catch (err: any) {
      alert("Demo load failed: " + err.message);
    } finally {
      setUploading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      setUploading(true);
      await uploadDatasetFile(file);
      await loadData();
    } catch (err: any) {
      alert("File upload error: " + err.message);
    } finally {
      setUploading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-slate-400 font-mono text-sm">Querying Verilumen ATE telemetry pipeline...</p>
      </div>
    );
  }

  if (!data?.loaded) {
    return (
      <div className="max-w-4xl mx-auto py-12 px-4 sm:px-6">
        <div className="text-center space-y-4 mb-10">
          <div className="inline-flex p-3 rounded-2xl bg-blue-500/10 text-blue-400 mb-2 border border-blue-500/20">
            <Cpu className="h-10 w-10 animate-pulse" />
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            Verilumen Semiconductor ATE Intelligence
          </h1>
          <p className="text-base text-slate-400 max-w-2xl mx-auto">
            Production-grade telemetry analysis for semiconductor Automated Test Equipment.
            Detect abnormal parametric drift, analyze multi-lot wafer yield, isolate failing tests, and predict device outcomes.
          </p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 shadow-xl">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Upload Box */}
            <div className="border-2 border-dashed border-slate-700 hover:border-blue-500/50 rounded-lg p-6 flex flex-col items-center justify-center text-center transition-all bg-slate-950/40">
              <Upload className="h-10 w-10 text-slate-400 mb-3" />
              <h3 className="text-sm font-semibold text-white mb-1">Upload ATE Test Dataset</h3>
              <p className="text-xs text-slate-400 mb-4">Accepts canonical ATE CSV files (up to 100MB)</p>
              <label className="cursor-pointer bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold py-2 px-4 rounded-md shadow transition">
                {uploading ? "Ingesting..." : "Select CSV File"}
                <input
                  type="file"
                  accept=".csv"
                  className="hidden"
                  onChange={handleFileUpload}
                  disabled={uploading}
                />
              </label>
            </div>

            {/* Demo Button Box */}
            <div className="border border-slate-800 rounded-lg p-6 flex flex-col items-center justify-center text-center bg-slate-950/20">
              <Database className="h-10 w-10 text-emerald-400 mb-3" />
              <h3 className="text-sm font-semibold text-white mb-1">Load High-Fidelity Synthetic Harness</h3>
              <p className="text-xs text-slate-400 mb-4">
                Instantly load 12,000+ multi-lot wafer test records with realistic electrical/thermal drift
              </p>
              <button
                onClick={handleDemoClick}
                disabled={uploading}
                className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold py-2 px-4 rounded-md shadow transition flex items-center space-x-1"
              >
                <span>{uploading ? "Ingesting..." : "Load Demo Dataset"}</span>
                <ArrowRight className="h-3 w-3" />
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const ys = data.yield_summary;
  const es = data.engineering_summary;

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center bg-slate-900 border border-slate-800 p-4 rounded-xl">
        <div>
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
            <h2 className="text-base font-semibold text-white">Active Dataset: {data.filename}</h2>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">Session ID: {data.dataset_id}</p>
        </div>

        <div className="flex space-x-2 mt-3 sm:mt-0">
          <label className="cursor-pointer bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 text-xs font-medium py-1.5 px-3 rounded-md transition flex items-center space-x-1.5">
            <Upload className="h-3.5 w-3.5" />
            <span>Upload New CSV</span>
            <input
              type="file"
              accept=".csv"
              className="hidden"
              onChange={handleFileUpload}
              disabled={uploading}
            />
          </label>
        </div>
      </div>

      {/* KPI Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
          <div className="text-xs text-slate-400 font-medium flex items-center justify-between">
            <span>Overall PASS Yield</span>
            <CheckCircle className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">{ys?.pass_yield_pct}%</div>
          <div className="text-xs text-slate-500 mt-1">{ys?.pass_count?.toLocaleString()} of {ys?.total_records?.toLocaleString()} tests</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
          <div className="text-xs text-slate-400 font-medium flex items-center justify-between">
            <span>FAIL Rate</span>
            <AlertCircle className="h-4 w-4 text-rose-400" />
          </div>
          <div className="text-2xl font-bold text-rose-400 mt-2">{ys?.fail_rate_pct}%</div>
          <div className="text-xs text-slate-500 mt-1">{ys?.fail_count?.toLocaleString()} failed executions</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
          <div className="text-xs text-slate-400 font-medium flex items-center justify-between">
            <span>Data Health Score</span>
            <Activity className="h-4 w-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold text-blue-400 mt-2">{data.quality_score}/100</div>
          <div className="text-xs text-slate-500 mt-1">Schema & Cleanliness Index</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
          <div className="text-xs text-slate-400 font-medium flex items-center justify-between">
            <span>Anomalies Flagged</span>
            <AlertCircle className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-amber-400 mt-2">{data.total_anomalies}</div>
          <div className="text-xs text-slate-500 mt-1">{data.anomaly_rate}% abnormal density</div>
        </div>
      </div>

      {/* Engineering Summary Card */}
      {es && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
          <h3 className="text-sm font-semibold text-white tracking-wide uppercase flex items-center space-x-2 mb-4">
            <span className="w-2 h-2 rounded-full bg-blue-500"></span>
            <span>Automated Engineering Synthesis</span>
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-xs font-semibold text-slate-300 uppercase mb-2">Key Observed Observations</h4>
              <ul className="space-y-2">
                {es.key_observations?.map((obs: string, idx: number) => (
                  <li key={idx} className="text-xs text-slate-300 flex items-start space-x-2">
                    <span className="text-blue-400 font-bold">•</span>
                    <span>{obs}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h4 className="text-xs font-semibold text-slate-400 uppercase mb-2">Limitations & Uncertainty</h4>
              <ul className="space-y-2">
                {es.limitations_and_caveats?.map((lim: string, idx: number) => (
                  <li key={idx} className="text-xs text-slate-400 flex items-start space-x-2">
                    <span className="text-amber-400 font-bold">&Delta;</span>
                    <span>{lim}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Quick Access Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Link href="/yield" className="group bg-slate-900 hover:bg-slate-850 border border-slate-800 p-4 rounded-xl transition">
          <BarChart className="h-6 w-6 text-blue-400 mb-2 group-hover:scale-110 transition-transform" />
          <h4 className="text-sm font-semibold text-white">Yield & Failures</h4>
          <p className="text-xs text-slate-400 mt-1">Breakdown by Lot, Wafer, Test, and Failure Mode</p>
        </Link>

        <Link href="/data-quality" className="group bg-slate-900 hover:bg-slate-850 border border-slate-800 p-4 rounded-xl transition">
          <Layers className="h-6 w-6 text-emerald-400 mb-2 group-hover:scale-110 transition-transform" />
          <h4 className="text-sm font-semibold text-white">Data Quality Audit</h4>
          <p className="text-xs text-slate-400 mt-1">Null rates, duplicates, and outlier limits</p>
        </Link>

        <Link href="/investigation" className="group bg-slate-900 hover:bg-slate-850 border border-slate-800 p-4 rounded-xl transition">
          <Activity className="h-6 w-6 text-purple-400 mb-2 group-hover:scale-110 transition-transform" />
          <h4 className="text-sm font-semibold text-white">Device Investigation</h4>
          <p className="text-xs text-slate-400 mt-1">Inspect measurements and limits for specific chips</p>
        </Link>

        <Link href="/prediction" className="group bg-slate-900 hover:bg-slate-850 border border-slate-800 p-4 rounded-xl transition">
          <Cpu className="h-6 w-6 text-amber-400 mb-2 group-hover:scale-110 transition-transform" />
          <h4 className="text-sm font-semibold text-white">ML Inference</h4>
          <p className="text-xs text-slate-400 mt-1">Predict unseen records and evaluate explainability</p>
        </Link>
      </div>
    </div>
  );
}
