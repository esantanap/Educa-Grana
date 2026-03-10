# -*- coding: utf-8 -*-
"""
Teste do validador de persona IAmiga.
"""

import sys
sys.path.append('src')

def test_persona_validator():
    """Testa o validador de persona."""
    print("🧪 TESTANDO VALIDADOR DE PERSONA IAmiga")
    print("=" * 50)
    
    try:
        from core.persona.persona_validator import IAmigaPersona, validate_iamiga_response
        
        persona = IAmigaPersona()
        
        # Casos de teste
        test_cases = [
            # (resposta, pergunta, descrição, deve_ser_corrigida)
            (
                "O Crediamigo é um programa de microcrédito.",
                "O que é Crediamigo?",
                "Resposta básica sem persona",
                True
            ),
            (
                "😊 Olá! O Crediamigo é um programa de microcrédito do Banco do Nordeste. Posso ajudar com mais informações? 🤖 IAmiga",
                "O que é Crediamigo?",
                "Resposta com persona completa",
                False
            ),
            (
                "Como modelo de linguagem, não posso garantir informações sobre empréstimos.",
                "Como funciona?",
                "Resposta com exposição técnica",
                True
            ),
            (
                "Política é um assunto complexo que envolve muitas variáveis.",
                "O que acha da política?",
                "Resposta fora do escopo",
                True
            ),
            (
                "",
                "Pergunta qualquer",
                "Resposta vazia",
                True
            )
        ]
        
        passed = 0
        failed = 0
        
        for i, (response, question, description, should_be_corrected) in enumerate(test_cases, 1):
            print(f"\n🔍 Teste {i}: {description}")
            print(f"Entrada: '{response[:50]}{'...' if len(response) > 50 else ''}'")
            
            try:
                # Aplicar persona
                corrected, is_valid, violations = persona.apply_persona(response, question)
                
                # Verificar se foi corrigida conforme esperado
                was_corrected = corrected != response
                
                if was_corrected == should_be_corrected:
                    print(f"✅ Resultado esperado: {'Corrigida' if was_corrected else 'Não precisou correção'}")
                    if violations:
                        print(f"   Violações detectadas: {len(violations)}")
                    passed += 1
                else:
                    print(f"❌ Resultado inesperado: {'Corrigida' if was_corrected else 'Não corrigida'}")
                    print(f"   Esperado: {'Correção' if should_be_corrected else 'Sem correção'}")
                    failed += 1
                
                print(f"Saída: '{corrected[:100]}{'...' if len(corrected) > 100 else ''}'")
                
            except Exception as e:
                print(f"❌ Erro no teste: {e}")
                failed += 1
        
        print(f"\n📊 Resultado dos Testes: {passed} passou, {failed} falhou")
        
        # Teste da função de conveniência
        print(f"\n🔧 Testando função de conveniência...")
        corrected, is_valid = validate_iamiga_response("Teste simples", "Pergunta teste")
        print(f"✅ Função de conveniência: {'OK' if corrected else 'Falhou'}")
        
        return failed == 0
        
    except Exception as e:
        print(f"❌ Erro geral no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_persona_validator()
    if success:
        print("\n🎉 TODOS OS TESTES DO VALIDADOR PASSARAM!")
    else:
        print("\n⚠️ Alguns testes falharam.")