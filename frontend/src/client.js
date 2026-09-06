const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getTopSkills(n = 10) {
  const res = await fetch(`${API_URL}/api/skills/top?n=${n}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getSkillsList() {
  const res = await fetch(`${API_URL}/api/skills/list`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getJobs({ location = "", skill = "" } = {}) {
  const params = new URLSearchParams();
  if (location) params.set("location", location);
  if (skill) params.set("skill", skill);
  const res = await fetch(`${API_URL}/api/jobs?${params}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getLocations() {
  const res = await fetch(`${API_URL}/api/locations`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getSalarySummary() {
  const res = await fetch(`${API_URL}/api/salary/summary`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getSalaryDistribution() {
  const res = await fetch(`${API_URL}/api/salary/distribution`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
