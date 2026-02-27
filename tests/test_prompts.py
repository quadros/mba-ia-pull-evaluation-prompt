"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class TestPrompts:
    @pytest.fixture(autouse=True)
    def load_prompt_data(self):
        """Carrega os dados do prompt v2 antes de cada teste."""
        data = load_prompts(PROMPT_FILE)
        self.prompt = data[PROMPT_KEY]
        self.system_prompt = self.prompt.get("system_prompt", "")
        self.user_prompt = self.prompt.get("user_prompt", "")

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in self.prompt, \
            "Campo 'system_prompt' não encontrado no YAML"
        assert self.system_prompt.strip(), \
            "O campo 'system_prompt' está vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: 'Você é um Product Manager')."""
        role_keywords = ["você é", "voce é", "você é um", "you are", "product manager", "persona"]
        system_lower = self.system_prompt.lower()
        assert any(kw in system_lower for kw in role_keywords), \
            "O system_prompt deve definir uma persona explícita (ex: 'Você é um Product Manager')"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        format_keywords = [
            "markdown", "user story", "como ", "eu quero", "para que",
            "critérios de aceitação", "criterios de aceitacao",
            "dado que", "quando ", "então", "entao"
        ]
        system_lower = self.system_prompt.lower()
        assert any(kw in system_lower for kw in format_keywords), \
            "O system_prompt deve mencionar o formato esperado (Markdown, User Story, Gherkin, etc.)"

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        few_shot_indicators = [
            "exemplo", "example", "relato de bug:", "user story:",
            "critérios de aceitação:", "dado que estou", "como um"
        ]
        # Verifica no system_prompt E nos few_shot_examples (campo estruturado)
        search_text = self.system_prompt.lower()
        few_shot_examples = self.prompt.get("few_shot_examples", [])
        for ex in few_shot_examples:
            search_text += str(ex.get("input", "")).lower()
            search_text += str(ex.get("output", "")).lower()

        matches = [kw for kw in few_shot_indicators if kw in search_text]
        assert len(matches) >= 2, \
            f"O prompt deve conter exemplos Few-shot (em system_prompt ou few_shot_examples) — encontrados: {matches}"

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum [TODO] no texto."""
        full_text = self.system_prompt + self.user_prompt
        assert "[TODO]" not in full_text, \
            "Encontrado '[TODO]' no prompt — remova antes de publicar"
        assert "TODO" not in full_text, \
            "Encontrado 'TODO' no prompt — remova antes de publicar"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = self.prompt.get("techniques_applied", [])
        assert isinstance(techniques, list), \
            "O campo 'techniques_applied' deve ser uma lista"
        assert len(techniques) >= 2, \
            f"Mínimo de 2 técnicas requeridas em 'techniques_applied', encontradas: {len(techniques)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
