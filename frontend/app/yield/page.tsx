"use client";

import { useEffect, useState } from "react";
import { fetchYield, fetchFailures } from "@/lib/api";
import { Layers, AlertCircle, BarChart3, TrendingUp, CheckCircle2 } from "lucide-react";

export default function YieldPage() {
  const [yieldData, setYieldData] = useState<any>(null);
  const [failureData, setFailureData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"lot" | "wafer" | "test">("lot");

  useEffect(() => {
    Promise.all([fetchYield(), fetchFailures()])
      .then(([y, f]) => {
        setYieldData(y);
        setFailureData(f);
      })
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

  if (!yieldData) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center max-w-xl mx-auto my-12">
        <h2 className="text-lg font-bold text-white mb-2">No Yield Data Available</h2>
        <p className="text-xs text-slate-400">Please load or upload an ATE dataset to populate yield analytics.</p>
      </div>
    );
  }

  const overall = yieldData.overall;
  const groups = activeTab === "lot" ? yieldData.by_lot : activeTab === "wafer" ? yieldData.by_wafer : yieldData.by_test;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Yield & Failure Mode Intelligence</h1>
        <p className="text-xs text-slate-400 mt-1">
          Grouped yield calculations across Lots, Wafers, and Individual Tests, along with Pareto failure modes.
        </p>
      </div>

      {/* Yield Banner */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Overall PASS Yield</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">{overall?.pass_yield_pct}%</div>
          <div className="text-xs text-slate-500 mt-1">{overall?.pass_count?.toLocaleString()} passing units</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Total FAIL Rate</div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{overall?.fail_rate_pct}%</div>
          <div className="text-xs text-slate-500 mt-1">{overall?.fail_count?.toLocaleString()} failing units</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Retest Rate</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{overall?.retest_rate_pct}%</div>
          <div className="text-xs text-slate-500 mt-1">{overall?.retest_records} units retested</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Total Devices & Wafers</div>
          <div className="text-2xl font-bold text-white mt-1">{overall?.total_devices?.toLocaleString()}</div>
          <div className="text-xs text-slate-500 mt-1">{overall?.total_lots} Lots &bull; {overall?.total_wafers} Wafers</div>
        </div>
      </div>

      {/* Grouped Yield Breakdown & Interactive Visual Representation */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-4 border-b border-slate-800 mb-4">
          <h3 className="text-sm font-semibold text-white uppercase tracking-wider">
            Grouped Yield Performance
          </h3>
          <div className="flex space-x-1 mt-2 sm:mt-0 bg-slate-950 p-1 rounded-lg border border-slate-800">
            <button
              onClick={() => setActiveTab("lot")}
              className={`px-3 py-1 text-xs rounded-md font-medium transition ${activeTab === "lot" ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"
                }`}
            >
              By Lot
            </button>
            <button
              onClick={() => setActiveTab("wafer")}
              className={`px-3 py-1 text-xs rounded-md font-medium transition ${activeTab === "wafer" ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"
                }`}
            >
              By Wafer
            </button>
            <button
              onClick={() => setActiveTab("test")}
              className={`px-3 py-1 text-xs rounded-md font-medium transition ${activeTab === "test" ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"
                }`}
            >
              By Test ID
            </button>
          </div>
        </div>

        {/* Visual Bar Yield Chart (Dynamic SVG / HTML Bar rendering) */}
        <div className="space-y-3 mb-6">
          {groups?.slice(0, 8).map((g: any) => (
            <div key={g.group_value} className="space-y-1">
              <div className="flex justify-between text-xs font-mono">
                <span className="text-slate-200 font-medium">{g.group_value}</span>
                <span className="text-slate-400">
                  Yield: <strong className="text-emerald-400">{g.pass_yield_pct}%</strong> | Fail: <strong className="text-rose-400">{g.fail_rate_pct}%</strong> ({g.fail_count}/{g.total_tests})
                </span>
              </div>
              <div className="h-3 w-full bg-slate-950 rounded-full overflow-hidden flex border border-slate-800">
                <div style={{ width: `${g.pass_yield_pct}%` }} className="bg-emerald-500 h-full transition-all"></div>
                <div style={{ width: `${g.fail_rate_pct}%` }} className="bg-rose-500 h-full transition-all"></div>
              </div>
            </div>
          ))}
        </div>

        {/* Tabular Details */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950 text-slate-400 uppercase font-mono">
              <tr>
                <th className="py-2.5 px-3">Identifier ({activeTab.toUpperCase()})</th>
                <th className="py-2.5 px-3">Total Tests</th>
                <th className="py-2.5 px-3">PASS Count</th>
                <th className="py-2.5 px-3">FAIL Count</th>
                <th className="py-2.5 px-3">Yield %</th>
                <th className="py-2.5 px-3">FAIL Rate %</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {groups?.map((g: any) => (
                <tr key={g.group_value} className="hover:bg-slate-850">
                  <td className="py-2.5 px-3 font-mono font-medium text-white">{g.group_value}</td>
                  <td className="py-2.5 px-3">{g.total_tests}</td>
                  <td className="py-2.5 px-3 text-emerald-400 font-mono">{g.pass_count}</td>
                  <td className="py-2.5 px-3 text-rose-400 font-mono">{g.fail_count}</td>
                  <td className="py-2.5 px-3 font-mono font-semibold text-emerald-400">{g.pass_yield_pct}%</td>
                  <td className="py-2.5 px-3 font-mono font-semibold text-rose-400">{g.fail_rate_pct}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Top Failing Tests & Failure Modes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Top Failing Tests */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
          <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4 flex items-center space-x-2">
            <AlertCircle className="h-4 w-4 text-rose-400" />
            <span>Top Failing Tests (Pareto by Count & Rate)</span>
          </h3>
          <div className="space-y-3">
            {failureData?.top_failing_tests?.map((t: any) => (
              <div key={t.test_id} className="p-3 bg-slate-950 rounded-lg border border-slate-800 flex justify-between items-center">
                <div>
                  <div className="font-mono text-xs font-semibold text-white">{t.test_id}</div>
                  <div className="text-xs text-slate-400">{t.test_name}</div>
                  <div className="text-[11px] text-amber-400 mt-1">Mode: {t.dominant_failure_mode}</div>
                </div>
                <div className="text-right font-mono">
                  <div className="text-sm font-bold text-rose-400">{t.fail_count} fails</div>
                  <div className="text-xs text-slate-500">{t.fail_rate_pct}% fail rate</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Common Failure Modes */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
          <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4 flex items-center space-x-2">
            <BarChart3 className="h-4 w-4 text-blue-400" />
            <span>Failure Mode Distribution</span>
          </h3>
          <div className="space-y-3">
            {failureData?.failure_modes?.map((fm: any) => (
              <div key={fm.failure_mode} className="space-y-1">
                <div className="flex justify-between text-xs font-mono">
                  <span className="text-slate-300 font-medium">{fm.failure_mode}</span>
                  <span className="text-slate-400">
                    <strong className="text-blue-400">{fm.percentage_of_failures}%</strong> of fails ({fm.count} units)
                  </span>
                </div>
                <div className="h-2.5 w-full bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                  <div style={{ width: `${fm.percentage_of_failures}%` }} className="bg-blue-500 h-full"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
