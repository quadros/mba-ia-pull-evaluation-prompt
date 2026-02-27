"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    username = os.getenv("USERNAME_LANGSMITH_HUB", "").strip()
    if not username:
        print("❌ USERNAME_LANGSMITH_HUB não configurado no .env")
        print("   Publique qualquer prompt no LangSmith Hub para gerar seu username,")
        print("   depois abra o prompt, clique no ícone de cadeado e copie o username.")
        return False

    system_prompt = prompt_data.get("system_prompt", "")
    user_prompt = prompt_data.get("user_prompt", "{bug_report}")
    few_shot_examples = prompt_data.get("few_shot_examples", [])

    # Construir mensagens: system + pares human/ai de few-shot + human final
    messages = [("system", system_prompt)]
    for example in few_shot_examples:
        messages.append(("human", example.get("input", "")))
        messages.append(("ai", example.get("output", "")))
    messages.append(("human", user_prompt))

    template = ChatPromptTemplate.from_messages(messages)

    full_name = f"{username}/{prompt_name}"
    print(f"Publicando: {full_name}")

    try:
        hub.push(
            full_name,
            template,
            new_repo_is_public=True,
        )
        print(f"✓ Prompt publicado com sucesso!")
        print(f"  URL: https://smith.langchain.com/hub/{full_name}")
        return True

    except Exception as e:
        print(f"❌ Erro ao fazer push do prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    for field in ["description", "system_prompt", "version"]:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório faltando: '{field}'")

    system_prompt = prompt_data.get("system_prompt", "").strip()
    if not system_prompt:
        errors.append("'system_prompt' está vazio")

    full_text = system_prompt + prompt_data.get("user_prompt", "")
    if "[TODO]" in full_text or "TODO" in full_text:
        errors.append("O prompt ainda contém marcadores TODO — remova-os antes de fazer push")

    techniques = prompt_data.get("techniques_applied", [])
    if len(techniques) < 2:
        errors.append(
            f"Mínimo de 2 técnicas em 'techniques_applied' — encontradas: {len(techniques)}"
        )

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DO PROMPT OTIMIZADO AO LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1

    input_file = "prompts/bug_to_user_story_v2.yml"
    prompt_key = "bug_to_user_story_v2"

    print(f"Carregando prompt de: {input_file}")
    yaml_data = load_yaml(input_file)

    if yaml_data is None:
        print(f"❌ Não foi possível carregar '{input_file}'")
        print("   Crie o arquivo 'prompts/bug_to_user_story_v2.yml' com o prompt otimizado.")
        return 1

    if prompt_key not in yaml_data:
        print(f"❌ Chave '{prompt_key}' não encontrada em '{input_file}'")
        return 1

    prompt_data = yaml_data[prompt_key]

    print("Validando prompt...")
    is_valid, errors = validate_prompt(prompt_data)

    if not is_valid:
        print("❌ Prompt inválido — corrija os erros antes de fazer push:")
        for error in errors:
            print(f"   • {error}")
        return 1

    print("✓ Validação OK")
    techniques = prompt_data.get("techniques_applied", [])
    print(f"  Versão: {prompt_data.get('version', '?')}")
    print(f"  Técnicas: {', '.join(techniques)}")

    success = push_prompt_to_langsmith(prompt_key, prompt_data)

    if success:
        print("\n✅ Push concluído com sucesso!")
        print("   Próximo passo: python src/evaluate.py")
        return 0
    else:
        print("\n❌ Push falhou. Verifique as mensagens de erro acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
