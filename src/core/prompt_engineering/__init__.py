# src/core/prompt_engineering/__init__.py
"""
Sistema de Prompt Engineering para IAmiga - Educa Grana.
Versão simplificada sem validador.
"""

try:
    from .prompt_engine import PromptEngineering, QuestionType
    PROMPT_ENGINE_AVAILABLE = True
    print("✅ PromptEngineering carregado com sucesso")
except ImportError as e:
    PROMPT_ENGINE_AVAILABLE = False
    print(f"❌ Erro ao carregar PromptEngineering: {e}")
    # Criar classes vazias para evitar erros
    class PromptEngineering:
        pass
    class QuestionType:
        pass

# Exportar apenas o que está disponível
__all__ = ['PromptEngineering', 'QuestionType']