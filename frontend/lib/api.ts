const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function fetchOverview() {
  const res = await fetch(`${API_BASE}/overview`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load overview data.");
  return res.json();
}

export async function fetchQuality() {
  const res = await fetch(`${API_BASE}/data-quality`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load data quality data.");
  return res.json();
}

export async function fetchYield() {
  const res = await fetch(`${API_BASE}/yield`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load yield analytics.");
  return res.json();
}

export async function fetchFailures() {
  const res = await fetch(`${API_BASE}/failures`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load failure modes.");
  return res.json();
}

export async function fetchAnomalies() {
  const res = await fetch(`${API_BASE}/anomalies`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load anomaly detection.");
  return res.json();
}

export async function fetchModelPerformance() {
  const res = await fetch(`${API_BASE}/model-performance`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load model performance.");
  return res.json();
}

export async function fetchDevices() {
  const res = await fetch(`${API_BASE}/investigation/devices`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load devices.");
  return res.json();
}

export async function fetchDeviceInvestigation(deviceId: string) {
  const res = await fetch(`${API_BASE}/investigation/device/${encodeURIComponent(deviceId)}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to load device ${deviceId}`);
  return res.json();
}

export async function fetchRecordInvestigation(deviceId: string, testId: string) {
  const res = await fetch(`${API_BASE}/investigation/record?device_id=${encodeURIComponent(deviceId)}&test_id=${encodeURIComponent(testId)}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load record investigation.");
  return res.json();
}

export async function submitPrediction(record: any) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(record),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Prediction request failed.");
  }
  return res.json();
}

export async function processDemoDataset() {
  const res = await fetch(`${API_BASE}/process-demo`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to trigger demo dataset processing.");
  return res.json();
}

export async function uploadDatasetFile(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Upload failed.");
  }
  return res.json();
}
