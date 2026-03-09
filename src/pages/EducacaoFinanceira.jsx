import { Link } from 'react-router-dom';
import './EducacaoFinanceira.css';

const modules = [
  {
    icon: '💵',
    title: 'Orçamento Pessoal',
    description: 'Aprenda a registrar suas receitas e despesas e criar um orçamento que funcione para você.',
    level: 'Iniciante',
    time: '15 min',
    link: '/educacao-financeira/orcamento',
    color: '#e8f5e9',
  },
  {
    icon: '🐷',
    title: 'Como Poupar',
    description: 'Estratégias práticas para começar a poupar mesmo com renda baixa e alcançar seus objetivos.',
    level: 'Iniciante',
    time: '12 min',
    link: '/educacao-financeira/poupanca',
    color: '#fff8e1',
  },
  {
    icon: '💳',
    title: 'Crédito Consciente',
    description: 'Entenda como funcionam cartão de crédito, cheque especial e empréstimos — e como evitar dívidas.',
    level: 'Intermediário',
    time: '20 min',
    link: '/educacao-financeira/credito',
    color: '#fce4ec',
  },
  {
    icon: '🆘',
    title: 'Reserva de Emergência',
    description: 'Por que e como construir uma reserva para imprevistos sem comprometer o orçamento do mês.',
    level: 'Iniciante',
    time: '10 min',
    link: '/educacao-financeira/reserva',
    color: '#e3f2fd',
  },
];

const levelColor = {
  Iniciante: 'badge-success',
  Intermediário: 'badge-warning',
  Avançado: 'badge-info',
};

export default function EducacaoFinanceira() {
  return (
    <div>
      <div className="page-header">
        <h1>📚 Educação Financeira</h1>
        <p>
          Conteúdos práticos e acessíveis para ajudar você a tomar o controle das suas finanças.
          Escolha um módulo e comece agora!
        </p>
      </div>

      <div className="section container">
        <div className="ef-intro">
          <div className="tip-box">
            <p className="tip-title">💡 Por que aprender sobre finanças?</p>
            <p>
              Entender como funciona o dinheiro é essencial para sair das dívidas, alcançar objetivos
              e ter segurança para enfrentar imprevistos. Você não precisa ganhar muito para ter
              uma vida financeira saudável — o segredo está na organização.
            </p>
          </div>
        </div>

        <h2 className="section-title" style={{ marginTop: '2rem' }}>Módulos de aprendizado</h2>
        <p className="section-subtitle">
          Todos os módulos são gratuitos e elaborados para quem está começando do zero.
        </p>

        <div className="ef-modules-grid">
          {modules.map((m) => (
            <Link
              to={m.link}
              key={m.title}
              className="ef-module-card"
              style={{ '--card-bg': m.color }}
            >
              <div className="ef-module-header">
                <span className="ef-module-icon">{m.icon}</span>
                <div className="ef-module-meta">
                  <span className={`badge ${levelColor[m.level]}`}>{m.level}</span>
                  <span className="ef-module-time">⏱ {m.time}</span>
                </div>
              </div>
              <h3>{m.title}</h3>
              <p>{m.description}</p>
              <span className="ef-module-cta">Ler conteúdo →</span>
            </Link>
          ))}
        </div>

        {/* Quick Tips Section */}
        <div className="ef-tips">
          <h2 className="section-title" style={{ marginTop: '3rem' }}>Dicas rápidas de finanças</h2>
          <div className="ef-tips-grid">
            <div className="ef-tip">
              <span>🎯</span>
              <div>
                <strong>Regra 50-30-20</strong>
                <p>Destine 50% da renda para necessidades, 30% para desejos e 20% para poupança e dívidas.</p>
              </div>
            </div>
            <div className="ef-tip">
              <span>📝</span>
              <div>
                <strong>Anote tudo</strong>
                <p>Registrar todos os gastos — até os pequenos — revela onde o dinheiro realmente vai.</p>
              </div>
            </div>
            <div className="ef-tip">
              <span>🚫</span>
              <div>
                <strong>Evite compras por impulso</strong>
                <p>Antes de comprar, espere 24 horas e pergunte: "Eu realmente preciso disso?"</p>
              </div>
            </div>
            <div className="ef-tip">
              <span>🔄</span>
              <div>
                <strong>Pague-se primeiro</strong>
                <p>Assim que receber seu salário, já separe o valor da poupança antes de gastar.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
