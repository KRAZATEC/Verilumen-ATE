"use client";

import { useEffect, useState } from "react";
import { fetchAnomalies } from "@/lib/api";
import { AlertTriangle, ShieldAlert, Cpu, Activity, Info } from "lucide-react";

export default function AnomaliesPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnomalies()
      .then(setData)
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!data?.total_records_analyzed) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center max-w-xl mx-auto my-12">
        <h2 className="text-lg font-bold text-white mb-2">No Anomaly Telemetry Available</h2>
        <p className="text-xs text-slate-400">Please load or upload an ATE dataset first.</p>
      </div>
    );
  }

  const matrix = data.anomaly_vs_fail_matrix || {};

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">ATE Anomaly Detection & Ranking</h1>
        <p className="text-xs text-slate-400 mt-1">
          Two-layer anomaly pipeline combining robust statistics (IQR/MAD & specification boundary proximity) and multivariate Isolation Forest.
        </p>
      </div>

      {/* Anomaly Metrics Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Flagged Anomalies</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{data.total_anomalies_flagged}</div>
          <div className="text-xs text-slate-500 mt-1">{data.anomaly_rate_pct}% anomaly rate</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Max Composite Anomaly Score</div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{data.max_anomaly_score}/100</div>
          <div className="text-xs text-slate-500 mt-1">Avg score: {data.avg_anomaly_score}</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Suspicious PASS (Golden Anomaly)</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{matrix.Anomaly_PASS || 0}</div>
          <div className="text-xs text-slate-500 mt-1">Passed spec but statistically anomalous</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Anomaly + Confirmed FAIL</div>
          <div className="text-2xl font-bold text-rose-500 mt-1">{matrix.Anomaly_FAIL || 0}</div>
          <div className="text-xs text-slate-500 mt-1">Dual-flagged catastrophic failures</div>
        </div>
      </div>

      {/* Ranked Suspicious Records Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
        <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4 flex items-center space-x-2">
          <AlertTriangle className="h-4 w-4 text-amber-400" />
          <span>Top Ranked Suspicious Records</span>
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950 text-slate-400 uppercase font-mono">
              <tr>
                <th className="py-2.5 px-3">Rank</th>
                <th className="py-2.5 px-3">Device & Test ID</th>
                <th className="py-2.5 px-3">Lot / Wafer</th>
                <th className="py-2.5 px-3">Measured vs Specs</th>
                <th className="py-2.5 px-3">Anomaly Score</th>
                <th className="py-2.5 px-3">Result & Mode</th>
                <th className="py-2.5 px-3">Detector Evidence</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {data.top_suspicious_records?.slice(0, 15).map((r: any) => (
                <tr key={r.rank} className="hover:bg-slate-850">
                  <td className="py-2.5 px-3 font-mono font-bold text-amber-400">#{r.rank}</td>
                  <td className="py-2.5 px-3">
                    <div className="font-mono text-white font-medium">{r.device_id}</div>
                    <div className="text-[11px] text-slate-400 font-mono">{r.test_id}</div>
                  </td>
                  <td className="py-2.5 px-3 font-mono text-slate-400">{r.lot_id} / {r.wafer_id}</td>
                  <td className="py-2.5 px-3 font-mono">
                    <span className="text-white font-bold">{r.measured_value}</span>{" "}
                    <span className="text-slate-500">[{r.lower_limit}, {r.upper_limit}]</span>
                  </td>
                  <td className="py-2.5 px-3">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20">
                      {r.anomaly_score}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 font-mono">
                    <span className={r.result === "FAIL" ? "text-rose-400 font-bold" : "text-emerald-400"}>
                      {r.result}
                    </span>{" "}
                    <span className="text-[11px] text-slate-500">({r.failure_mode})</span>
                  </td>
                  <td className="py-2.5 px-3 text-[11px] text-slate-300 max-w-xs">
                    {r.detector_evidence?.map((e: string, i: number) => (
                      <div key={i}>&bull; {e}</div>
                    ))}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
