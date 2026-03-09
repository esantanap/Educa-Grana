import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import EducacaoFinanceira from './pages/EducacaoFinanceira';
import ProgramasAssistencia from './pages/ProgramasAssistencia';
import Calculadora from './pages/Calculadora';
import Orcamento from './pages/modules/Orcamento';
import Poupanca from './pages/modules/Poupanca';
import Credito from './pages/modules/Credito';
import Reserva from './pages/modules/Reserva';

function NotFound() {
  return (
    <div style={{ textAlign: 'center', padding: '4rem 1rem' }}>
      <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🔍</div>
      <h1 style={{ marginBottom: '0.5rem' }}>Página não encontrada</h1>
      <p style={{ color: 'var(--color-text-secondary)', marginBottom: '1.5rem' }}>
        A página que você procura não existe.
      </p>
      <a href="/" className="btn btn-primary">Ir para o início</a>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Navbar />
        <main style={{ flex: 1 }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/educacao-financeira" element={<EducacaoFinanceira />} />
            <Route path="/educacao-financeira/orcamento" element={<Orcamento />} />
            <Route path="/educacao-financeira/poupanca" element={<Poupanca />} />
            <Route path="/educacao-financeira/credito" element={<Credito />} />
            <Route path="/educacao-financeira/reserva" element={<Reserva />} />
            <Route path="/programas-assistencia" element={<ProgramasAssistencia />} />
            <Route path="/calculadora" element={<Calculadora />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}
