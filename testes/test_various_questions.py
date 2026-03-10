# test_various_questions.py
import sys
sys.path.append('src')
from agent import answer_question

questions = [
    "O que é o Crediamigo?",
    "Como funciona a avaliação de crédito?",
    "Quais são os documentos necessários?",
    "Como fazer um empréstimo?",
    "o que é PNMPO?"
]

print("🧪 TESTANDO DIFERENTES PERGUNTAS COM BUSCA SEMÂNTICA")
print("=" * 60)

for i, question in enumerate(questions, 1):
    print(f"\n📝 Teste {i}: {question}")
    print("-" * 40)
    
    response = answer_question(question)
    print(f"Resposta: {response[:200]}...")
    
    print("\n" + "─" * 60)

print("\n✅ Todos os testes concluídos!")