"use client";

import { useState } from "react";
import { submitPrediction } from "@/lib/api";
import { Flame, CheckCircle, AlertTriangle, ArrowRight, Activity, Cpu } from "lucide-react";

export default function PredictionPage() {
  const [formData, setFormData] = useState({
    Device_ID: "DEV_UNSEEN_9901",
    Test_ID: "T101_LEAKAGE",
    Test_Name: "Standby Leakage Current",
    Lot_ID: "LOT_2026D",
    Wafer_ID: "W04",
    VDD_V: 1.25,
    Temperature_C: 95.0,
    Measured_Value: 4.88,
    Lower_Limit: 0.05,
    Upper_Limit: 5.00,
    Retest_Count: 1,
  });

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await submitPrediction({
        ...formData,
        VDD_V: Number(formData.VDD_V),
        Temperature_C: Number(formData.Temperature_C),
        Measured_Value: Number(formData.Measured_Value),
        Lower_Limit: Number(formData.Lower_Limit),
        Upper_Limit: Number(formData.Upper_Limit),
        Retest_Count: Number(formData.Retest_Count),
      });
      setResult(res);
    } catch (err: any) {
      setError(err.message || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">ML Failure Prediction on Unseen Units</h1>
        <p className="text-xs text-slate-400 mt-1">
          Demonstrate trained machine learning pipeline inferences on unseen ATE test telemetry records.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Form Container */}
        <form onSubmit={handleSubmit} className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
          <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-2 flex items-center space-x-2">
            <Cpu className="h-4 w-4 text-blue-400" />
            <span>Unseen Test Telemetry Input</span>
          </h3>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[11px] font-mono text-slate-400">Device ID</label>
              <input
                type="text"
                value={formData.Device_ID}
                onChange={(e) => setFormData({ ...formData, Device_ID: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 text-white text-xs rounded p-2 font-mono"
              />
            </div>
            <div>
              <label className="text-[11px] font-mono text-slate-400">Test ID</label>
              <input
                type="text"
                value={formData.Test_ID}
                onChange={(e) => setFormData({ ...formData, Test_ID: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 text-white text-xs rounded p-2 font-mono"
              />
            </div>
            <div>
              <label className="text-[11px] font-mono text-slate-400">Lot ID</label>
              <input
                type="text"
                value={formData.Lot_ID}
                onChange={(e) => setFormData({ ...formData, Lot_ID: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 text-white text-xs rounded p-2 font-mono"
              />
            </div>
            <div>
              <label className="text-[11px] font-mono text-slate-400">Wafer ID</label>
              <input
                type="text"
                value={formData.Wafer_ID}
                onChange={(e) => setFormData({ ...formData, Wafer_ID: e.target.value })}
                className="w-full bg-slate-950 border border-slate-800 text-white text-xs rounded p-2 font-mono"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="text-[11px] font-mono text-slate-400">VDD (V)</label>
              <input
                type="number"
                step="0.01"
                value={formData.VDD_V}
                onChange={(e) => setFormData({ ...formData, VDD_V: parseFloat(e.target.value) })}
                className="w-full bg-slate-950 border border-slate-800 text-white text-xs rounded p-2 font-mono"
              />
            </div>
            <div>
              <label className="text-[11px] font-mono text-slate-400">Temperature (°C)</label>
              <input
                type="number"
                step="0.1"
                value={formData.Temperature_C}
                onChange={(e) => setFormData({ ...formData, Temperature_C: parseFloat(e.target.value) })}
                className="w-full bg-slate-950 border border-slate-800 text-white text-xs rounded p-2 font-mono"
              />
            </div>
            <div>
              <label className="text-[11px] font-mono text-slate-400">Retest Count</label>
              <input
                type="number"
                value={formData.Retest_Count}
                onChange={(e) => setFormData({ ...formData, Retest_Count: parseInt(e.target.value) })}
                className="w-full bg-slate-950 border border-slate-800 text-white text-xs rounded p-2 font-mono"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="text-[11px] font-mono text-slate-400">Measured Value</label>
              <input
                type="number"
                step="0.001"
                value={formData.Measured_Value}
                onChange={(e) => setFormData({ ...formData, Measured_Value: parseFloat(e.target.value) })}
                className="w-full bg-slate-950 border border-slate-800 text-white text-xs rounded p-2 font-mono font-bold text-blue-400"
              />
            </div>
            <div>
              <label className="text-[11px] font-mono text-slate-400">Lower Limit</label>
              <input
                type="number"
                step="0.001"
                value={formData.Lower_Limit}
                onChange={(e) => setFormData({ ...formData, Lower_Limit: parseFloat(e.target.value) })}
                className="w-full bg-slate-950 border border-slate-800 text-white text-xs rounded p-2 font-mono"
              />
            </div>
            <div>
              <label className="text-[11px] font-mono text-slate-400">Upper Limit</label>
              <input
                type="number"
                step="0.001"
                value={formData.Upper_Limit}
                onChange={(e) => setFormData({ ...formData, Upper_Limit: parseFloat(e.target.value) })}
                className="w-full bg-slate-950 border border-slate-800 text-white text-xs rounded p-2 font-mono"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold py-2.5 rounded-lg transition"
          >
            {loading ? "Running Inference Pipeline..." : "Execute Real-Time Model Inference"}
          </button>
        </form>

        {/* Inference Results Output */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
          <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-2 flex items-center space-x-2">
            <Flame className="h-4 w-4 text-amber-400" />
            <span>Model Prediction & Attribution</span>
          </h3>

          {error && (
            <div className="p-3 bg-rose-500/10 border border-rose-500/30 text-rose-400 rounded-lg text-xs">
              {error}
            </div>
          )}

          {!result && !error && (
            <div className="text-center py-16 text-slate-500 text-xs">
              Submit the form on the left to trigger the trained ML classifier.
            </div>
          )}

          {result && (
            <div className="space-y-4">
              <div className="p-4 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
                <div>
                  <div className="text-xs text-slate-400 font-mono">Predicted Outcome:</div>
                  <div className={`text-2xl font-extrabold font-mono mt-1 ${result.prediction === "FAIL" ? "text-rose-400" : "text-emerald-400"
                    }`}>
                    {result.prediction}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xs text-slate-400 font-mono">Failure Probability:</div>
                  <div className="text-xl font-bold text-white font-mono mt-1">
                    {Math.round(result.probability_of_fail * 100)}%
                  </div>
                </div>
              </div>

              <div className="text-xs text-slate-300 font-mono bg-slate-950 p-3 rounded-lg border border-slate-800">
                {result.engineering_summary}
              </div>

              {/* Feature Contributions */}
              <div className="space-y-2">
                <div className="text-xs font-semibold text-slate-400 uppercase">Parametric Influence Drivers</div>
                {result.top_contributions?.map((c: any, i: number) => (
                  <div key={i} className="p-2.5 bg-slate-950 rounded border border-slate-800 flex justify-between items-center text-xs">
                    <div>
                      <span className="font-mono text-white font-bold">{c.feature}</span> ({c.value})
                      <div className="text-[11px] text-slate-400 mt-0.5">{c.impact_note}</div>
                    </div>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${c.influence === "INCREASES_FAIL_RISK" ? "bg-rose-500/10 text-rose-400 border border-rose-500/20" : "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                      }`}>
                      {c.influence}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
