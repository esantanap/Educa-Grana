# src/create_vectordb.py - Versão com suporte a PDFs + Metadados enriquecidos
import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
import PyPDF2
from typing import Dict, Tuple

load_dotenv(override=True)

def classify_kind(file_name: str, title: str, first_page_text: str) -> str:
    """
    Classificar tipo de documento baseado em nome, título e conteúdo
    
    Returns:
        str: normativo, procedimento, fluxo_operacional, apresentacao, ou oneoff_nota
    """
    file_lower = file_name.lower()
    first_page_lower = first_page_text[:500].lower()
    title_lower = title.lower()
    
    # Padrões de classificação
    if any(word in file_lower or word in first_page_lower for word in 
           ['normativo', 'norma', 'instrução normativa', 'resolução', 'circular']):
        return "normativo"
    
    if any(word in file_lower or word in first_page_lower for word in 
           ['procedimento', 'manual', 'roteiro', 'passo a passo', 'como fazer']):
        return "procedimento"
    
    if any(word in file_lower or word in first_page_lower for word in 
           ['fluxo', 'processo', 'workflow', 'etapas', 'diagrama']):
        return "fluxo_operacional"
    
    if any(word in file_lower or word in title_lower for word in 
           ['apresenta', 'slides', '.ppt', 'treinamento', 'capacitação']):
        return "apresentacao"
    
    return "oneoff_nota"

def extract_version_or_date(text: str) -> str:
    """
    Extrair versão ou data do documento
    
    Returns:
        str: versão/data encontrada ou string vazia
    """
    # Procurar por padrões de versão
    version_patterns = [
        r'versão\s+(\d+\.?\d*)',
        r'v\.?\s*(\d+\.?\d*)',
        r'revisão\s+(\d+)',
    ]
    
    for pattern in version_patterns:
        match = re.search(pattern, text[:1000], re.IGNORECASE)
        if match:
            return f"v{match.group(1)}"
    
    # Procurar por datas (formato brasileiro)
    date_patterns = [
        r'(\d{2}/\d{2}/\d{4})',
        r'(\d{2}\.\d{2}\.\d{4})',
        r'(\d{4}-\d{2}-\d{2})',
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text[:1000])
        if match:
            return match.group(1)
    
    return ""

def extract_title_from_pdf(pdf_reader: PyPDF2.PdfReader) -> str:
    """Extrair título do PDF (metadados ou primeira linha)"""
    try:
        # Tentar metadados
        if pdf_reader.metadata and pdf_reader.metadata.title:
            return str(pdf_reader.metadata.title)
        
        # Tentar primeira página
        if len(pdf_reader.pages) > 0:
            first_page = pdf_reader.pages[0].extract_text()
            lines = [l.strip() for l in first_page.split('\n') if l.strip()]
            if lines:
                # Título geralmente é a primeira linha não vazia
                return lines[0][:100]  # Limitar tamanho
    except:
        pass
    
    return ""

