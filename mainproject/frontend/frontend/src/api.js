const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function createSession() {
  const r = await fetch(`${API_BASE}/session`, { method: "POST" });
  return r.json();
}

export async function execCommand(sessionId, command) {
  const r = await fetch(`${API_BASE}/execute`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, command })
  });
  return r.json();
}

export async function complete(sessionId, prefix) {
  const url = new URL(`${API_BASE}/complete`);
  url.searchParams.set("prefix", prefix);
  if (sessionId) url.searchParams.set("session_id", sessionId);
  const r = await fetch(url);
  return r.json();
}
