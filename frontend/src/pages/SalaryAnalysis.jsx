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
import { getSalarySummary, getSalaryDistribution } from "../client";

function StatCard({ label, value }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm px-6 py-5">
      <div className="text-sm text-slate-500">{label}</div>
      <div className="text-2xl font-semibold text-slate-900 mt-1">{value}</div>
    </div>
  );
}

export default function SalaryAnalysis() {
  const [summary, setSummary] = useState(null);
  const [distribution, setDistribution] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([getSalarySummary(), getSalaryDistribution()])
      .then(([s, d]) => {
        setSummary(s);
        setDistribution(d);
      })
      .catch((e) => setError(e.message));
  }, []);

  const fmt = (n) => (n == null ? "—" : `S$${n.toLocaleString()}`);

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900 mb-1">Salary Analysis</h1>
      <p className="text-sm text-slate-500 mb-6">
        Singapore market only (Adzuna, SGD) — the one currency this dataset has enough salaried listings for.
      </p>

      {error && <p className="text-red-600">{error}</p>}

      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          <StatCard label="Jobs with salary data" value={summary.count} />
          <StatCard label="Average" value={fmt(summary.avg)} />
          <StatCard label="Minimum" value={fmt(summary.min)} />
          <StatCard label="Maximum" value={fmt(summary.max)} />
        </div>
      )}

      {distribution.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
          <h2 className="text-sm font-semibold text-slate-700 mb-4">Salary distribution (annual SGD)</h2>
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={distribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="range" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" fill="#4f46e5" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
