import { Link } from 'react-router-dom';
import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container container">
        <div className="footer-brand">
          <span className="footer-logo">💰</span>
          <span className="footer-title">Educa-Grana</span>
          <p className="footer-desc">
            Educação financeira acessível para comunidades de baixa renda.
          </p>
        </div>

        <div className="footer-links">
          <h3>Navegação</h3>
          <ul>
            <li><Link to="/">Início</Link></li>
            <li><Link to="/educacao-financeira">Educação Financeira</Link></li>
            <li><Link to="/programas-assistencia">Programas Sociais</Link></li>
            <li><Link to="/calculadora">Calculadora de Orçamento</Link></li>
          </ul>
        </div>

        <div className="footer-links">
          <h3>Temas</h3>
          <ul>
            <li><Link to="/educacao-financeira/orcamento">Orçamento Pessoal</Link></li>
            <li><Link to="/educacao-financeira/poupanca">Como Poupar</Link></li>
            <li><Link to="/educacao-financeira/credito">Crédito Consciente</Link></li>
            <li><Link to="/educacao-financeira/reserva">Reserva de Emergência</Link></li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <p>© 2024 Educa-Grana · Projeto Extensionista Uninter · Desenvolvido para comunidades de baixa renda</p>
      </div>
    </footer>
  );
}
