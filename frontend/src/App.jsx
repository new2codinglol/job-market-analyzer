import { NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Jobs from "./pages/Jobs";
import SalaryAnalysis from "./pages/SalaryAnalysis";

const navLinkClass = ({ isActive }) =>
  `px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
    isActive ? "bg-indigo-600 text-white shadow-sm" : "text-slate-600 hover:bg-slate-100"
  }`;

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="bg-white/80 backdrop-blur border-b border-slate-200 px-4 sm:px-8 py-3 sm:py-4 flex flex-wrap items-center gap-2 sticky top-0 z-10">
        <span className="font-bold text-slate-900 mr-4 tracking-tight whitespace-nowrap w-full sm:w-auto mb-1 sm:mb-0">Job Market Analyzer</span>
        <NavLink to="/" end className={navLinkClass}>Dashboard</NavLink>
        <NavLink to="/jobs" className={navLinkClass}>Jobs</NavLink>
        <NavLink to="/salary" className={navLinkClass}>Salary</NavLink>
      </nav>
      <div className="p-4 sm:p-8 max-w-5xl mx-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/salary" element={<SalaryAnalysis />} />
        </Routes>
      </div>
      <footer className="px-4 sm:px-8 py-4 text-sm text-slate-500 max-w-5xl mx-auto">
        Job data from Adzuna,{" "}
        <a href="https://remoteok.com" className="underline hover:text-slate-700">Remote OK</a>, and{" "}
        <a href="https://weworkremotely.com" className="underline hover:text-slate-700">We Work Remotely</a>.
      </footer>
    </div>
  );
}
