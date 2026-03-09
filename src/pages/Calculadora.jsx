import { useState, useMemo } from 'react';
import './Calculadora.css';

const incomeCategories = [
  { key: 'salario', label: 'Salário / Renda principal' },
  { key: 'beneficios', label: 'Benefícios (Bolsa Família, BPC etc.)' },
  { key: 'bicos', label: 'Trabalhos extras / Bicos' },
  { key: 'outros_receita', label: 'Outras receitas' },
];

const expenseCategories = [
  { key: 'aluguel', label: '🏠 Aluguel / Moradia' },
  { key: 'alimentacao', label: '🍽️ Alimentação' },
  { key: 'transporte', label: '🚌 Transporte' },
  { key: 'luz', label: '💡 Luz / Água / Gás' },
  { key: 'celular', label: '📱 Celular / Internet' },
  { key: 'saude', label: '💊 Saúde / Remédios' },
  { key: 'educacao', label: '🎓 Educação' },
  { key: 'vestuario', label: '👕 Roupas / Calçados' },
  { key: 'lazer', label: '🎭 Lazer / Entretenimento' },
  { key: 'dividas', label: '💳 Dívidas / Parcelas' },
  { key: 'outros_despesa', label: '📦 Outros gastos' },
];

function formatBRL(value) {
  if (!value && value !== 0) return '';
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
}

function parseNumber(str) {
  const clean = str.replace(/[^\d,]/g, '').replace(',', '.');
  const num = parseFloat(clean);
  return isNaN(num) ? 0 : num;
}

