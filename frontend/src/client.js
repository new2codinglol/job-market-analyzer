const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getTopSkills(n = 10) {
  const res = await fetch(`${API_URL}/api/skills/top?n=${n}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
