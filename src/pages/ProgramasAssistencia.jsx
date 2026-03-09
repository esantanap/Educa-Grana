import { useState } from 'react';
import './ProgramasAssistencia.css';

const programs = [
  {
    id: 'bolsa-familia',
    icon: '👨‍👩‍👧‍👦',
    name: 'Bolsa Família',
    category: 'Renda',
    badge: 'badge-success',
    summary: 'Transferência de renda para famílias em situação de pobreza e extrema pobreza.',
    description:
      'O Bolsa Família é o principal programa de transferência de renda do governo federal. Beneficia famílias com renda mensal de até R$ 218 por pessoa. O valor dos benefícios varia conforme a composição familiar e pode incluir adicionais para crianças, gestantes e nutrizes.',
    eligibility: [
      'Renda familiar mensal de até R$ 218 por pessoa',
      'Estar inscrito no CadÚnico',
      'Crianças em idade escolar devem estar matriculadas e frequentando a escola',
      'Crianças menores de 7 anos devem manter o calendário de vacinação em dia',
    ],
    howToApply:
      'Procure o CRAS (Centro de Referência de Assistência Social) do seu município para se inscrever no CadÚnico. Com o CadÚnico atualizado, o sistema verifica automaticamente se você atende aos critérios.',
    contact: 'Central de Atendimento: 121 (gratuito) | gov.br/bolsafamilia',
    website: 'https://www.gov.br/bolsafamilia',
  },
  {
    id: 'bpc',
    icon: '👴',
    name: 'BPC/LOAS',
    category: 'Renda',
    badge: 'badge-success',
    summary: 'Benefício de 1 salário mínimo para idosos acima de 65 anos e pessoas com deficiência.',
    description:
      'O Benefício de Prestação Continuada (BPC) garante 1 salário mínimo mensal a idosos com 65 anos ou mais e a pessoas com deficiência de qualquer idade que comprovem não ter meios de prover a própria manutenção ou de tê-la provida por sua família.',
    eligibility: [
      'Idoso com 65 anos ou mais OU pessoa com deficiência (qualquer idade)',
      'Renda familiar mensal per capita inferior a 1/4 do salário mínimo',
      'Estar inscrito no CadÚnico',
      'Não receber outro benefício da Seguridade Social',
    ],
    howToApply:
      'Agende pelo Meu INSS (meu.inss.gov.br) ou ligue 135 (gratuito). Você precisará de documentos pessoais, comprovante de renda familiar e, para PcD, laudo médico.',
    contact: 'Central INSS: 135 (gratuito) | meu.inss.gov.br',
    website: 'https://www.gov.br/inss',
  },
  {
    id: 'auxilio-gas',
    icon: '🔥',
    name: 'Auxílio Gás',
    category: 'Benefícios',
    badge: 'badge-info',
    summary: 'Auxílio bimestral para compra de gás de cozinha para famílias de baixa renda.',
    description:
      'O Auxílio Gás dos Brasileiros é pago a cada dois meses e tem valor equivalente a 100% do preço médio nacional do botijão de 13kg. O benefício é pago automaticamente para quem se encaixa nos critérios, via Caixa Econômica Federal.',
    eligibility: [
      'Estar inscrito no CadÚnico com dados atualizados',
      'Renda familiar mensal de até meio salário mínimo por pessoa',
      'Famílias com integrante recebendo BPC também têm direito',
    ],
    howToApply:
      'Não é necessário fazer inscrição separada. O benefício é concedido automaticamente com base no CadÚnico. Mantenha seu cadastro atualizado no CRAS.',
    contact: 'Central de Atendimento: 121 (gratuito)',
    website: 'https://www.gov.br/pt-br/noticias/assistencia-social/2021/11/auxilio-gas',
  },
  {
    id: 'cadunico',
    icon: '📋',
    name: 'CadÚnico',
    category: 'Cadastro',
    badge: 'badge-warning',
    summary: 'Cadastro único que abre porta para vários benefícios sociais do governo federal.',
    description:
      'O Cadastro Único (CadÚnico) é uma ferramenta do governo federal para identificar e caracterizar as famílias de baixa renda. É a porta de entrada para acessar mais de 20 programas sociais, incluindo Bolsa Família, Auxílio Gás, tarifa social de energia e outros.',
    eligibility: [
      'Famílias com renda mensal de até meio salário mínimo por pessoa',
      'Famílias com renda total de até 3 salários mínimos',
      'Famílias em situação de pobreza ou vulnerabilidade',
    ],
    howToApply:
      'Procure o CRAS mais próximo com documentos pessoais de todos os moradores da casa (RG, CPF, certidão de nascimento), comprovante de residência e dados sobre renda familiar.',
    contact: 'CRAS do seu município | Central de Atendimento: 121',
    website: 'https://www.gov.br/pt-br/temas/cadastro-unico',
  },
  {
    id: 'tarifa-social',
    icon: '⚡',
    name: 'Tarifa Social de Energia',
    category: 'Benefícios',
    badge: 'badge-info',
    summary: 'Desconto na conta de luz de até 65% para famílias de baixa renda.',
    description:
      'A Tarifa Social de Energia Elétrica (TSEE) garante descontos na conta de luz para famílias de baixa renda inscritas no CadÚnico. O desconto varia de 10% a 65% dependendo do consumo mensal.',
    eligibility: [
      'Estar inscrito no CadÚnico',
      'Ser beneficiário do Bolsa Família ou BPC/LOAS',
      'Renda familiar de até 3 salários mínimos',
      'Pessoa com deficiência ou doença que exige uso contínuo de equipamentos médicos',
    ],
    howToApply:
      'Entre em contato com a distribuidora de energia elétrica da sua região apresentando o número do NIS (do CadÚnico). Muitas distribuidoras aplicam o desconto automaticamente.',
    contact: 'Distribuidora de energia da sua região',
    website: 'https://www.gov.br/pt-br/temas/tarifa-social-de-energia-eletrica',
  },
  {
    id: 'pronatec',
    icon: '🎓',
    name: 'Qualificação Profissional Gratuita',
    category: 'Educação',
    badge: 'badge-success',
    summary: 'Cursos profissionalizantes gratuitos oferecidos pelo SENAI, SENAC, SENAR e outras instituições.',
    description:
      'O governo federal e estados oferecem cursos profissionalizantes gratuitos por meio de programas como o Qualifica Mais, cursos no SENAI, SENAC, SENAR e SENAT para beneficiários do CadÚnico e trabalhadores em geral. Qualificação profissional é fundamental para aumentar a renda.',
    eligibility: [
      'Maiores de 16 anos',
      'Beneficiários do CadÚnico têm prioridade em muitos programas',
      'Cada curso tem seus critérios específicos',
    ],
    howToApply:
      'Acesse o portal gov.br/qualificamais, entre no site do SENAI (senai.br), SENAC (senac.br) ou procure o SINE (Sistema Nacional de Emprego) da sua cidade.',
    contact: 'SINE do seu município | gov.br/qualificamais | senai.br | senac.br',
    website: 'https://www.gov.br/trabalho-e-emprego',
  },
  {
    id: 'farmacia-popular',
    icon: '💊',
    name: 'Farmácia Popular',
    category: 'Saúde',
    badge: 'badge-info',
    summary: 'Medicamentos gratuitos ou com até 90% de desconto para doenças crônicas.',
    description:
      'O Programa Farmácia Popular disponibiliza medicamentos gratuitamente ou com descontos de até 90% para tratamento de hipertensão, diabetes, asma, osteoporose, rinite e outros. Os medicamentos podem ser retirados em farmácias credenciadas.',
    eligibility: [
      'Ter receita médica válida para o medicamento',
      'Medicamentos do "Aqui Tem Farmácia Popular" são gratuitos para hipertensão e diabetes',
      'Outros medicamentos têm copagamento mínimo',
    ],
    howToApply:
      'Procure uma farmácia credenciada ao Farmácia Popular com receita médica e documento de identidade com CPF. Não é necessária inscrição prévia.',
    contact: 'Disque Saúde: 136 (gratuito) | gov.br/farmaciapopular',
    website: 'https://www.gov.br/saude/pt-br/acesso-a-informacao/acoes-e-programas/farmacia-popular',
  },
  {
    id: 'minha-casa',
    icon: '🏠',
    name: 'Minha Casa, Minha Vida',
    category: 'Moradia',
    badge: 'badge-warning',
    summary: 'Programa habitacional com subsídios do governo para famílias de baixa renda adquirirem a casa própria.',
    description:
      'O Minha Casa, Minha Vida oferece subsídios e financiamentos com juros reduzidos para famílias comprarem ou construírem sua casa. Famílias com renda de até R$ 2.640 podem receber subsídio de até 95% do valor do imóvel.',
    eligibility: [
      'Renda familiar bruta mensal de até R$ 8.000',
      'Não ter imóvel em seu nome ou financiamento habitacional ativo',
      'Não ter sido beneficiado anteriormente pelo programa',
      'Estar inscrito no CadÚnico (para as faixas de menor renda)',
    ],
    howToApply:
      'Procure a Caixa Econômica Federal ou prefeitura do seu município. Você também pode se inscrever pelo site da Caixa ou pelo aplicativo Habitação Caixa.',
    contact: 'Caixa Econômica Federal: 0800 726 0101 | caixa.gov.br',
    website: 'https://www.caixa.gov.br/voce/habitacao/minha-casa-minha-vida',
  },
];

