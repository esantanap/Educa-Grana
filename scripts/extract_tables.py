#!/usr/bin/env python3
# scripts/extract_tables.py
"""
Script para extrair tabelas dos PDFs do Educa Grana e gerar arquivos estruturados.
Facilita a busca em dados tabulares que ficam fragmentados no knowledge_base.json.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

# Diretórios
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
TABLES_DIR = DATA_DIR / "tables"
TABLES_DIR.mkdir(exist_ok=True)

# ============================================================================
# TABELAS MANUAIS (extraídas do documento 1102-05-01)
# ============================================================================

LINHAS_CREDITO = {
    "metadata": {
        "source": "1102-05-01 – Linhas de Crédito (18230).pdf",
        "title": "Linhas de Crédito do Programa Educa Grana",
        "version": "001",
        "date": "26/11/2025",
        "type": "table",
        "kind": "normativo"
    },
    "columns": [
        "Linha de Crédito",
        "Modalidade",
        "Finalidade",
        "Valores",
        "Prazo e Carência"
    ],
    "data": [
        {
            "linha": "Capital de Giro Solidário",
            "modalidade": "Solidário - Grupo de 3 a 10 clientes",
            "finalidade": "Capital de giro",
            "valores": {
                "minimo": "R$ 100,00",
                "maximo_inicial": "R$ 4.000,00 no 1º crédito e R$ 8.000,00 nos demais",
                "maximo_simples": "R$ 6.000,00 no 1º crédito e R$ 15.000,00 nos demais",
                "maximo_ampliada": "R$ 9.000,00 no 1º crédito e R$ 21.000,00 nos demais"
            },
            "prazo": "De 02 a 09 meses, com até 60 dias para pagamento da 1ª parcela"
        },
        {
            "linha": "Capital de Giro Individual",
            "modalidade": "Individual",
            "finalidade": "Capital de giro",
            "valores": {
                "minimo": "R$ 300,00",
                "maximo_inicial": "R$ 3.000,00 no 1º crédito e R$ 8.000,00 nos demais",
                "maximo_simples": "R$ 6.000,00 no 1º crédito e R$ 15.000,00 nos demais",
                "maximo_ampliada": "R$ 9.000,00 no 1º crédito e R$ 21.000,00 nos demais"
            },
            "prazo": "De 02 a 12 meses, com até 60 dias para pagamento da 1ª parcela"
        },
        {
            "linha": "Investimento Fixo",
            "modalidade": "Individual",
            "finalidade": "Investimento",
            "valores": {
                "minimo": "R$ 300,00",
                "maximo_inicial": "R$ 8.000,00",
                "maximo_simples": "R$ 15.000,00",
                "maximo_ampliada": "R$ 21.000,00"
            },
            "prazo": "De 02 a 12 meses, com até 60 dias para pagamento da 1ª parcela"
        },
        {
            "linha": "Educa Grana Comunidade",
            "modalidade": "Solidário - Banco comunitário de 11 a 30 clientes",
            "finalidade": "Capital de giro; Investimento",
            "valores": {
                "minimo": "R$ 100,00",
                "maximo": "R$ 1.100,00 no 1º crédito e R$ 8.000,00 nos demais"
            },
            "prazo": "De 04 a 12 meses, com até 60 dias para pagamento da 1ª parcela"
        },
        {
            "linha": "Educa Grana Mais",
            "modalidade": "Individual",
            "finalidade": "Capital de giro; Investimento",
            "valores": {
                "minimo": "R$ 1.000,00",
                "maximo": "R$ 15.000,00 no 1º crédito e R$ 21.000,00 nos demais"
            },
            "prazo": "De 02 a 12 meses, com até 90 dias para pagamento da 1ª parcela"
        },
        {
            "linha": "Educa Grana Delas",
            "modalidade": "Solidário - Grupo de 3 a 10 clientes; Individual",
            "finalidade": "Capital de giro; Investimento",
            "observacao": "Exclusivo para mulheres, ou pessoas que se identificam como do gênero feminino",
            "valores": {
                "minimo": "R$ 500,00",
                "maximo_inicial": "R$ 6.000,00 no 1º crédito e R$ 8.000,00 nos demais",
                "maximo_simples": "R$ 8.000,00 no 1º crédito e R$ 10.000,00 nos demais",
                "maximo_ampliada": "R$ 10.000,00 no 1º crédito e R$ 12.000,00 nos demais"
            },
            "prazo": "De 04 a 12 meses, com até 90 dias para pagamento da 1ª parcela"
        }
    ]
}


def generate_html_table(table_data: Dict[str, Any], output_path: Path) -> str:
    """Gerar HTML formatado da tabela"""
    
    metadata = table_data["metadata"]
    data = table_data["data"]
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata['title']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #A6193C;
            border-bottom: 3px solid #A6193C;
            padding-bottom: 10px;
        }}
        .metadata {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th {{
            background: #A6193C;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #dee2e6;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .linha-nome {{
            font-weight: 600;
            color: #A6193C;
        }}
        .obs {{
            font-size: 12px;
            color: #666;
            font-style: italic;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{metadata['title']}</h1>
        
        <div class="metadata">
            <strong>Fonte:</strong> {metadata['source']}<br>
            <strong>Versão:</strong> {metadata['version']} - {metadata['date']}<br>
            <strong>Tipo:</strong> {metadata['kind'].capitalize()}
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Linha de Crédito</th>
                    <th>Modalidade</th>
                    <th>Finalidade</th>
                    <th>Valores</th>
                    <th>Prazo e Carência</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for item in data:
        # Formatar valores
        valores_html = []
        valores = item.get("valores", {})
        if "minimo" in valores:
            valores_html.append(f"<strong>Mín:</strong> {valores['minimo']}")
        if "maximo" in valores:
            valores_html.append(f"<strong>Máx:</strong> {valores['maximo']}")
        if "maximo_inicial" in valores:
            valores_html.append(f"<strong>Inicial:</strong> {valores['maximo_inicial']}")
        if "maximo_simples" in valores:
            valores_html.append(f"<strong>Simples:</strong> {valores['maximo_simples']}")
        if "maximo_ampliada" in valores:
            valores_html.append(f"<strong>Ampliada:</strong> {valores['maximo_ampliada']}")
        
        valores_str = "<br>".join(valores_html)
        
        obs = f'<div class="obs">Obs: {item["observacao"]}</div>' if "observacao" in item else ""
        
        html += f"""
                <tr>
                    <td class="linha-nome">{item['linha']}{obs}</td>
                    <td>{item['modalidade']}</td>
                    <td>{item['finalidade']}</td>
                    <td>{valores_str}</td>
                    <td>{item['prazo']}</td>
                </tr>
