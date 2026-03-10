# Arquivos Removidos - Limpeza de Código

**Data:** 13/01/2026  
**Motivo:** Consolidação de código e remoção de arquivos obsoletos

## Arquivos Removidos da pasta `src/agent_antigos/`

Total: 12 arquivos antigos removidos

| Arquivo | Tamanho | Última Modificação | Observação |
|---------|---------|-------------------|------------|
| agent.py | 13KB | 10/12/2025 | Versão antiga |
| agent1.py | 10KB | 10/12/2025 | Versão antiga |
| agent2.py.py | 10KB | 10/12/2025 | Versão antiga (nome duplicado) |
| agent_com_guardrails.py | 12KB | 09/12/2025 | Versão com guardrails antiga |
| agent_keyword_backup.py | 10KB | 09/12/2025 | Backup de versão keyword |
| agent_keyword_version.py | 10KB | 09/12/2025 | Versão keyword |
| agent_old.py | 9KB | 10/12/2025 | Versão antiga |
| agent_old1.py | 9KB | 09/12/2025 | Versão antiga |
| agent_old2.py | 14KB | 09/12/2025 | Versão antiga |
| agent_original_backup.py | 10KB | 09/12/2025 | Backup original |
| agent_semantic_final.py | 10KB | 10/12/2025 | Versão semântica antiga |
| agent_semantic_hybrid.py | 12KB | 10/12/2025 | Versão híbrida antiga |

## Arquivo Atual

- **Localização:** `src/agent.py`
- **Recursos:**
  - ✅ Busca semântica TF-IDF
  - ✅ Logging profissional
  - ✅ SSL seguro
  - ✅ Citação de fontes
  - ✅ Sem paths hardcoded

## Recuperação

Caso precise recuperar algum arquivo:
```bash
git log --all --full-history -- "src/agent_antigos/*"
git checkout <commit-hash> -- src/agent_antigos/<arquivo>
```

## Benefícios da Limpeza

1. **Clareza:** Apenas 1 versão ativa do agent
2. **Manutenção:** Menos confusão sobre qual arquivo usar
3. **Espaço:** ~130KB liberados
4. **Git:** Histórico limpo e organizado
