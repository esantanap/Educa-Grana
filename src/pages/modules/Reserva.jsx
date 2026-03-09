import { Link } from 'react-router-dom';
import './Module.css';

export default function Reserva() {
  return (
    <div>
      <div className="page-header">
        <h1>🆘 Reserva de Emergência</h1>
        <p>Construa uma rede de proteção financeira para enfrentar imprevistos sem precisar se endividar.</p>
      </div>

      <div className="module-container container">
        <nav className="module-breadcrumb" aria-label="Caminho de navegação">
          <Link to="/educacao-financeira">Educação Financeira</Link>
          <span>›</span>
          <span>Reserva de Emergência</span>
        </nav>

        <section className="module-section">
          <h2>O que é reserva de emergência?</h2>
          <p>
            Reserva de emergência é um dinheiro guardado especificamente para situações inesperadas:
            uma doença, demissão, conserto urgente ou outro imprevisto. É o <strong>colchão financeiro</strong>
            &nbsp;que evita que você precise pegar empréstimo ou usar o cartão de crédito em momentos difíceis.
          </p>
        </section>

        <div className="info-box">
          <strong>📊 Dado preocupante:</strong> Aproximadamente 70% dos brasileiros não têm uma reserva
          de emergência. Isso significa que qualquer imprevisto pode levar a dívidas.
        </div>

        <section className="module-section">
          <h2>Quanto devo guardar?</h2>
          <p>A regra geral é ter entre <strong>3 e 6 meses</strong> de despesas mensais guardadas:</p>
          <div className="reserve-table">
            <div className="reserve-row header">
              <span>Situação</span>
              <span>Meta recomendada</span>
              <span>Exemplo (gasto R$ 2.000/mês)</span>
            </div>
            {[
              { situation: 'Emprego estável (CLT)', meta: '3 meses', example: 'R$ 6.000' },
              { situation: 'Autônomo / Freelancer', meta: '6 meses', example: 'R$ 12.000' },
              { situation: 'Família com crianças', meta: '6 meses', example: 'R$ 12.000' },
            ].map((row) => (
              <div className="reserve-row" key={row.situation}>
                <span>{row.situation}</span>
                <span>{row.meta}</span>
                <span>{row.example}</span>
              </div>
            ))}
          </div>
          <p style={{ marginTop: '0.75rem', fontSize: '0.9rem', color: 'var(--color-text-secondary)' }}>
            * Se você recebe Bolsa Família ou BPC, inclua esses valores no cálculo da sua renda mensal.
          </p>
        </section>

        <section className="module-section">
          <h2>Como construir a reserva do zero</h2>
          <ol className="module-steps">
            <li>
              <div className="step-number">1</div>
              <div>
                <strong>Defina um valor inicial pequeno</strong>
                <p>Comece com a meta de guardar R$ 500 ou 1 mês de despesas. Pequenas metas são mais fáceis de alcançar.</p>
              </div>
            </li>
            <li>
              <div className="step-number">2</div>
              <div>
                <strong>Separe o dinheiro toda vez que receber</strong>
                <p>Mesmo que seja R$ 30 por mês. O hábito é mais importante que o valor inicial.</p>
              </div>
            </li>
            <li>
              <div className="step-number">3</div>
              <div>
                <strong>Guarde em conta separada</strong>
                <p>A reserva não deve ficar misturada com o dinheiro do dia a dia. Use uma conta poupança ou digital.</p>
              </div>
            </li>
            <li>
              <div className="step-number">4</div>
              <div>
                <strong>Não toque, exceto em emergências reais</strong>
                <p>Viagem, roupas, eletrônicos — não são emergências. Promoção tentadora também não é emergência.</p>
              </div>
            </li>
          </ol>
        </section>

        <div className="tip-box">
          <p className="tip-title">💡 O que conta como emergência?</p>
          <ul className="module-list" style={{ marginTop: '0.5rem' }}>
            <li>✅ Consulta médica ou remédio urgente</li>
            <li>✅ Conserto de item essencial (geladeira, carro para trabalho)</li>
            <li>✅ Perda de emprego / renda</li>
            <li>✅ Emergência familiar inesperada</li>
            <li>❌ Compra em promoção</li>
            <li>❌ Viagem de lazer</li>
            <li>❌ Presentão de aniversário</li>
          </ul>
        </div>

        <section className="module-section">
          <h2>Onde guardar a reserva?</h2>
          <p>A reserva de emergência precisa ser:</p>
          <ul className="module-list">
            <li>✅ <strong>Segura</strong> — sem risco de perder o dinheiro</li>
            <li>✅ <strong>Líquida</strong> — você precisa conseguir sacar quando precisar</li>
            <li>✅ <strong>Rendendo</strong> — pelo menos acima da inflação</li>
          </ul>
          <p style={{ marginTop: '0.75rem' }}>
            Boas opções: <strong>Poupança</strong>, <strong>CDB com liquidez diária</strong> ou
            <strong> conta digital que rende 100% do CDI</strong> (como Nubank, Inter, C6 Bank).
          </p>
        </section>

        <div className="module-nav">
          <Link to="/educacao-financeira/credito" className="btn btn-outline">← Crédito Consciente</Link>
          <Link to="/calculadora" className="btn btn-primary">Usar a Calculadora →</Link>
        </div>
      </div>
    </div>
  );
}
