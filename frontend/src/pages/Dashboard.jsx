import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { getTopSkills } from "../client";

export default function Dashboard() {
  const [skills, setSkills] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getTopSkills(10).then(setSkills).catch((e) => setError(e.message));
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900 mb-1">Top Skills</h1>
      <p className="text-sm text-slate-500 mb-6">Most-mentioned skills across all scraped job postings.</p>
      {error && <p className="text-red-600">{error}</p>}
      {!error && skills.length === 0 && (
        <p className="text-slate-500">No data yet — run fetch_seed.py to populate seed_jobs.json.</p>
      )}
      {skills.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={skills}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="skill" tick={{ fill: "#475569", fontSize: 12 }} />
              <YAxis tick={{ fill: "#475569", fontSize: 12 }} allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" fill="#4f46e5" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
