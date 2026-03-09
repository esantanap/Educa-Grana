import { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import './Navbar.css';

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => setMenuOpen((prev) => !prev);
  const closeMenu = () => setMenuOpen(false);

  return (
    <header className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand" onClick={closeMenu}>
          <span className="navbar-logo">💰</span>
          <span className="navbar-title">Educa-Grana</span>
        </Link>

        <button
          className="navbar-toggle"
          aria-label="Abrir menu de navegação"
          aria-expanded={menuOpen}
          onClick={toggleMenu}
        >
          <span className={`hamburger ${menuOpen ? 'open' : ''}`}></span>
        </button>

        <nav className={`navbar-nav ${menuOpen ? 'open' : ''}`} aria-label="Navegação principal">
          <NavLink to="/" end onClick={closeMenu} className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Início
          </NavLink>
          <NavLink to="/educacao-financeira" onClick={closeMenu} className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Educação Financeira
          </NavLink>
          <NavLink to="/programas-assistencia" onClick={closeMenu} className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Programas Sociais
          </NavLink>
          <NavLink to="/calculadora" onClick={closeMenu} className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Calculadora
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
