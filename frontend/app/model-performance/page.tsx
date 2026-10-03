"use client";

import { useEffect, useState } from "react";
import { fetchModelPerformance } from "@/lib/api";
import { BrainCircuit, Trophy, CheckCircle, ShieldAlert } from "lucide-react";

export default function ModelPerformancePage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchModelPerformance()
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

  if (!data?.all_metrics) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center max-w-xl mx-auto my-12">
        <h2 className="text-lg font-bold text-white mb-2">No Model Performance Benchmarks</h2>
        <p className="text-xs text-slate-400">Please load or upload an ATE dataset to train and compare classifiers.</p>
      </div>
    );
  }

  const models = Object.values(data.all_metrics);
  const bestModel = data.best_model;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Machine Learning Model Comparison</h1>
        <p className="text-xs text-slate-400 mt-1">
          Rigorous benchmarking across multiple classification architectures under Stratified Group K-Fold cross-validation.
        </p>
      </div>

      {/* Best Model Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-3 bg-amber-500/10 rounded-lg border border-amber-500/20 text-amber-400">
            <Trophy className="h-6 w-6" />
          </div>
          <div>
            <div className="text-xs text-slate-400 font-mono">Selected Production Classifier:</div>
            <div className="text-lg font-bold text-white font-mono">{bestModel}</div>
          </div>
        </div>
        <div className="text-xs text-slate-400 font-mono text-right">
          <div>Target: Result (FAIL=1, PASS=0)</div>
          <div>Validation: StratifiedGroupKFold (grouped by Device_ID)</div>
        </div>
      </div>

      {/* Comparison Metrics Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
        <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">
          Cross-Model Benchmark Evaluation
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950 text-slate-400 uppercase font-mono">
              <tr>
                <th className="py-2.5 px-3">Classifier Architecture</th>
                <th className="py-2.5 px-3">F1 Score</th>
                <th className="py-2.5 px-3">Precision</th>
                <th className="py-2.5 px-3">Recall</th>
                <th className="py-2.5 px-3">ROC-AUC</th>
                <th className="py-2.5 px-3">PR-AUC</th>
                <th className="py-2.5 px-3">Accuracy</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {models.map((m: any) => {
                const isBest = m.model_name === bestModel;
                return (
                  <tr key={m.model_name} className={isBest ? "bg-blue-900/20 font-medium" : "hover:bg-slate-850"}>
                    <td className="py-2.5 px-3 font-mono font-bold text-white flex items-center space-x-1.5">
                      <span>{m.model_name}</span>
                      {isBest && <span className="text-[10px] bg-blue-500 text-white px-1.5 py-0.2 rounded font-sans">BEST</span>}
                    </td>
                    <td className="py-2.5 px-3 font-mono font-bold text-emerald-400">{m.f1_score}</td>
                    <td className="py-2.5 px-3 font-mono text-slate-300">{m.precision}</td>
                    <td className="py-2.5 px-3 font-mono text-slate-300">{m.recall}</td>
                    <td className="py-2.5 px-3 font-mono text-blue-400">{m.roc_auc}</td>
                    <td className="py-2.5 px-3 font-mono text-purple-400">{m.pr_auc}</td>
                    <td className="py-2.5 px-3 font-mono text-slate-400">{m.accuracy}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Class Imbalance & Validation Notes */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm space-y-3">
        <h4 className="text-xs font-semibold text-slate-300 uppercase">Imbalance & Leakage Mitigation Strategy</h4>
        <p className="text-xs text-slate-400">
          ATE semiconductor testing features inherent class imbalance (~93% PASS, ~7% FAIL). To prevent bias toward the majority class:
        </p>
        <ul className="space-y-1.5 text-xs text-slate-400 font-mono">
          <li>&bull; Class weights are balanced inversely proportional to class frequencies across all estimators.</li>
          <li>&bull; StratifiedGroupKFold ensures that multiple test measurements from the same Device_ID do not leak across training and validation folds.</li>
          <li>&bull; Evaluated using PR-AUC and F1 rather than raw accuracy alone to prevent false confidence.</li>
        </ul>
      </div>
    </div>
  );
}
