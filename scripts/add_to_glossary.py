#!/usr/bin/env python3
# scripts/add_to_glossary.py
"""
Script interativo para adicionar termos ao glossário de forma segura.
Valida JSON e faz backup automático.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

GLOSSARIO_PATH = Path("src/core/domain/glossario.json")
BACKUP_DIR = Path("data/glossary_backups")


def load_glossario():
    """Carrega o glossário atual."""
    with open(GLOSSARIO_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_glossario(data):
    """Salva o glossário com backup automático."""
    # Criar diretório de backup
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    # Fazer backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"glossario_backup_{timestamp}.json"
    shutil.copy(GLOSSARIO_PATH, backup_file)
    print(f"✅ Backup criado: {backup_file}")
    
    # Salvar novo glossário
    with open(GLOSSARIO_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Glossário atualizado: {GLOSSARIO_PATH}")


def add_alias():
    """Adiciona novo alias ao glossário."""
    glossario = load_glossario()
    
    print("\n" + "=" * 80)
    print("➕ ADICIONAR ALIAS")
    print("=" * 80)
    
    # Mostrar aliases existentes
    print("\n📚 Aliases atuais:")
    for i, key in enumerate(glossario['aliases'].keys(), 1):
        print(f"   {i}. {key}: {glossario['aliases'][key]}")
    
    print("\n" + "-" * 80)
    
    # Coletar dados
    termo_principal = input("\n🔑 Termo principal (ex: 'prazo'): ").strip().lower()
    
    if termo_principal in glossario['aliases']:
        print(f"\n⚠️  Termo '{termo_principal}' já existe!")
        print(f"   Aliases atuais: {glossario['aliases'][termo_principal]}")
        adicionar_mais = input("   Adicionar mais aliases a este termo? (s/n): ").strip().lower()
        
        if adicionar_mais == 's':
            sinonimos_str = input("   Digite os novos sinônimos (separados por vírgula): ")
            novos_sinonimos = [s.strip().lower() for s in sinonimos_str.split(',')]
            glossario['aliases'][termo_principal].extend(novos_sinonimos)
            print(f"✅ Adicionados: {novos_sinonimos}")
        else:
            print("❌ Operação cancelada")
            return
    else:
        sinonimos_str = input(f"📝 Sinônimos de '{termo_principal}' (separados por vírgula): ")
        sinonimos = [s.strip().lower() for s in sinonimos_str.split(',')]
        glossario['aliases'][termo_principal] = sinonimos
        print(f"✅ Novo alias criado: {termo_principal} → {sinonimos}")
    
    # Confirmar
    print("\n" + "-" * 80)
    print("📋 RESUMO DA MUDANÇA:")
    print(f"   Termo: {termo_principal}")
    print(f"   Aliases: {glossario['aliases'][termo_principal]}")
    
    confirmar = input("\n💾 Salvar mudanças? (s/n): ").strip().lower()
    
    if confirmar == 's':
        save_glossario(glossario)
        print("\n✅ Glossário atualizado com sucesso!")
    else:
        print("\n❌ Mudanças descartadas")


def adjust_doc_boost():
    """Ajusta pesos de doc_boosts."""
    glossario = load_glossario()
    
    print("\n" + "=" * 80)
    print("⚖️  AJUSTAR DOC_BOOSTS")
    print("=" * 80)
    
    # Mostrar boosts atuais
    print("\n📊 Boosts atuais:")
    for kind, boost in glossario['doc_boosts'].items():
        print(f"   {kind}: {boost}")
    
    print("\n" + "-" * 80)
    
    tipo_doc = input("\n📄 Tipo de documento (ex: 'normativo'): ").strip().lower()
    
    if tipo_doc not in glossario['doc_boosts']:
        print(f"\n⚠️  Tipo '{tipo_doc}' não existe!")
        print(f"   Tipos disponíveis: {list(glossario['doc_boosts'].keys())}")
        return
    
    boost_atual = glossario['doc_boosts'][tipo_doc]
    print(f"\n   Boost atual de '{tipo_doc}': {boost_atual}")
    
    try:
        novo_boost = float(input(f"   Novo boost (0.7 a 1.5, sugerido: {boost_atual}): "))
        
        if novo_boost < 0.7 or novo_boost > 1.5:
            print("⚠️  Valor fora do recomendado (0.7 a 1.5)")
            confirmar = input("   Continuar mesmo assim? (s/n): ").strip().lower()
            if confirmar != 's':
                print("❌ Operação cancelada")
                return
        
        glossario['doc_boosts'][tipo_doc] = round(novo_boost, 2)
        
        # Confirmar
        print("\n" + "-" * 80)
        print("📋 RESUMO DA MUDANÇA:")
        print(f"   Tipo: {tipo_doc}")
        print(f"   Boost anterior: {boost_atual}")
        print(f"   Novo boost: {novo_boost}")
        
        confirmar = input("\n💾 Salvar mudanças? (s/n): ").strip().lower()
        
        if confirmar == 's':
            save_glossario(glossario)
            print("\n✅ Glossário atualizado com sucesso!")
        else:
            print("\n❌ Mudanças descartadas")
            
    except ValueError:
        print("❌ Valor inválido! Use números (ex: 1.25)")


def add_stop_term():
    """Adiciona termo à lista de stop_expansion_in."""
    glossario = load_glossario()
    
    print("\n" + "=" * 80)
    print("🛑 ADICIONAR TERMO PROTEGIDO")
    print("=" * 80)
    
    print("\n📋 Termos protegidos atuais:")
    for term in glossario['stop_expansion_in']:
        print(f"   • {term}")
    
    print("\n" + "-" * 80)
    
    novo_termo = input("\n🔒 Termo a proteger (ex: 'matrícula'): ").strip()
    
    if novo_termo in glossario['stop_expansion_in']:
        print(f"\n⚠️  Termo '{novo_termo}' já está protegido!")
        return
    
    glossario['stop_expansion_in'].append(novo_termo)
    
    print(f"\n✅ Adicionado: '{novo_termo}'")
    
    confirmar = input("\n💾 Salvar mudanças? (s/n): ").strip().lower()
    
    if confirmar == 's':
        save_glossario(glossario)
        print("\n✅ Glossário atualizado com sucesso!")
    else:
        print("\n❌ Mudanças descartadas")


def main():
    print("=" * 80)
    print("📚 EDITOR DE GLOSSÁRIO - IAmiga")
    print("=" * 80)
    
    if not GLOSSARIO_PATH.exists():
        print(f"\n❌ Arquivo não encontrado: {GLOSSARIO_PATH}")
        return
    
    while True:
        print("\n" + "=" * 80)
        print("🛠️  O QUE DESEJA FAZER?")
        print("=" * 80)
        print("1. ➕ Adicionar/editar alias")
        print("2. ⚖️  Ajustar doc_boost")
        print("3. 🛑 Adicionar termo protegido")
        print("4. 📄 Ver glossário completo")
        print("5. 🚪 Sair")
        
        escolha = input("\nEscolha uma opção (1-5): ").strip()
        
        if escolha == '1':
            add_alias()
        elif escolha == '2':
            adjust_doc_boost()
        elif escolha == '3':
            add_stop_term()
        elif escolha == '4':
            glossario = load_glossario()
            print("\n" + json.dumps(glossario, ensure_ascii=False, indent=2))
        elif escolha == '5':
            print("\n👋 Até logo!")
            break
        else:
            print("\n⚠️  Opção inválida!")
    
    print("\n💡 LEMBRE-SE: Reinicie o Streamlit para aplicar as mudanças!")
    print("   Comando: streamlit run src/core/frontend/app.py")


if __name__ == "__main__":
    main()
