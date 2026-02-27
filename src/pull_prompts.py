"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_TO_PULL = "leonanluppi/bug_to_user_story_v1"
OUTPUT_FILE = "prompts/bug_to_user_story_v1.yml"


def pull_prompts_from_langsmith():
    """
    Faz pull do prompt ruim do LangSmith Hub e salva localmente.

    Returns:
        True se sucesso, False caso contrário
    """
    print_section_header("PULL DO PROMPT DO LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return False

    print(f"Fazendo pull: {PROMPT_TO_PULL}")

    try:
        prompt = hub.pull(PROMPT_TO_PULL)
    except Exception as e:
        print(f"❌ Erro ao fazer pull do prompt '{PROMPT_TO_PULL}': {e}")
        return False

    # Extrair mensagens do ChatPromptTemplate
    system_content = ""
    user_content = ""

    for message in prompt.messages:
        if not hasattr(message, "prompt"):
            continue
        template = message.prompt.template
        class_name = message.__class__.__name__.lower()
        if "system" in class_name:
            system_content = template
        elif "human" in class_name:
            user_content = template

    if not system_content and not user_content:
        # Fallback: usar repr para não perder o conteúdo
        print("⚠️  Não foi possível extrair mensagens estruturadas — usando formato bruto")
        system_content = str(prompt)

    print("✓ Prompt extraído com sucesso")
    print(f"  - System prompt: {len(system_content)} caracteres")
    print(f"  - User prompt:   {len(user_content)} caracteres")

    prompt_data = {
        "bug_to_user_story_v1": {
            "description": "Prompt inicial para converter relatos de bugs em User Stories (baixa qualidade)",
            "source": PROMPT_TO_PULL,
            "system_prompt": system_content,
            "user_prompt": user_content if user_content else "{bug_report}",
            "version": "v1",
            "tags": ["bug-analysis", "user-story", "product-management"],
        }
    }

    if save_yaml(prompt_data, OUTPUT_FILE):
        print(f"✓ Arquivo salvo em: {OUTPUT_FILE}")
        return True
    else:
        print(f"❌ Falha ao salvar arquivo: {OUTPUT_FILE}")
        return False


def main():
    """Função principal"""
    success = pull_prompts_from_langsmith()
    if success:
        print("\n✅ Pull concluído com sucesso!")
        print(f"   Próximo passo: analise o prompt em '{OUTPUT_FILE}'")
        print("   e crie sua versão otimizada em 'prompts/bug_to_user_story_v2.yml'")
        return 0
    else:
        print("\n❌ Pull falhou. Verifique as mensagens de erro acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
