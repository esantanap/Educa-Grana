import { Link } from 'react-router-dom';
import './Module.css';

export default function Orcamento() {
  return (
    <div>
      <div className="page-header">
        <h1>💵 Orçamento Pessoal</h1>
        <p>Aprenda a controlar suas receitas e despesas e criar um plano financeiro que funcione para você.</p>
      </div>

      <div className="module-container container">
        <nav className="module-breadcrumb" aria-label="Caminho de navegação">
          <Link to="/educacao-financeira">Educação Financeira</Link>
          <span>›</span>
          <span>Orçamento Pessoal</span>
        </nav>

        <section className="module-section">
          <h2>O que é orçamento pessoal?</h2>
          <p>
            Orçamento pessoal é um plano que organiza quanto dinheiro você recebe e quanto você gasta
            em um determinado período (geralmente um mês). É como um mapa do seu dinheiro — sem ele,
            é fácil se perder.
          </p>
          <p>
            Fazer um orçamento não significa deixar de gastar com o que você gosta. Significa saber
            <strong> para onde seu dinheiro vai</strong> e ter controle sobre isso.
          </p>
        </section>

        <section className="module-section">
          <h2>Como montar seu orçamento em 4 passos</h2>
          <ol className="module-steps">
            <li>
              <div className="step-number">1</div>
              <div>
                <strong>Liste todas as suas receitas</strong>
                <p>Salário, bicos, benefícios, pensão alimentícia, aluguéis... Inclua tudo que entra no mês.</p>
              </div>
            </li>
            <li>
              <div className="step-number">2</div>
              <div>
                <strong>Liste todas as suas despesas</strong>
                <p>Aluguel, luz, água, alimentação, transporte, celular, remédios, escola dos filhos...</p>
              </div>
            </li>
            <li>
              <div className="step-number">3</div>
              <div>
                <strong>Calcule a diferença</strong>
                <p>Receitas − Despesas = Saldo. Se o resultado for positivo, você tem margem para poupar.</p>
              </div>
            </li>
            <li>
              <div className="step-number">4</div>
              <div>
                <strong>Ajuste e acompanhe</strong>
                <p>Revise seu orçamento mensalmente. Corte gastos supérfluos e direcione para poupança.</p>
              </div>
            </li>
          </ol>
        </section>

        <div className="tip-box">
          <p className="tip-title">💡 Dica: A Regra 50-30-20</p>
          <p>
            Divida sua renda em três partes: <strong>50%</strong> para necessidades (aluguel, comida,
            contas), <strong>30%</strong> para desejos (lazer, roupas extras) e <strong>20%</strong>
            &nbsp;para poupança e pagamento de dívidas.
          </p>
        </div>

        <section className="module-section">
          <h2>Categorias de despesas mais comuns</h2>
          <div className="expense-categories">
            {[
              { icon: '🏠', label: 'Moradia', examples: 'Aluguel, condomínio, IPTU' },
              { icon: '🍽️', label: 'Alimentação', examples: 'Supermercado, feira, refeições' },
              { icon: '🚌', label: 'Transporte', examples: 'Ônibus, combustível, manutenção' },
              { icon: '💡', label: 'Contas fixas', examples: 'Luz, água, gás, internet, celular' },
              { icon: '💊', label: 'Saúde', examples: 'Remédios, consultas, plano de saúde' },
              { icon: '🎓', label: 'Educação', examples: 'Escola, cursos, material escolar' },
              { icon: '👕', label: 'Vestuário', examples: 'Roupas, calçados' },
              { icon: '🎭', label: 'Lazer', examples: 'Passeios, assinaturas, hobbies' },
            ].map((cat) => (
              <div className="expense-cat-card" key={cat.label}>
                <span>{cat.icon}</span>
                <div>
                  <strong>{cat.label}</strong>
                  <p>{cat.examples}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <div className="info-box">
          <strong>📱 Ferramenta gratuita:</strong> Use nossa{' '}
          <Link to="/calculadora" style={{ color: 'var(--color-info)', fontWeight: 600 }}>
            Calculadora de Orçamento
          </Link>{' '}
          para montar o seu orçamento agora mesmo, direto no celular.
        </div>

        <section className="module-section">
          <h2>Por que a maioria das pessoas não faz orçamento?</h2>
          <p>Muita gente evita fazer orçamento porque tem medo de descobrir que está gastando mais do que deveria. Mas é exatamente por isso que o orçamento é importante:</p>
          <ul className="module-list">
            <li>✅ Você para de se surpreender quando o dinheiro acaba</li>
            <li>✅ Consegue identificar onde cortar gastos</li>
            <li>✅ Toma decisões mais conscientes antes de comprar algo</li>
            <li>✅ Fica mais tranquilo sobre o futuro financeiro</li>
          </ul>
        </section>

        <div className="module-nav">
          <Link to="/educacao-financeira" className="btn btn-outline">← Voltar aos módulos</Link>
          <Link to="/educacao-financeira/poupanca" className="btn btn-primary">Próximo: Como Poupar →</Link>
        </div>
      </div>
    </div>
  );
}
