#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de teste para validar otimizações de custos
Testa as melhorias aplicadas nos parâmetros de busca
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from src.agent import answer_question
import time

# Perguntas de teste
TEST_QUESTIONS = [
    "Quais são as linhas de crédito disponíveis?",
    "Como funciona o Crediamigo Comunidade?",
    "Qual o valor máximo de empréstimo?",
    "Quais documentos são necessários para solicitar crédito?",
    "Como fazer renovação de crédito?",
]

def test_question(question: str, index: int):
    """Testa uma pergunta e retorna métricas"""
    print(f"\n{'='*80}")
    print(f"TESTE {index + 1}/{len(TEST_QUESTIONS)}")
    print(f"{'='*80}")
    print(f"PERGUNTA: {question}")
    print(f"{'-'*80}")
    
    start_time = time.time()
    
    try:
        response = answer_question(question)
        elapsed = time.time() - start_time
        
        # Extrair métricas da resposta
        response_length = len(response)
        sources_count = response.count("**Fontes consultadas:**")
        
        print(f"\nRESPOSTA ({response_length} caracteres, {elapsed:.2f}s):")
        print(f"{'-'*80}")
        
        # Mostrar apenas primeiras linhas da resposta
        lines = response.split('\n')
        for line in lines[:10]:
            print(line)
        
        if len(lines) > 10:
            print(f"... (+{len(lines)-10} linhas)")
        
        print(f"\nMETRICAS:")
        print(f"  - Tempo de resposta: {elapsed:.2f}s")
        print(f"  - Tamanho da resposta: {response_length} caracteres")
        print(f"  - Fontes citadas: {'Sim' if sources_count > 0 else 'Não'}")
        
        return {
            "question": question,
            "success": True,
            "time": elapsed,
            "length": response_length,
            "has_sources": sources_count > 0
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\nERRO ({elapsed:.2f}s):")
        print(f"  {str(e)}")
        
        return {
            "question": question,
            "success": False,
            "time": elapsed,
            "error": str(e)
        }

def main():
    """Executa bateria de testes"""
    print("TESTE DE OTIMIZACOES - IAmiga")
    print("="*80)
    print(f"Total de perguntas: {len(TEST_QUESTIONS)}")
    print("="*80)
    
    results = []
    
    for i, question in enumerate(TEST_QUESTIONS):
        result = test_question(question, i)
        results.append(result)
        time.sleep(0.5)  # Pequena pausa entre testes
    
    # Resumo final
    print(f"\n\n{'='*80}")
    print("RESUMO DOS TESTES")
    print(f"{'='*80}")
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"\n[OK] Sucesso: {len(successful)}/{len(TEST_QUESTIONS)}")
    print(f"[ERRO] Falhas: {len(failed)}/{len(TEST_QUESTIONS)}")
    
    if successful:
        avg_time = sum(r["time"] for r in successful) / len(successful)
        avg_length = sum(r["length"] for r in successful) / len(successful)
        with_sources = sum(1 for r in successful if r["has_sources"])
        
        print(f"\n[TEMPO] Tempo médio de resposta: {avg_time:.2f}s")
        print(f"[TEXTO] Tamanho médio de resposta: {avg_length:.0f} caracteres")
        print(f"[FONTES] Respostas com fontes: {with_sources}/{len(successful)}")
    
    if failed:
        print(f"\n[ATENCAO] Perguntas que falharam:")
        for r in failed:
            print(f"  - {r['question']}")
            print(f"    Erro: {r.get('error', 'Desconhecido')}")
    
    print(f"\n{'='*80}")
    print("Testes concluidos!")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