"""
    
    html += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    
    output_path.write_text(html, encoding='utf-8')
    return str(output_path.absolute())


def generate_text_summary(table_data: Dict[str, Any], output_path: Path) -> str:
    """Gerar resumo em texto para adicionar ao knowledge_base"""
    
    metadata = table_data["metadata"]
    data = table_data["data"]
    
    linhas = [item['linha'] for item in data]
    linhas_str = ", ".join(linhas)
    
    summary = f"""Tabela Completa: {metadata['title']}
Fonte: {metadata['source']}

O Programa Educa Grana dispõe das seguintes linhas de crédito:

"""
    
    for i, item in enumerate(data, 1):
        summary += f"{i}. {item['linha']}\n"
        summary += f"   - Modalidade: {item['modalidade']}\n"
        summary += f"   - Finalidade: {item['finalidade']}\n"
        
        valores = item.get("valores", {})
        if "minimo" in valores:
            summary += f"   - Valores: Mínimo {valores['minimo']}"
            if "maximo" in valores:
                summary += f" / Máximo {valores['maximo']}"
            elif "maximo_inicial" in valores:
                summary += f" / Inicial {valores['maximo_inicial']}"
            summary += "\n"
        
        summary += f"   - Prazo: {item['prazo']}\n"
        
        if "observacao" in item:
            summary += f"   - Obs: {item['observacao']}\n"
        
        summary += "\n"
    
    summary += f"\nLista resumida: {linhas_str}"
    
    output_path.write_text(summary, encoding='utf-8')
    return str(output_path.absolute())


def main():
    print("=" * 80)
    print("📊 EXTRAÇÃO DE TABELAS DOS PDFs DO Educa Grana")
    print("=" * 80)
    
    # 1. Linhas de Crédito
    print("\n1️⃣ Processando: Linhas de Crédito...")
    
    # JSON
    json_path = TABLES_DIR / "linhas_credito.json"
    json_path.write_text(json.dumps(LINHAS_CREDITO, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"   ✅ JSON: {json_path}")
    
    # HTML
    html_path = TABLES_DIR / "linhas_credito.html"
    generate_html_table(LINHAS_CREDITO, html_path)
    print(f"   ✅ HTML: {html_path}")
    
    # Texto resumido
    txt_path = TABLES_DIR / "linhas_credito.txt"
    generate_text_summary(LINHAS_CREDITO, txt_path)
    print(f"   ✅ TXT: {txt_path}")
    
    # Adicionar ao knowledge_base
    print("\n2️⃣ Adicionando ao knowledge_base.json...")
    kb_path = DATA_DIR / "knowledge_base.json"
    
    if kb_path.exists():
        with open(kb_path, 'r', encoding='utf-8') as f:
            kb = json.load(f)
        
        # Criar entrada com tabela completa
        table_entry = {
            "id": "TABLE_linhas_credito",
            "source": "1102-05-01 – Linhas de Crédito (18230).pdf",
            "type": "table",
            "content": txt_path.read_text(encoding='utf-8'),
            "length": len(txt_path.read_text(encoding='utf-8')),
            "kind": "table",  # 🔥 IMPORTANTE: tipo = table para boost máximo
            "title": "Tabela Completa de Linhas de Crédito",
            "section": "Linhas de Crédito",
            "version_date": "v001",
            "table_data": LINHAS_CREDITO  # Dados estruturados
        }
        
        # Verificar se já existe
        existing = [i for i, doc in enumerate(kb) if doc.get("id") == "TABLE_linhas_credito"]
        if existing:
            kb[existing[0]] = table_entry
            print("   ✅ Tabela atualizada no knowledge_base.json")
        else:
            kb.append(table_entry)
            print("   ✅ Tabela adicionada ao knowledge_base.json")
        
        # Salvar
        with open(kb_path, 'w', encoding='utf-8') as f:
            json.dump(kb, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("✅ EXTRAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print(f"\n📂 Arquivos gerados em: {TABLES_DIR}/")
    print(f"   - linhas_credito.json (dados estruturados)")
    print(f"   - linhas_credito.html (visualização)")
    print(f"   - linhas_credito.txt (texto para busca)")
    print(f"\n💡 Próximos passos:")
    print(f"   1. Abra {html_path} no navegador para visualizar")
    print(f"   2. Reinicie o Streamlit para usar a nova entrada do knowledge_base")
    print(f"   3. Teste: 'Quais linhas de crédito?' - agora deve listar todas as 6 linhas")


if __name__ == "__main__":
    main()
