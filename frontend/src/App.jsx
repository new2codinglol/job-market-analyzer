import { NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Jobs from "./pages/Jobs";

const navLinkClass = ({ isActive }) =>
  `px-3 py-2 text-sm font-medium rounded ${isActive ? "bg-blue-600 text-white" : "text-slate-700 hover:bg-slate-100"}`;

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="bg-white border-b border-slate-200 px-8 py-4 flex items-center gap-2">
        <span className="font-bold text-slate-900 mr-4">Job Market Analyzer</span>
        <NavLink to="/" end className={navLinkClass}>Dashboard</NavLink>
        <NavLink to="/jobs" className={navLinkClass}>Jobs</NavLink>
      </nav>
      <div className="p-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/jobs" element={<Jobs />} />
        </Routes>
      </div>
    </div>
  );
}
