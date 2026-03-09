import { Link } from 'react-router-dom';
import './Module.css';

export default function Poupanca() {
  return (
    <div>
      <div className="page-header">
        <h1>🐷 Como Poupar</h1>
        <p>Estratégias simples para guardar dinheiro mesmo com renda limitada e construir um futuro mais seguro.</p>
      </div>

      <div className="module-container container">
        <nav className="module-breadcrumb" aria-label="Caminho de navegação">
          <Link to="/educacao-financeira">Educação Financeira</Link>
          <span>›</span>
          <span>Como Poupar</span>
        </nav>

        <section className="module-section">
          <h2>Poupar com pouco dinheiro — é possível?</h2>
          <p>
            Muita gente acha que só é possível poupar quando se ganha muito. Mas a verdade é que
            <strong> o hábito de poupar é mais importante do que o valor poupado</strong>. Começar
            com R$ 10, R$ 20 por mês já faz diferença.
          </p>
          <p>
            Poupar não é luxo — é uma necessidade. Quem não poupa fica vulnerável a qualquer
            imprevisto: uma conta de saúde, um conserto, uma demissão.
          </p>
        </section>

        <section className="module-section">
          <h2>Estratégias para quem ganha pouco</h2>
          <div className="strategy-cards">
            {[
              {
                icon: '🥇',
                title: 'Pague-se primeiro',
                desc: 'Assim que receber seu salário ou benefício, separe logo o valor para poupança — mesmo que seja R$ 20. Não espere sobrar dinheiro, porque raramente sobra.',
              },
              {
                icon: '🪣',
                title: 'O método dos potes',
                desc: 'Divida sua renda em categorias (alimentação, transporte, lazer, poupança) e só gaste o que está no pote de cada categoria. Pode ser em envelopes físicos ou contas separadas.',
              },
              {
                icon: '📅',
                title: 'Desafio dos 52 envelopes',
                desc: 'Poupe R$ 1 na semana 1, R$ 2 na semana 2... até R$ 52 na semana 52. No final do ano, você terá R$ 1.378 guardados!',
              },
              {
                icon: '🔄',
                title: 'Automatize a poupança',
                desc: 'Configure transferência automática para a poupança logo no dia do pagamento. O que os olhos não veem, a mão não gasta.',
              },
            ].map((s) => (
              <div className="strategy-card" key={s.title}>
                <span className="strategy-icon">{s.icon}</span>
                <div>
                  <strong>{s.title}</strong>
                  <p>{s.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <div className="tip-box">
          <p className="tip-title">💡 Poupança vs. Conta corrente</p>
          <p>
            Guarde a poupança em uma conta separada da conta corrente — de preferência em um banco
            diferente. Isso dificulta o resgate por impulso e mantém o dinheiro mais seguro.
          </p>
        </div>

        <section className="module-section">
          <h2>Onde guardar meu dinheiro?</h2>
          <div className="grid-2" style={{ marginTop: '1rem' }}>
            {[
              {
                title: '🏦 Poupança',
                pros: ['Segura (garantida pelo FGC)', 'Sem taxas', 'Fácil de abrir'],
                cons: ['Rentabilidade baixa'],
              },
              {
                title: '📱 Conta digital com rendimento',
                pros: ['Rende 100% do CDI ou mais', 'Sem tarifas', 'Acesso fácil'],
                cons: ['Requer celular e internet'],
              },
            ].map((opt) => (
              <div className="card" key={opt.title}>
                <h3 style={{ marginBottom: '0.75rem' }}>{opt.title}</h3>
                <ul className="pros-list">
                  {opt.pros.map((p) => <li key={p}>✅ {p}</li>)}
                  {opt.cons.map((c) => <li key={c} style={{ color: 'var(--color-error)' }}>⚠️ {c}</li>)}
                </ul>
              </div>
            ))}
          </div>
        </section>

        <section className="module-section">
          <h2>Pequenas mudanças, grandes resultados</h2>
          <p>Pequenos cortes no dia a dia podem gerar uma poupança significativa no ano:</p>
          <div className="savings-table">
            <div className="savings-row header">
              <span>Economia</span>
              <span>Por mês</span>
              <span>Por ano</span>
            </div>
            {[
              { action: 'Levar almoço de casa 3x/semana', month: 'R$ 90', year: 'R$ 1.080' },
              { action: 'Cancelar 1 assinatura não usada', month: 'R$ 30', year: 'R$ 360' },
              { action: 'Reduzir gastos com deliveries', month: 'R$ 120', year: 'R$ 1.440' },
              { action: 'Comprar na feira ao invés de supermercado', month: 'R$ 80', year: 'R$ 960' },
            ].map((row) => (
              <div className="savings-row" key={row.action}>
                <span>{row.action}</span>
                <span>{row.month}</span>
                <span>{row.year}</span>
              </div>
            ))}
          </div>
        </section>

        <div className="module-nav">
          <Link to="/educacao-financeira/orcamento" className="btn btn-outline">← Orçamento Pessoal</Link>
          <Link to="/educacao-financeira/credito" className="btn btn-primary">Próximo: Crédito →</Link>
        </div>
      </div>
    </div>
  );
}
