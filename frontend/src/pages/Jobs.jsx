import { useEffect, useState } from "react";
import { getJobs, getSkillsList, getLocations } from "../client";

const SOURCE_STYLES = {
  adzuna: "bg-blue-50 text-blue-700",
  remoteok: "bg-emerald-50 text-emerald-700",
  weworkremotely: "bg-violet-50 text-violet-700",
};

function formatSalary(job) {
  if (!job.salary_min && !job.salary_max) return null;
  const lo = job.salary_min?.toLocaleString();
  const hi = job.salary_max?.toLocaleString();
  if (lo && hi && lo !== hi) return `${lo} – ${hi}`;
  return lo || hi;
}

export default function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [skills, setSkills] = useState([]);
  const [locations, setLocations] = useState([]);
  const [location, setLocation] = useState("");
  const [skill, setSkill] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    getSkillsList().then(setSkills).catch(() => {});
    getLocations().then(setLocations).catch(() => {});
  }, []);

  useEffect(() => {
    getJobs({ location, skill }).then(setJobs).catch((e) => setError(e.message));
  }, [location, skill]);

  const selectClass =
    "border border-slate-200 rounded-lg px-3 py-2 text-sm bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-200 focus:border-indigo-400";

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900 mb-6">Jobs</h1>

      <div className="flex flex-wrap gap-3 mb-6">
        <select value={location} onChange={(e) => setLocation(e.target.value)} className={selectClass}>
          <option value="">All locations</option>
          {locations.map((l) => (
            <option key={l} value={l}>{l}</option>
          ))}
        </select>
        <select value={skill} onChange={(e) => setSkill(e.target.value)} className={selectClass}>
          <option value="">All skills</option>
          {skills.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      {error && <p className="text-red-600">{error}</p>}
      <p className="text-slate-500 text-sm mb-3">{jobs.length} jobs</p>

      <div className="grid gap-3">
        {jobs.map((job) => {
          const salary = formatSalary(job);
          return (
            <a
              key={job.id}
              href={job.redirect_url}
              target="_blank"
              rel="noreferrer"
              className="block bg-white border border-slate-200 rounded-xl p-4 shadow-sm hover:shadow-md hover:border-indigo-200 transition-all"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="font-semibold text-slate-900">{job.title}</div>
                  <div className="text-sm text-slate-600 mt-0.5">{job.company} — {job.location}</div>
                </div>
                <span className={`text-xs font-medium px-2 py-1 rounded-full whitespace-nowrap ${SOURCE_STYLES[job.source] || "bg-slate-100 text-slate-600"}`}>
                  {job.source}
                </span>
              </div>
              {salary && (
                <div className="text-sm text-emerald-700 font-medium mt-2">{salary}</div>
              )}
            </a>
          );
        })}
      </div>
    </div>
  );
}