def extract_text_from_pdf(pdf_path):
    """Extrair texto de arquivo PDF com metadados enriquecidos"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n\n"
            
            # Extrair título e primeira página para classificação
            title = extract_title_from_pdf(pdf_reader)
            first_page = pdf_reader.pages[0].extract_text() if len(pdf_reader.pages) > 0 else ""
            
            return text.strip(), title, first_page
    except Exception as e:
        print(f"❌ Erro ao ler PDF {pdf_path}: {e}")
        return "", "", ""

def create_enhanced_knowledge_base():
    """Criar base de conhecimento com suporte a PDFs e TXTs"""
    
    print("🚀 Criando base de conhecimento com suporte a PDFs...")
    
    # Configurações com paths absolutos
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docs_directory = os.path.join(current_dir, "..", "data", "docs")
    output_file = os.path.join(current_dir, "..", "data", "knowledge_base.json")
    
    # Verificar se existe pasta de documentos
    if not os.path.exists(docs_directory):
        print(f"❌ Pasta {docs_directory} não encontrada!")
        return False
    
    # Listar arquivos suportados
    txt_files = list(Path(docs_directory).glob("*.txt"))
    pdf_files = list(Path(docs_directory).glob("*.pdf"))
    
    print(f"📁 Arquivos encontrados:")
    print(f"  📄 TXT: {len(txt_files)}")
    print(f"  �� PDF: {len(pdf_files)}")
    
    all_files = txt_files + pdf_files
    
    if not all_files:
        print("❌ Nenhum arquivo encontrado!")
        return False
    
    # Processar todos os arquivos
    knowledge_base = []
    
    for file_path in all_files:
        print(f"📄 Processando: {file_path.name}")
        
        try:
            # Extrair texto baseado no tipo de arquivo
            title = ""
            first_page = ""
            
            if file_path.suffix.lower() == '.pdf':
                content, title, first_page = extract_text_from_pdf(file_path)
            elif file_path.suffix.lower() == '.txt':
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Para TXT, usar primeiras linhas como "primeira página"
                    first_page = content[:1000]
                    lines = [l.strip() for l in content.split('\n') if l.strip()]
                    title = lines[0][:100] if lines else ""
            else:
                continue
            
            if not content.strip():
                print(f"  ⚠️ Arquivo vazio ou não foi possível extrair texto")
                continue
            
            # Classificar tipo de documento
            doc_kind = classify_kind(file_path.name, title, first_page)
            version_date = extract_version_or_date(first_page)
            
            print(f"  📋 Tipo: {doc_kind} | Versão/Data: {version_date or 'N/A'}")
            
            # Dividir em parágrafos/seções
            # Para PDFs, usar quebras duplas ou seções maiores
            if file_path.suffix.lower() == '.pdf':
                # Para PDFs, criar chunks maiores
                chunks = []
                lines = content.split('\n')
                current_chunk = ""
                
                for line in lines:
                    line = line.strip()
                    if line:
                        current_chunk += line + " "
                        
                        # Criar chunk quando atingir tamanho adequado
                        if len(current_chunk) > 800:
                            chunks.append(current_chunk.strip())
                            current_chunk = ""
                
                # Adicionar último chunk se houver
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                    
                paragraphs = chunks
            else:
                # Para TXT, usar parágrafos
                paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            
            # Adicionar à base de conhecimento
            for i, paragraph in enumerate(paragraphs):
                if len(paragraph) > 50:  # Apenas conteúdo significativo
                    doc_entry = {
                        "id": f"{file_path.stem}_{i}",
                        "source": file_path.name,
                        "type": file_path.suffix.lower(),
                        "content": paragraph,
                        "length": len(paragraph),
                        "kind": doc_kind,
                        "title": title[:100] if title else file_path.stem,
                        "section": "",  # Pode ser preenchido com detecção de seções
                    }
                    
                    if version_date:
                        doc_entry["version_date"] = version_date
                    
                    knowledge_base.append(doc_entry)
            
            print(f"  ✅ {len(paragraphs)} seções extraídas")
            
        except Exception as e:
            print(f"  ❌ Erro ao processar {file_path.name}: {e}")
    
    if not knowledge_base:
        print("❌ Nenhum conteúdo foi extraído!")
        return False
    
    # Salvar base de conhecimento
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Base de conhecimento criada: {output_file}")
    print(f"📊 Total de entradas: {len(knowledge_base)}")
    
    # Estatísticas por tipo
    txt_count = sum(1 for item in knowledge_base if item['type'] == '.txt')
    pdf_count = sum(1 for item in knowledge_base if item['type'] == '.pdf')
    
    print(f"📈 Distribuição:")
    print(f"  📄 TXT: {txt_count} entradas")
    print(f"  📕 PDF: {pdf_count} entradas")
    
    # Estatísticas por kind
    kind_stats = {}
    for item in knowledge_base:
        kind = item.get('kind', 'oneoff_nota')
        kind_stats[kind] = kind_stats.get(kind, 0) + 1
    
    print(f"📑 Classificação:")
    for kind, count in sorted(kind_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {kind}: {count} documentos")
    
    return True

if __name__ == "__main__":
    print("🎯 Criando base de conhecimento com PDFs...")
    print("=" * 50)
    
    success = create_enhanced_knowledge_base()
    
    print("=" * 50)
    if success:
        print("🎉 Base de conhecimento criada com sucesso!")
        print("💡 Agora você pode fazer perguntas sobre todos os documentos")
    else:
        print("❌ Falha ao criar base de conhecimento")