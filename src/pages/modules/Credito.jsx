import { Link } from 'react-router-dom';
import './Module.css';

export default function Credito() {
  return (
    <div>
      <div className="page-header">
        <h1>💳 Crédito Consciente</h1>
        <p>Entenda como funcionam cartão de crédito, empréstimos e cheque especial — e como usá-los sem se endividar.</p>
      </div>

      <div className="module-container container">
        <nav className="module-breadcrumb" aria-label="Caminho de navegação">
          <Link to="/educacao-financeira">Educação Financeira</Link>
          <span>›</span>
          <span>Crédito Consciente</span>
        </nav>

        <section className="module-section">
          <h2>O que é crédito?</h2>
          <p>
            Crédito é a possibilidade de usar dinheiro que você ainda não tem para pagar depois.
            Pode ser útil para comprar algo necessário parcelado, mas também pode virar uma
            <strong> armadilha de dívidas</strong> se não for usado com cuidado.
          </p>
        </section>

        <div className="warning-box">
          <strong>⚠️ Atenção:</strong> O Brasil tem uma das maiores taxas de juros do mundo.
          O cartão de crédito rotativo pode cobrar mais de <strong>400% ao ano</strong>.
          Evite pagar o mínimo da fatura!
        </div>

        <section className="module-section">
          <h2>Tipos de crédito mais comuns</h2>
          <div className="credit-types">
            {[
              {
                icon: '💳',
                title: 'Cartão de crédito',
                risk: 'Alto risco',
                riskClass: 'badge-warning',
                desc: 'Permite comprar agora e pagar depois. Se a fatura não for paga integralmente até o vencimento, incide juros altíssimos (rotativo). Use com cuidado e SEMPRE pague o total da fatura.',
              },
              {
                icon: '🏦',
                title: 'Cheque especial',
                risk: 'Muito alto risco',
                riskClass: 'badge-warning',
                desc: 'Crédito automático vinculado à conta corrente. Tem juros altíssimos (acima de 100% ao ano em muitos bancos). Deve ser evitado ao máximo — use apenas em emergências e pague imediatamente.',
              },
              {
                icon: '📋',
                title: 'Empréstimo pessoal',
                risk: 'Risco médio',
                riskClass: 'badge-info',
                desc: 'Valor fixo emprestado pelo banco com parcelas mensais. Mais barato que o cheque especial, mas ainda tem juros relevantes. Compare as taxas antes de contratar.',
              },
              {
                icon: '📦',
                title: 'Crédito consignado',
                risk: 'Menor risco',
                riskClass: 'badge-success',
                desc: 'Desconto direto no salário ou benefício (como o INSS). Tem as menores taxas de juros entre os empréstimos. Mas cuidado: o desconto é automático e pode comprometer sua renda.',
              },
            ].map((type) => (
              <div className="credit-type-card" key={type.title}>
                <div className="credit-type-header">
                  <span>{type.icon}</span>
                  <h3>{type.title}</h3>
                  <span className={`badge ${type.riskClass}`}>{type.risk}</span>
                </div>
                <p>{type.desc}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="module-section">
          <h2>Regras de ouro para usar crédito</h2>
          <ul className="module-list">
            <li>✅ Nunca use crédito para pagar despesas do dia a dia (comida, contas)</li>
            <li>✅ Sempre pague o <strong>total</strong> da fatura do cartão — nunca o mínimo</li>
            <li>✅ Mantenha o limite do cartão em no máximo 30% da sua renda</li>
            <li>✅ Compare as taxas de juros antes de contratar qualquer empréstimo</li>
            <li>✅ Tenha sempre uma reserva de emergência para evitar recorrer a crédito</li>
            <li>❌ Não faça novas dívidas para pagar dívidas antigas (bola de neve)</li>
            <li>❌ Não acredite em promessas de crédito "fácil e sem consulta" de desconhecidos</li>
          </ul>
        </section>

        <section className="module-section">
          <h2>Como sair das dívidas</h2>
          <ol className="module-steps">
            <li>
              <div className="step-number">1</div>
              <div>
                <strong>Liste todas as suas dívidas</strong>
                <p>Valor total, taxa de juros e parcela mensal de cada dívida.</p>
              </div>
            </li>
            <li>
              <div className="step-number">2</div>
              <div>
                <strong>Priorize as de maior juros</strong>
                <p>Pague primeiro as dívidas mais caras (cartão de crédito, cheque especial).</p>
              </div>
            </li>
            <li>
              <div className="step-number">3</div>
              <div>
                <strong>Negocie com os credores</strong>
                <p>Bancos e empresas geralmente aceitam renegociar dívidas com desconto. Peça condições melhores.</p>
              </div>
            </li>
            <li>
              <div className="step-number">4</div>
              <div>
                <strong>Use o Desenrola Brasil</strong>
                <p>Programa do governo federal que permite renegociar dívidas com desconto de até 96%. Acesse pelo gov.br.</p>
              </div>
            </li>
          </ol>
        </section>

        <div className="tip-box">
          <p className="tip-title">💡 Consulte seu CPF gratuitamente</p>
          <p>
            Verifique se seu nome está negativado (SPC/Serasa) gratuitamente pelo site{' '}
            <strong>consumidor.gov.br</strong> ou no app do Serasa. Também é possível limpar o nome
            pelo programa <strong>Desenrola Brasil</strong>.
          </p>
        </div>

        <div className="module-nav">
          <Link to="/educacao-financeira/poupanca" className="btn btn-outline">← Como Poupar</Link>
          <Link to="/educacao-financeira/reserva" className="btn btn-primary">Próximo: Reserva de Emergência →</Link>
        </div>
      </div>
    </div>
  );
}
