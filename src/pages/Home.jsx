import { Link } from 'react-router-dom';
import './Home.css';

const features = [
  {
    icon: '📚',
    title: 'Educação Financeira',
    description: 'Aprenda a controlar seu dinheiro, criar um orçamento, poupar e entender crédito de forma simples e prática.',
    link: '/educacao-financeira',
    color: '#e8f5e9',
  },
  {
    icon: '🏛️',
    title: 'Programas Sociais',
    description: 'Conheça os principais programas de assistência social do governo federal que podem ajudar você e sua família.',
    link: '/programas-assistencia',
    color: '#e3f2fd',
  },
  {
    icon: '🧮',
    title: 'Calculadora de Orçamento',
    description: 'Use nossa calculadora interativa para planejar suas receitas, despesas e descobrir quanto você pode poupar.',
    link: '/calculadora',
    color: '#fff8e1',
  },
];

const topics = [
  { icon: '💵', label: 'Orçamento Pessoal', link: '/educacao-financeira/orcamento' },
  { icon: '🐷', label: 'Como Poupar', link: '/educacao-financeira/poupanca' },
  { icon: '💳', label: 'Crédito Consciente', link: '/educacao-financeira/credito' },
  { icon: '🆘', label: 'Reserva de Emergência', link: '/educacao-financeira/reserva' },
];

const stats = [
  { value: '70%', label: 'dos brasileiros não têm reserva de emergência' },
  { value: '45%', label: 'das famílias estão endividadas' },
  { value: '30M+', label: 'famílias recebem algum benefício social' },
];

export default function Home() {
  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content container">
          <div className="hero-text">
            <span className="hero-badge">🌱 Educação Financeira Gratuita</span>
            <h1>
              Aprenda a cuidar do seu dinheiro e conhecer seus direitos
            </h1>
            <p>
              O Educa-Grana oferece conteúdo gratuito sobre finanças pessoais e informações sobre
              programas de assistência social para ajudar famílias de baixa renda a alcançar
              estabilidade financeira.
            </p>
            <div className="hero-buttons">
              <Link to="/educacao-financeira" className="btn btn-secondary">
                Começar a aprender
              </Link>
              <Link to="/programas-assistencia" className="btn btn-outline-white">
                Ver programas sociais
              </Link>
            </div>
          </div>
          <div className="hero-illustration" aria-hidden="true">
            <div className="hero-card-float">
              <span>💰</span>
              <div>
                <strong>Meta de poupança</strong>
                <p>R$ 500 / mês</p>
              </div>
            </div>
            <div className="hero-emoji-main">🏠</div>
            <div className="hero-card-float hero-card-right">
              <span>📈</span>
              <div>
                <strong>Controle financeiro</strong>
                <p>Receitas &gt; Despesas</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Strip */}
      <section className="stats-strip">
        <div className="container stats-grid">
          {stats.map((stat) => (
            <div key={stat.value} className="stat-item">
              <span className="stat-value">{stat.value}</span>
              <span className="stat-label">{stat.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="section container">
        <h2 className="section-title">O que você encontra aqui</h2>
        <p className="section-subtitle">
          Ferramentas e informações para transformar sua relação com o dinheiro
        </p>
        <div className="features-grid">
          {features.map((f) => (
            <Link to={f.link} key={f.title} className="feature-card" style={{ '--card-bg': f.color }}>
              <div className="feature-icon">{f.icon}</div>
              <h3>{f.title}</h3>
              <p>{f.description}</p>
              <span className="feature-link">Acessar →</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Topics Quick Access */}
      <section className="topics-section">
        <div className="container">
          <h2 className="section-title">Temas em destaque</h2>
          <p className="section-subtitle">Acesse diretamente os conteúdos mais buscados</p>
          <div className="topics-grid">
            {topics.map((t) => (
              <Link to={t.link} key={t.label} className="topic-chip">
                <span className="topic-icon">{t.icon}</span>
                <span>{t.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section container">
        <div className="cta-box">
          <div className="cta-text">
            <h2>Você pode ter direito a benefícios sociais</h2>
            <p>
              Saiba quais programas do governo federal podem ajudar você e sua família.
              Conheça os critérios de elegibilidade e como se inscrever.
            </p>
          </div>
          <Link to="/programas-assistencia" className="btn btn-secondary">
            Conhecer programas sociais
          </Link>
        </div>
      </section>
    </div>
  );
}