const categories = ['Todos', 'Renda', 'Benefícios', 'Cadastro', 'Educação', 'Saúde', 'Moradia'];

export default function ProgramasAssistencia() {
  const [activeCategory, setActiveCategory] = useState('Todos');
  const [expanded, setExpanded] = useState(null);

  const filtered = activeCategory === 'Todos'
    ? programs
    : programs.filter((p) => p.category === activeCategory);

  const toggle = (id) => setExpanded((prev) => (prev === id ? null : id));

  return (
    <div>
      <div className="page-header">
        <h1>🏛️ Programas de Assistência Social</h1>
        <p>
          Conheça os principais programas do governo federal que podem ajudar você e sua família.
          Veja os critérios e saiba como se inscrever.
        </p>
      </div>

      <div className="section container">
        <div className="tip-box">
          <p className="tip-title">💡 Como acessar os benefícios?</p>
          <p>
            A maioria dos programas sociais exige a inscrição no <strong>CadÚnico</strong> (Cadastro
            Único). Procure o <strong>CRAS</strong> (Centro de Referência de Assistência Social)
            mais próximo para se cadastrar gratuitamente.
          </p>
        </div>

        {/* Category Filter */}
        <div className="pa-filters">
          {categories.map((cat) => (
            <button
              key={cat}
              className={`pa-filter-btn ${activeCategory === cat ? 'active' : ''}`}
              onClick={() => setActiveCategory(cat)}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Programs List */}
        <div className="pa-programs-list">
          {filtered.map((program) => (
            <div
              key={program.id}
              className={`pa-program-card ${expanded === program.id ? 'expanded' : ''}`}
            >
              <button
                className="pa-program-header"
                onClick={() => toggle(program.id)}
                aria-expanded={expanded === program.id}
              >
                <span className="pa-program-icon">{program.icon}</span>
                <div className="pa-program-title">
                  <div className="pa-program-name-row">
                    <h3>{program.name}</h3>
                    <span className={`badge ${program.badge}`}>{program.category}</span>
                  </div>
                  <p className="pa-program-summary">{program.summary}</p>
                </div>
                <span className="pa-program-chevron" aria-hidden="true">
                  {expanded === program.id ? '▲' : '▼'}
                </span>
              </button>

              {expanded === program.id && (
                <div className="pa-program-body">
                  <p className="pa-program-desc">{program.description}</p>

                  <h4>📋 Critérios de elegibilidade</h4>
                  <ul className="pa-list">
                    {program.eligibility.map((e) => (
                      <li key={e}>✅ {e}</li>
                    ))}
                  </ul>

                  <h4>📝 Como solicitar</h4>
                  <p>{program.howToApply}</p>

                  <div className="pa-contact-box">
                    <strong>📞 Contato:</strong> {program.contact}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="info-box" style={{ marginTop: '2rem' }}>
          <strong>📢 Ligue 121 gratuitamente</strong> para tirar dúvidas sobre programas sociais,
          verificar o status do seu cadastro no CadÚnico ou obter informações sobre o Bolsa Família.
          O serviço é gratuito e funciona de segunda a sábado.
        </div>
      </div>
    </div>
  );
}
