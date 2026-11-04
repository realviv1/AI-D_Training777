import { NavLink } from "react-router-dom";

export default function Navbar({ registrationCount }) {
  return (
    <header className="site-header">
      <div className="nav-inner">
        <NavLink to="/" className="brand" aria-label="Gather home">
          <span className="brand-mark">G</span>
          <span>gather<span className="brand-dot">.</span></span>
        </NavLink>

        <nav className="nav-links" aria-label="Main navigation">
          <NavLink to="/" end className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            Events
          </NavLink>
          <NavLink to="/registrations" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            Registrations
            <span className="nav-count">{registrationCount}</span>
          </NavLink>
        </nav>
      </div>
    </header>
  );
}