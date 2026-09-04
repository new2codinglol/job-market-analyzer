import { useEffect, useState } from "react";
import { getJobs, getSkillsList } from "../client";

export default function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [skills, setSkills] = useState([]);
  const [location, setLocation] = useState("");
  const [skill, setSkill] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    getSkillsList().then(setSkills).catch(() => {});
  }, []);

  useEffect(() => {
    getJobs({ location, skill }).then(setJobs).catch((e) => setError(e.message));
  }, [location, skill]);

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900 mb-6">Jobs</h1>

      <div className="flex gap-4 mb-6">
        <input
          type="text"
          placeholder="Filter by location..."
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="border border-slate-300 rounded px-3 py-2 text-sm"
        />
        <select
          value={skill}
          onChange={(e) => setSkill(e.target.value)}
          className="border border-slate-300 rounded px-3 py-2 text-sm"
        >
          <option value="">All skills</option>
          {skills.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      {error && <p className="text-red-600">{error}</p>}
      <p className="text-slate-500 text-sm mb-2">{jobs.length} jobs</p>

      <div className="space-y-3">
        {jobs.map((job) => (
          <a
            key={job.id}
            href={job.redirect_url}
            target="_blank"
            rel="noreferrer"
            className="block border border-slate-200 rounded p-4 hover:bg-slate-50"
          >
            <div className="font-semibold text-slate-900">{job.title}</div>
            <div className="text-sm text-slate-600">{job.company} — {job.location}</div>
          </a>
        ))}
      </div>
    </div>
  );
}