export default function Calculadora() {
  const [income, setIncome] = useState({});
  const [expenses, setExpenses] = useState({});

  const totalIncome = useMemo(
    () => Object.values(income).reduce((acc, v) => acc + parseNumber(v || '0'), 0),
    [income],
  );

  const totalExpenses = useMemo(
    () => Object.values(expenses).reduce((acc, v) => acc + parseNumber(v || '0'), 0),
    [expenses],
  );

  const balance = totalIncome - totalExpenses;
  const savingsRate = totalIncome > 0 ? ((balance / totalIncome) * 100).toFixed(1) : 0;
  const emergencyGoal = totalExpenses * 3;

  const handleIncome = (key, val) => setIncome((prev) => ({ ...prev, [key]: val }));
  const handleExpense = (key, val) => setExpenses((prev) => ({ ...prev, [key]: val }));

  const reset = () => {
    setIncome({});
    setExpenses({});
  };

  const balanceClass = balance > 0 ? 'positive' : balance < 0 ? 'negative' : 'zero';

  return (
    <div>
      <div className="page-header">
        <h1>🧮 Calculadora de Orçamento</h1>
        <p>Insira suas receitas e despesas para ver seu saldo mensal e receber dicas personalizadas.</p>
      </div>

      <div className="calc-container container">
        <div className="calc-grid">
          {/* Income Column */}
          <div className="calc-section">
            <div className="calc-section-header income">
              <span>💰</span>
              <h2>Receitas (o que entra)</h2>
            </div>
            <div className="calc-fields">
              {incomeCategories.map((cat) => (
                <div className="calc-field" key={cat.key}>
                  <label htmlFor={`income-${cat.key}`}>{cat.label}</label>
                  <div className="calc-input-wrap">
                    <span className="calc-prefix">R$</span>
                    <input
                      id={`income-${cat.key}`}
                      type="number"
                      min="0"
                      step="0.01"
                      placeholder="0,00"
                      value={income[cat.key] || ''}
                      onChange={(e) => handleIncome(cat.key, e.target.value)}
                    />
                  </div>
                </div>
              ))}
            </div>
            <div className="calc-total income-total">
              <span>Total de receitas</span>
              <strong>{formatBRL(totalIncome)}</strong>
            </div>
          </div>

          {/* Expenses Column */}
          <div className="calc-section">
            <div className="calc-section-header expense">
              <span>💸</span>
              <h2>Despesas (o que sai)</h2>
            </div>
            <div className="calc-fields">
              {expenseCategories.map((cat) => (
                <div className="calc-field" key={cat.key}>
                  <label htmlFor={`expense-${cat.key}`}>{cat.label}</label>
                  <div className="calc-input-wrap">
                    <span className="calc-prefix">R$</span>
                    <input
                      id={`expense-${cat.key}`}
                      type="number"
                      min="0"
                      step="0.01"
                      placeholder="0,00"
                      value={expenses[cat.key] || ''}
                      onChange={(e) => handleExpense(cat.key, e.target.value)}
                    />
                  </div>
                </div>
              ))}
            </div>
            <div className="calc-total expense-total">
              <span>Total de despesas</span>
              <strong>{formatBRL(totalExpenses)}</strong>
            </div>
          </div>
        </div>

        {/* Result Panel */}
        {(totalIncome > 0 || totalExpenses > 0) && (
          <div className="calc-result">
            <h2>📊 Resultado do seu orçamento</h2>

            <div className="calc-result-cards">
              <div className="calc-result-card">
                <span className="calc-result-label">Total de receitas</span>
                <span className="calc-result-value income-color">{formatBRL(totalIncome)}</span>
              </div>
              <div className="calc-result-card">
                <span className="calc-result-label">Total de despesas</span>
                <span className="calc-result-value expense-color">{formatBRL(totalExpenses)}</span>
              </div>
              <div className={`calc-result-card balance-card ${balanceClass}`}>
                <span className="calc-result-label">Saldo mensal</span>
                <span className="calc-result-value">{formatBRL(balance)}</span>
                <span className="calc-result-sub">
                  {balance > 0
                    ? `${savingsRate}% da sua renda disponível`
                    : balance < 0
                    ? 'Seus gastos superam a renda'
                    : 'Receitas e despesas estão equilibradas'}
                </span>
              </div>
            </div>

            {/* Progress bar */}
            {totalIncome > 0 && (
              <div className="calc-progress-wrap">
                <div className="calc-progress-labels">
                  <span>Despesas ({((totalExpenses / totalIncome) * 100).toFixed(0)}%)</span>
                  <span>Disponível ({Math.max(0, (balance / totalIncome) * 100).toFixed(0)}%)</span>
                </div>
                <div className="calc-progress-bar">
                  <div
                    className="calc-progress-fill expense-fill"
                    style={{ width: `${Math.min(100, (totalExpenses / totalIncome) * 100)}%` }}
                  />
                </div>
              </div>
            )}

            {/* Tips based on result */}
            <div className="calc-tips">
              {balance < 0 && (
                <div className="warning-box">
                  <strong>⚠️ Atenção:</strong> Suas despesas superam a renda em{' '}
                  <strong>{formatBRL(Math.abs(balance))}</strong>. Revise seus gastos e identifique
                  onde é possível cortar. Verifique também se você tem direito a algum benefício social.
                </div>
              )}
              {balance >= 0 && balance < totalIncome * 0.1 && totalIncome > 0 && (
                <div className="warning-box">
                  <strong>⚠️ Margem apertada:</strong> Você tem pouca sobra no mês. Qualquer imprevisto
                  pode desequilibrar seu orçamento. Tente reduzir gastos para criar uma reserva.
                </div>
              )}
              {balance >= totalIncome * 0.1 && balance < totalIncome * 0.2 && (
                <div className="tip-box">
                  <p className="tip-title">💡 Você está no caminho certo!</p>
                  <p>
                    Você tem uma margem de {savingsRate}% da sua renda. Tente aumentar para 20%
                    guardando mais ou reduzindo gastos variáveis.
                  </p>
                </div>
              )}
              {balance >= totalIncome * 0.2 && (
                <div className="tip-box">
                  <p className="tip-title">🎉 Excelente controle financeiro!</p>
                  <p>
                    Você poupa {savingsRate}% da sua renda — acima da meta recomendada de 20%. Continue
                    assim e considere diversificar onde guardar o dinheiro para fazê-lo render mais.
                  </p>
                </div>
              )}

              {/* Emergency fund tip */}
              <div className="info-box">
                <strong>🆘 Meta de reserva de emergência:</strong> Com suas despesas atuais, você
                precisaria de <strong>{formatBRL(emergencyGoal)}</strong> para ter 3 meses de reserva.
                {balance > 0 && (
                  <span>
                    {' '}Poupando {formatBRL(balance)} por mês, você atingiria essa meta em{' '}
                    <strong>{Math.ceil(emergencyGoal / balance)} meses</strong>.
                  </span>
                )}
              </div>
            </div>
          </div>
        )}

        <div className="calc-actions">
          <button className="btn btn-outline" onClick={reset}>
            🔄 Limpar calculadora
          </button>
        </div>
      </div>
    </div>
  );
}
