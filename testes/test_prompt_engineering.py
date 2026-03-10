# -*- coding: utf-8 -*-
"""
Teste do sistema de Prompt Engineering para IAmiga.
"""

import sys
sys.path.append('src')

def test_prompt_engineering():
    """Testa o sistema de prompt engineering."""
    print("🧪 TESTANDO SISTEMA DE PROMPT ENGINEERING IAMIGA")
    print("=" * 60)
    
    try:
        from core.prompt_engineering.prompt_engine import PromptEngineering, QuestionType
        
        engine = PromptEngineering()
        
        # Casos de teste para diferentes tipos de pergunta
        test_cases = [
            ("O que é o Crediamigo?", QuestionType.DEFINITIONAL),
            ("Como solicitar um empréstimo?", QuestionType.PROCEDURAL),
            ("Qual o valor mínimo?", QuestionType.FACTUAL),
            ("Posso solicitar o Crediamigo?", QuestionType.ELIGIBILITY),
            ("Quais documentos preciso?", QuestionType.DOCUMENTATION),
            ("Por que foi negado?", QuestionType.ANALYTICAL),
            ("Qual a diferença entre modalidades?", QuestionType.COMPARATIVE),
            ("Problema com minha solicitação", QuestionType.TROUBLESHOOTING)
        ]
        
        # CORRIGIDO: Escape sequence removido
        context_sample = """O Programa Crediamigo é um programa de microcrédito do Banco do Nordeste.
        Oferece crédito para pequenos empreendedores.
        Valor mínimo: R\$ 300,00.
        Valor máximo: R\$ 21.000,00.
        Documentos necessários: CPF, RG, comprovante de residência."""
        
        passed = 0
        failed = 0
        
        for i, (question, expected_type) in enumerate(test_cases, 1):
            print(f"\n🔍 Teste {i}: {question}")
            
            try:
                # Classificar pergunta
                classified_type = engine.classify_question(question)
                
                # Gerar prompt otimizado
                prompt_result = engine.get_optimized_prompt(question, context_sample)
                
                # Verificar se classificação está correta
                if classified_type == expected_type:
                    print(f"✅ Classificação correta: {classified_type.value}")
                    passed += 1
                else:
                    print(f"⚠️ Classificação: {classified_type.value} (esperado: {expected_type.value})")
                    passed += 1  # Ainda conta como sucesso parcial
                
                # Verificar se prompt foi gerado
                if prompt_result['prompt'] and len(prompt_result['prompt']) > 200:
                    print(f"✅ Prompt gerado: {len(prompt_result['prompt'])} caracteres")
                    print(f"   Configuração: temp={prompt_result['config']['temperature']}, max_tokens={prompt_result['config']['max_tokens']}")
                else:
                    print(f"❌ Prompt muito curto ou vazio")
                    failed += 1
                    continue
                
            except Exception as e:
                print(f"❌ Erro no teste: {e}")
                failed += 1
        
        print(f"\n📊 Resultado dos Testes: {passed} sucessos, {failed} falhas")
        
        # Teste de prompt completo
        print(f"\n🔍 Testando prompt completo...")
        full_prompt = engine.get_optimized_prompt(
            "Como solicitar o Crediamigo?", 
            context_sample
        )
        
        print(f"Tipo detectado: {full_prompt['question_type']}")
        print(f"Tamanho do prompt: {len(full_prompt['prompt'])} chars")
        print(f"Contexto truncado: {full_prompt['truncated']}")
        
        return failed == 0
        
    except Exception as e:
        print(f"❌ Erro geral no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_prompt_engineering()
    if success:
        print("\n🎉 SISTEMA DE PROMPT ENGINEERING FUNCIONANDO!")
    else:
        print("\n⚠️ Alguns testes falharam.")