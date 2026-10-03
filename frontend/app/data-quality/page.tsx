"use client";

import { useEffect, useState } from "react";
import { fetchQuality } from "@/lib/api";
import { ShieldAlert, ShieldCheck, FileSpreadsheet, AlertOctagon, HelpCircle } from "lucide-react";

export default function DataQualityPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchQuality()
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center max-w-xl mx-auto my-12">
        <AlertOctagon className="h-12 w-12 text-amber-500 mx-auto mb-3" />
        <h2 className="text-lg font-bold text-white mb-2">No Active Dataset Loaded</h2>
        <p className="text-xs text-slate-400 mb-4">Please upload an ATE CSV dataset on the Overview page first.</p>
      </div>
    );
  }

  const { schema_report, quality_report } = data;
  const dup = quality_report?.duplicate_summary;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">ATE Data Quality & Schema Profiling</h1>
        <p className="text-xs text-slate-400 mt-1">
          Comprehensive schema integrity checks, type inference, missing value imputation tracking, and outlier detection.
        </p>
      </div>

      {/* Top Banner Health Score */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Schema Status</div>
          <div className="flex items-center space-x-2 mt-2">
            {schema_report?.is_valid ? (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <ShieldCheck className="w-3.5 h-3.5 mr-1" /> VALID SCHEMA
              </span>
            ) : (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-rose-500/10 text-rose-400 border border-rose-500/20">
                <ShieldAlert className="w-3.5 h-3.5 mr-1" /> SCHEMA ISSUES
              </span>
            )}
          </div>
          <div className="text-xs text-slate-500 mt-2">
            {schema_report?.total_rows?.toLocaleString()} rows &bull; {schema_report?.total_columns} columns
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Exact Redundant Duplicates</div>
          <div className="text-2xl font-bold text-white mt-1">
            {dup?.total_duplicate_rows || 0}
          </div>
          <div className="text-xs text-slate-500 mt-1">
            {dup?.duplicate_percentage}% of raw stream &bull; Policy: Filtered in clean layer
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <div className="text-xs text-slate-400 font-medium">Overall Quality Index</div>
          <div className="text-2xl font-bold text-blue-400 mt-1">
            {quality_report?.overall_health_score}/100
          </div>
          <div className="text-xs text-slate-500 mt-1">
            Penalized by missingness & duplicate rates
          </div>
        </div>
      </div>

      {/* Missing Values Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
        <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4 flex items-center space-x-2">
          <span>Missing Values & Imputation Audit</span>
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950 text-slate-400 uppercase font-mono">
              <tr>
                <th className="py-2.5 px-3">Column Name</th>
                <th className="py-2.5 px-3">Data Type</th>
                <th className="py-2.5 px-3">Missing Count</th>
                <th className="py-2.5 px-3">Missing %</th>
                <th className="py-2.5 px-3">Applied Imputation Policy</th>
                <th className="py-2.5 px-3">Imputed Value</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {quality_report?.missing_records_summary?.map((m: any) => (
                <tr key={m.column} className="hover:bg-slate-850">
                  <td className="py-2.5 px-3 font-mono font-medium text-white">{m.column}</td>
                  <td className="py-2.5 px-3 font-mono text-slate-400">{m.data_type}</td>
                  <td className="py-2.5 px-3">{m.missing_count}</td>
                  <td className="py-2.5 px-3">
                    <span className={m.missing_percentage > 0 ? "text-amber-400 font-medium" : "text-slate-500"}>
                      {m.missing_percentage}%
                    </span>
                  </td>
                  <td className="py-2.5 px-3 text-slate-400">{m.imputation_strategy}</td>
                  <td className="py-2.5 px-3 font-mono text-blue-400">{m.imputed_value !== null ? String(m.imputed_value) : "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Outlier Summaries */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
        <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">
          Statistical Outlier & Specification Boundary Checks
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {quality_report?.outlier_summaries?.map((o: any) => (
            <div key={o.column} className="bg-slate-950 p-4 rounded-lg border border-slate-800">
              <div className="font-mono text-xs font-semibold text-white">{o.column}</div>
              <div className="text-xs text-slate-400 mt-1">{o.method}</div>
              <div className="mt-3 space-y-1 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-400">Statistical Outliers:</span>
                  <span className="text-white font-mono">{o.outlier_count} ({o.outlier_percentage}%)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Tukey Thresholds:</span>
                  <span className="text-blue-400 font-mono">[{o.lower_threshold}, {o.upper_threshold}]</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Spec Boundary Violations:</span>
                  <span className="text-rose-400 font-mono font-medium">{o.spec_violations_count}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
