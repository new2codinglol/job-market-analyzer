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
import { getTopSkills } from "./client";

export default function App() {
  const [skills, setSkills] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getTopSkills(10).then(setSkills).catch((e) => setError(e.message));
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <h1 className="text-2xl font-bold text-slate-900 mb-6">
        Job Market Analyzer — Top Skills
      </h1>
      {error && <p className="text-red-600">{error}</p>}
      {!error && skills.length === 0 && (
        <p className="text-slate-500">No data yet — run fetch_seed.py to populate seed_jobs.json.</p>
      )}
      {skills.length > 0 && (
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={skills}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="skill" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#2563eb" />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
