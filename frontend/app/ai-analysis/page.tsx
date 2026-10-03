"use client";

import { useEffect, useState } from "react";
import { fetchDevices, fetchRecordInvestigation } from "@/lib/api";
import { Sparkles, CheckCircle, AlertTriangle, HelpCircle, FileText } from "lucide-react";

export default function AIAnalysisPage() {
  const [devices, setDevices] = useState<string[]>([]);
  const [selectedDevice, setSelectedDevice] = useState<string>("");
  const [selectedTest, setSelectedTest] = useState<string>("T101_LEAKAGE");
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDevices()
      .then((res) => {
        if (res.devices?.length > 0) {
          setDevices(res.devices);
          setSelectedDevice(res.devices[0]);
        }
      })
      .catch((err) => console.error(err));
  }, []);

  const runAnalysis = () => {
    if (!selectedDevice || !selectedTest) return;
    setLoading(true);
    fetchRecordInvestigation(selectedDevice, selectedTest)
      .then((data) => setAnalysisData(data.ai_analysis))
      .catch((err) => alert("Analysis query failed: " + err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    if (selectedDevice && selectedTest) {
      runAnalysis();
    }
  }, [selectedDevice, selectedTest]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Evidence-Based AI Semiconductor Analysis</h1>
        <p className="text-xs text-slate-400 mt-1">
          Deterministic Evidence Synthesis & Explainability. Strictly separates observed physical evidence from inferred engineering hypotheses.
        </p>
      </div>

      {/* Control Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col sm:flex-row gap-4 items-center">
        <div className="flex-1 w-full sm:w-auto">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
            DUT Selection
          </label>
          <select
            value={selectedDevice}
            onChange={(e) => setSelectedDevice(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 text-white text-xs rounded-lg px-3 py-2 outline-none font-mono"
          >
            {devices.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>

        <div className="flex-1 w-full sm:w-auto">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
            Test Identifier
          </label>
          <select
            value={selectedTest}
            onChange={(e) => setSelectedTest(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 text-white text-xs rounded-lg px-3 py-2 outline-none font-mono"
          >
            <option value="T101_LEAKAGE">T101_LEAKAGE (Standby Leakage)</option>
            <option value="T102_IDD_ACTIVE">T102_IDD_ACTIVE (Active Core Current)</option>
            <option value="T201_VOLTAGE_REF">T201_VOLTAGE_REF (Bandgap Reference)</option>
            <option value="T301_PLL_FREQ">T301_PLL_FREQ (PLL Lock Frequency)</option>
            <option value="T302_PROP_DELAY">T302_PROP_DELAY (Critical Path Propagation)</option>
            <option value="T401_SCAN_CHAIN_0">T401_SCAN_CHAIN_0 (Scan Chain)</option>
            <option value="T501_JITTER_RMS">T501_JITTER_RMS (Clock Jitter)</option>
            <option value="T601_THERMAL_SENSOR">T601_THERMAL_SENSOR (On-Die Diode)</option>
          </select>
        </div>

        <div className="pt-4 sm:pt-4">
          <button
            onClick={runAnalysis}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold py-2.5 px-4 rounded-lg transition"
          >
            {loading ? "Analyzing..." : "Synthesize Evidence"}
          </button>
        </div>
      </div>

      {/* Structured AI Analysis Panels */}
      {analysisData && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Panel 1: Observed Evidence (Facts) */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-sm font-semibold text-emerald-400 uppercase tracking-wider flex items-center space-x-2">
                <CheckCircle className="h-4 w-4" />
                <span>Observed Physical Evidence (Facts)</span>
              </h3>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Ground Truth
              </span>
            </div>

            <div className="space-y-3">
              {analysisData.observed_evidence?.map((ev: any, idx: number) => (
                <div key={idx} className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                  <div className="text-xs font-bold text-white font-mono">{ev.category}</div>
                  <p className="text-xs text-slate-300 mt-1">{ev.finding}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Panel 2: Inferred Engineering Interpretations (Hypotheses) */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-sm font-semibold text-blue-400 uppercase tracking-wider flex items-center space-x-2">
                <Sparkles className="h-4 w-4" />
                <span>Inferred Causes & Diagnostic Hypotheses</span>
              </h3>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                Confidence: {analysisData.confidence_level}
              </span>
            </div>

            <div className="space-y-3">
              {analysisData.possible_interpretations?.map((interp: string, idx: number) => (
                <div key={idx} className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                  <p className="text-xs text-slate-200">{interp}</p>
                </div>
              ))}
            </div>

            {/* Strict Limitations Box */}
            <div className="mt-4 p-3 bg-slate-950 rounded-lg border border-slate-800">
              <div className="text-[11px] font-bold text-slate-400 uppercase flex items-center space-x-1 mb-1">
                <AlertTriangle className="h-3 w-3 text-amber-400" />
                <span>Limitations & Unknowns</span>
              </div>
              <ul className="space-y-1">
                {analysisData.limitations_and_unknowns?.map((lim: string, idx: number) => (
                  <li key={idx} className="text-[11px] text-slate-400">&bull; {lim}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
