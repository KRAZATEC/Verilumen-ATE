"use client";

import { useEffect, useState } from "react";
import { fetchDevices, fetchDeviceInvestigation, fetchRecordInvestigation } from "@/lib/api";
import { Search, Cpu, AlertCircle, ShieldCheck, Thermometer, Zap } from "lucide-react";

export default function InvestigationPage() {
  const [devices, setDevices] = useState<string[]>([]);
  const [selectedDevice, setSelectedDevice] = useState<string>("");
  const [deviceData, setDeviceData] = useState<any>(null);
  const [selectedTest, setSelectedTest] = useState<string>("");
  const [recordData, setRecordData] = useState<any>(null);
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

  useEffect(() => {
    if (!selectedDevice) return;
    setLoading(true);
    fetchDeviceInvestigation(selectedDevice)
      .then((data) => {
        setDeviceData(data);
        if (data.records?.length > 0) {
          setSelectedTest(data.records[0].Test_ID);
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, [selectedDevice]);

  useEffect(() => {
    if (!selectedDevice || !selectedTest) return;
    fetchRecordInvestigation(selectedDevice, selectedTest)
      .then(setRecordData)
      .catch((err) => console.error(err));
  }, [selectedDevice, selectedTest]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Failure & Device Investigation</h1>
        <p className="text-xs text-slate-400 mt-1">
          Deep-dive inspection into specific silicon units, test measurements, specification bounds, and telemetry conditions.
        </p>
      </div>

      {/* Selectors Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col sm:flex-row gap-4 items-center">
        <div className="flex-1 w-full sm:w-auto">
          <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
            Select Device Under Test (DUT)
          </label>
          <select
            value={selectedDevice}
            onChange={(e) => setSelectedDevice(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 text-white text-xs rounded-lg px-3 py-2 outline-none focus:border-blue-500 font-mono"
          >
            {devices.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </div>

        {deviceData && (
          <div className="flex space-x-6 text-xs font-mono text-slate-400 pt-3 sm:pt-0">
            <div>
              Lot: <span className="text-white font-bold">{deviceData.lot_id}</span>
            </div>
            <div>
              Wafer: <span className="text-white font-bold">{deviceData.wafer_id}</span>
            </div>
            <div>
              Executed Tests: <span className="text-white font-bold">{deviceData.total_tests_logged}</span>
            </div>
            <div>
              Fails: <span className={deviceData.fails_count > 0 ? "text-rose-400 font-bold" : "text-emerald-400 font-bold"}>{deviceData.fails_count}</span>
            </div>
          </div>
        )}
      </div>

      {/* Device Tests Table */}
      {deviceData && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm">
          <h3 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">
            Test Execution Log for {selectedDevice}
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 uppercase font-mono">
                <tr>
                  <th className="py-2.5 px-3">Test ID & Name</th>
                  <th className="py-2.5 px-3">VDD & Temp</th>
                  <th className="py-2.5 px-3">Measured Value</th>
                  <th className="py-2.5 px-3">Spec Limits [LL, UL]</th>
                  <th className="py-2.5 px-3">Result</th>
                  <th className="py-2.5 px-3">Failure Mode</th>
                  <th className="py-2.5 px-3">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {deviceData.records?.map((rec: any) => (
                  <tr
                    key={rec.Test_ID}
                    className={`cursor-pointer transition ${selectedTest === rec.Test_ID ? "bg-blue-900/30 font-medium" : "hover:bg-slate-850"
                      }`}
                    onClick={() => setSelectedTest(rec.Test_ID)}
                  >
                    <td className="py-2.5 px-3">
                      <div className="font-mono text-white font-semibold">{rec.Test_ID}</div>
                      <div className="text-[11px] text-slate-400">{rec.Test_Name}</div>
                    </td>
                    <td className="py-2.5 px-3 font-mono text-slate-400">
                      {rec.VDD_V}V &bull; {rec.Temperature_C}°C
                    </td>
                    <td className="py-2.5 px-3 font-mono font-bold text-white">{rec.Measured_Value}</td>
                    <td className="py-2.5 px-3 font-mono text-slate-400">[{rec.Lower_Limit}, {rec.Upper_Limit}]</td>
                    <td className="py-2.5 px-3 font-mono">
                      <span className={rec.Result === "FAIL" ? "text-rose-400 font-bold" : "text-emerald-400 font-bold"}>
                        {rec.Result}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 font-mono text-slate-400">{rec.Failure_Mode || "NONE"}</td>
                    <td className="py-2.5 px-3">
                      <button
                        onClick={() => setSelectedTest(rec.Test_ID)}
                        className="text-[11px] text-blue-400 hover:underline font-mono"
                      >
                        Inspect &rarr;
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Deep-Dive Inspection Card for Selected Record */}
      {recordData && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm space-y-4">
          <div className="flex justify-between items-center border-b border-slate-800 pb-3">
            <div>
              <h3 className="text-base font-bold text-white font-mono">
                Telemetry Deep Dive: {selectedDevice} &bull; {selectedTest}
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">{recordData.record?.Test_Name}</p>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono text-slate-400">Result:</span>
              <span className={`px-2.5 py-1 rounded text-xs font-bold font-mono ${recordData.record?.Result === "FAIL" ? "bg-rose-500/20 text-rose-400 border border-rose-500/30" : "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                }`}>
                {recordData.record?.Result}
              </span>
            </div>
          </div>

          <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 font-mono text-xs whitespace-pre-wrap text-slate-300">
            {recordData.narrative}
          </div>
        </div>
      )}
    </div>
  );
}
