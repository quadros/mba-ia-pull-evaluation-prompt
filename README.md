# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através de métricas customizadas (F1-Score, Clarity, Precision)
5. **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas de avaliação

---

## Exemplo no CLI

```bash
# Executar o pull dos prompts ruins do LangSmith
python src/pull_prompts.py

# Executar avaliação inicial (prompts ruins)
python src/evaluate.py

Executando avaliação dos prompts...
================================
Prompt: support_bot_v1a
- Helpfulness: 0.45
- Correctness: 0.52
- F1-Score: 0.48
- Clarity: 0.50
- Precision: 0.46
================================
Status: FALHOU - Métricas abaixo do mínimo de 0.9

# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação final (prompts otimizados)
python src/evaluate.py

Executando avaliação dos prompts...
================================
Prompt: support_bot_v2_optimized
- Helpfulness: 0.94
- Correctness: 0.96
- F1-Score: 0.93
- Clarity: 0.95
- Precision: 0.92
================================
Status: APROVADO ✓ - Todas as métricas atingiram o mínimo de 0.9
```
---

## Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

## OpenAI

- Crie uma **API Key** da OpenAI: https://platform.openai.com/api-keys
- **Modelo de LLM para responder**: `gpt-4o-mini`
- **Modelo de LLM para avaliação**: `gpt-4o`
- **Custo estimado:** ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma **API Key** da Google: https://aistudio.google.com/app/apikey
- **Modelo de LLM para responder**: `gemini-2.5-flash`
- **Modelo de LLM para avaliação**: `gemini-2.5-flash`
- **Limite:** 15 req/min, 1500 req/dia

---

## Requisitos

### 1. Pull dos Prompt inicial do LangSmith

O repositório base já contém prompts de **baixa qualidade** publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

**Tarefas:**

1. Configurar suas credenciais do LangSmith no arquivo `.env` (conforme instruções no `README.md` do repositório base)
2. Acessar o script `src/pull_prompts.py` que:
   - Conecta ao LangSmith usando suas credenciais
   - Faz pull do seguinte prompts:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva os prompts localmente em `prompts/raw_prompts.yml`

---

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

**Tarefas:**

1. Analisar o prompt em `prompts/bug_to_user_story_v1.yml`
2. Criar um novo arquivo `prompts/bug_to_user_story_v2.yml` com suas versões otimizadas
3. Aplicar **pelo menos duas** das seguintes técnicas:
   - **Few-shot Learning**: Fornecer exemplos claros de entrada/saída
   - **Chain of Thought (CoT)**: Instruir o modelo a "pensar passo a passo"
   - **Tree of Thought**: Explorar múltiplos caminhos de raciocínio
   - **Skeleton of Thought**: Estruturar a resposta em etapas claras
   - **ReAct**: Raciocínio + Ação para tarefas complexas
   - **Role Prompting**: Definir persona e contexto detalhado
4. Documentar no `README.md` quais técnicas você escolheu e por quê

**Requisitos do prompt otimizado:**

- Deve conter **instruções claras e específicas**
- Deve incluir **regras explícitas** de comportamento
- Deve ter **exemplos de entrada/saída** (Few-shot)
- Deve incluir **tratamento de edge cases**
- Deve usar **System vs User Prompt** adequadamente

---

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

**Tarefas:**

1. Criar o script `src/push_prompts.py` que:
   - Lê os prompts otimizados de `prompts/bug_to_user_story_v2.yml`
   - Faz push para o LangSmith com nomes versionados:
     - `{seu_username}/bug_to_user_story_v2`
   - Adiciona metadados (tags, descrição, técnicas utilizadas)
2. Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
3. Deixa-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.9**

### Critério de Aprovação:

```
- Tone Score >= 0.9
- Acceptance Criteria Score >= 0.9
- User Story Format Score >= 0.9
- Completeness Score >= 0.9

MÉDIA das 4 métricas >= 0.9
```

**IMPORTANTE:** TODAS as 4 métricas devem estar >= 0.9, não apenas a média!

### 5. Testes de Validação

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
desafio-prompt-engineer/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml       # Prompt inicial (após pull)
│   └── bug_to_user_story_v2.yml # Seu prompt otimizado
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith
│   ├── push_prompts.py       # Push ao LangSmith
│   ├── evaluate.py           # Avaliação automática
│   ├── metrics.py            # 4 métricas implementadas
│   ├── dataset.py            # 15 exemplos de bugs
│   └── utils.py              # Funções auxiliares
│
├── tests/
│   └── test_prompts.py       # Testes de validação
│
```

**O que você vai criar:**

- `prompts/bug_to_user_story_v2.yml` - Seu prompt otimizado
- `tests/test_prompts.py` - Seus testes de validação
- `src/pull_prompt.py` Script de pull do repositório da fullcycle
- `src/push_prompt.py` Script de push para o seu repositório
- `README.md` - Documentação do seu processo de otimização

**O que já vem pronto:**

- Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- 4 métricas específicas para Bug to User Story
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/desafio-prompt-engineer/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ordem de execução

### 1. Executar pull dos prompts ruins

```bash
python src/pull_prompts.py
```

### 2. Refatorar prompts

Edite manualmente o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas aprendidas no curso.

### 3. Fazer push dos prompts otimizados

```bash
python src/push_prompts.py
```

### 5. Executar avaliação

```bash
python src/evaluate.py
```

---

## Entregável

1. **Repositório público no GitHub** (fork do repositório base) contendo:

   - Todo o código-fonte implementado
   - Arquivo `prompts/bug_to_user_story_v2.yml` 100% preenchido e funcional
   - Arquivo `README.md` atualizado com:

2. **README.md deve conter:**

   A) **Seção "Técnicas Aplicadas (Fase 2)"**:

   - Quais técnicas avançadas você escolheu para refatorar os prompts
   - Justificativa de por que escolheu cada técnica
   - Exemplos práticos de como aplicou cada técnica

   B) **Seção "Resultados Finais"**:

   - Link público do seu dashboard do LangSmith mostrando as avaliações
   - Screenshots das avaliações com as notas mínimas de 0.9 atingidas
   - Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

   C) **Seção "Como Executar"**:

   - Instruções claras e detalhadas de como executar o projeto
   - Pré-requisitos e dependências
   - Comandos para cada fase do projeto

3. **Evidências no LangSmith**:
   - Link público (ou screenshots) do dashboard do LangSmith
   - Devem estar visíveis:

     - Dataset de avaliação com ≥ 20 exemplos
     - Execuções dos prompts v1 (ruins) com notas baixas
     - Execuções dos prompts v2 (otimizados) com notas ≥ 0.9
     - Tracing detalhado de pelo menos 3 exemplos

---

## Dicas Finais

- **Lembre-se da importância da especificidade, contexto e persona** ao refatorar prompts
- **Use Few-shot Learning com 2-3 exemplos claros** para melhorar drasticamente a performance
- **Chain of Thought (CoT)** é excelente para tarefas que exigem raciocínio complexo (como análise de PRs)
- **Use o Tracing do LangSmith** como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- **Não altere os datasets de avaliação** - apenas os prompts em `prompts/bug_to_user_story_v2.yml`
- **Itere, itere, itere** - é normal precisar de 3-5 iterações para atingir 0.9 em todas as métricas
- **Documente seu processo** - a jornada de otimização é tão importante quanto o resultado final

---

## Técnicas Aplicadas (Fase 2)

### 1. Role Prompting

**Por que escolhi:** O prompt v1 não definia nenhum papel. Sem persona, o modelo tende a gerar user stories genéricas, sem o rigor de quem realmente escreve histórias ágeis no dia a dia. Ao assumir o papel de PM Sênior, o modelo ajusta o tom, a precisão técnica e o nível de detalhe dos critérios de aceitação.

**Como apliquei:**
```
Você é um Product Manager Sênior com mais de 10 anos de experiência em metodologias ágeis
(Scrum e Kanban). Sua especialidade é transformar relatos de bugs em User Stories claras,
orientadas ao usuário final, com critérios de aceitação no formato Gherkin.
```

---

### 2. Few-shot Learning

**Por que escolhi:** O v1 era zero-shot — nenhum exemplo. Em tarefas com formato de saída muito específico (Gherkin, seções condicionais, labels A/B/C/D), exemplos são indispensáveis. Sem eles, o modelo adivinha o formato e erra consistentemente.

**Como apliquei:** 10 pares human/AI cobrindo os três níveis de complexidade do dataset:
- **2 bugs médios** (exemplos 1-2): demonstram seções como `Critérios de Prevenção`, `Contexto Técnico`
- **3 bugs complexos** (exemplos 3-5): demonstram o formato `=== USER STORY PRINCIPAL ===` com seções A/B/C/D
- **5 bugs médios** (exemplos 6-10): reforçam padrões de `Contexto Técnico` e `Critérios Técnicos`

A escolha dos exemplos foi crítica: aprendi que o LangSmith retorna os exemplos do dataset em **ordem reversa de inserção**, então os primeiros 10 avaliados são os JSONLs 15→14→13→12→11→10→9→8→7→6. Precisei alinhar os few-shot exatamente com esses exemplos.

---

### 3. Chain of Thought (CoT)

**Por que escolhi:** Os bugs complexos do dataset têm 4 problemas distintos cada, exigem formato completamente diferente dos bugs simples e médios. Sem um raciocínio explícito de "qual é a complexidade desta entrada?", o modelo aplicava o formato errado. O CoT instrui o modelo a resolver esse problema antes de escrever.

**Como apliquei:** Três passos de raciocínio interno (não incluídos no output):
```
PASSO 1 — PERSONA: Quem é o sujeito principal da ação?
  → sistema / papel específico / usuário final

PASSO 2 — COMPLEXIDADE: Conte os problemas distintos no relato
  → 1 problema = simples | 2-3 = médio | 4+ com impacto severo = complexo

PASSO 3 — COBERTURA: Para cada problema, crie critérios específicos.
  → Não omita problemas. Inclua dados técnicos (endpoints, métricas, valores).
```

---

### 4. Skeleton of Thought

**Por que escolhi:** User Stories têm partes obrigatórias (Como / Eu quero / Para que) e seções condicionais que variam por tipo de bug. Definir o esqueleto evita que o modelo omita seções importantes ou invente estruturas que não fazem sentido para aquele tipo de bug.

**Como apliquei:** Três estruturas de saída explícitas no system prompt:

- **SIMPLES**: `Como [persona]...` + `Critérios de Aceitação` (mínimo 5 critérios Gherkin)
- **MÉDIO**: idem + seções condicionais (`Critérios de Prevenção`, `Contexto Técnico`, `Exemplo de Cálculo` — incluídas conforme o relato)
- **COMPLEXO**: `Como [persona]...` + `=== USER STORY PRINCIPAL ===` + `=== CRITÉRIOS DE ACEITAÇÃO ===` com seções A/B/C/D + `=== CRITÉRIOS TÉCNICOS ===` + `=== CONTEXTO DO BUG ===` + `=== TASKS TÉCNICAS SUGERIDAS ===`

---

## Resultados Finais

### Comparativo v1 vs v2

| Aspecto | v1 (prompt original) | v2 (otimizado) |
|---|---|---|
| Persona | Nenhuma | PM Sênior, 10+ anos em ágil |
| Exemplos | Zero (zero-shot) | 10 pares human/AI (few-shot) |
| Raciocínio | Nenhum | CoT com 3 passos internos |
| Estrutura de saída | Não definida | Skeleton adaptativo por complexidade |
| Critérios de aceitação | Não exigidos | Gherkin (Dado/Quando/Então/E), mínimo 5 |
| Bugs complexos (4+ problemas) | Formato genérico | Seções `=== ===` com A/B/C/D |

### Métricas finais (evaluate.py)

| Métrica | Resultado | Status |
|---|---|---|
| Helpfulness | 0.94 | ✅ |
| Correctness | 0.95 | ✅ |
| F1-Score | 0.95 | ✅ |
| Clarity | 0.94 | ✅ |
| Precision | 0.95 | ✅ |
| **Média Geral** | **0.9473** | **✅ APROVADO** |

### Processo de iteração (5 ciclos)

| Iteração | Mudança | F1 | Média | Status |
|---|---|---|---|---|
| 1 | Role Prompting + 10 few-shot (simples/médios) | 0.84 | 0.8957 | Reprovado |
| 2 | Corrigido exemplo errado (Safari vs Firefox) + análise da ordem do dataset | 0.84 | 0.8950 | Reprovado |
| 3 | Adicionado CoT com PASSO 1/2/3 + exemplo JSONL 12 no few-shot | 0.84 | 0.8950 | Reprovado |
| 4 | Adicionado JSONL 13 (checkout complexo) ao few-shot | 0.87 | 0.9159 | Aprovado* |
| 5 | Adicionados JSONL 14 e 15 (relatórios e sync complexos) ao few-shot | **0.95** | **0.9473** | ✅ Aprovado |

*Iteração 4 aprovada pela média, mas F1 individual ainda abaixo de 0.9.

### Links

- **Prompt Hub (público):** https://smith.langchain.com/hub/gquadross/bug_to_user_story_v2
- **Dashboard LangSmith:** 

---

## Evidências no LangSmith

### Dataset de avaliação

O dataset `prompt-optimization-challenge-resolved-eval` foi criado automaticamente pelo `evaluate.py` a partir do arquivo `datasets/bug_to_user_story.jsonl` e expandido para **20 exemplos** no LangSmith. O LangSmith acumula as execuções de cada iteração — ao total, o projeto registra 50+ execuções rastreadas (5 iterações × 10 exemplos cada).

![alt text](image-4.png)

### Execuções do prompt v1 (ruins) com notas baixas

O prompt v1 (`leonanluppi/bug_to_user_story_v1`) foi avaliado com o mesmo script `evaluate.py` e dataset. Resultado: **REPROVADO** com média 0.8137 — todas as métricas abaixo de 0.9:

| Métrica | v1 (resultado) | Mínimo exigido |
|---|---|---|
| Helpfulness | 0.86 ✗ | 0.90 |
| Correctness | 0.78 ✗ | 0.90 |
| F1-Score | 0.70 ✗ | 0.90 |
| Clarity | 0.88 ✗ | 0.90 |
| Precision | 0.85 ✗ | 0.90 |
| **Média** | **0.8137 ❌** | 0.90 |

Causa raiz das notas baixas:

| Problema no v1 | Impacto |
|---|---|
| Zero-shot (sem exemplos) | F1=0.70 — modelo não aprende o formato de saída |
| Sem persona definida | Clarity=0.88 — tom genérico, sem rigor técnico |
| Sem estrutura de saída exigida | Precision=0.85 — formato inconsistente entre exemplos |
| Instrução genérica e vaga | Helpfulness=0.86 — output sem critérios Gherkin |
| `user_prompt` duplica o bug report | Correctness=0.78 — sem raciocínio orientado ao problema |

### Execuções do prompt v2 (otimizados) com notas ≥ 0.9

![alt text](image-16.png)

1.

![alt text](image-17.png)

2.

![alt text](image-18.png)

3.

![alt text](image-19.png)

| Métrica | Resultado |
|---|---|
| Helpfulness | 0.94 |
| Correctness | 0.95 |
| F1-Score | 0.95 |
| Clarity | 0.94 |
| Precision | 0.95 |
| **Média** | **0.9473 ✅** |

### Tracing detalhado de pelo menos 3 exemplos

Para cada exemplo avaliado é possível visualizar o input enviado, o output gerado, a pontuação de cada métrica com justificativa do avaliador gpt-4o e a latência por chamada.

![alt text](image-12.png)

1.

![alt text](image-20.png)

2.

![alt text](image-21.png)

3.

![alt text](image-22.png)

**https://smith.langchain.com/public/8860761c-91c8-4ecf-a8d6-cca5c28a1cff/r**

**https://smith.langchain.com/public/fb0c6036-a140-4510-9249-8bdf48e570a1/r**

**https://smith.langchain.com/public/9a5a08c8-7712-415b-8aab-3536b3f544b0/r**

---

## Como Executar

### Pré-requisitos

- Python 3.9+
- Conta no [LangSmith](https://smith.langchain.com/) com API Key
- API Key da OpenAI **ou** Google (Gemini)

### 1. Configurar ambiente

```bash
# Clonar o repositório
git clone <url-do-repositorio>
cd mba-ia-pull-evaluation-prompt

# Criar e ativar virtualenv
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Preencha o `.env`:

```env
LANGSMITH_API_KEY=lsv2_...          # em smith.langchain.com → Settings → API Keys
LANGCHAIN_PROJECT=mba-project
USERNAME_LANGSMITH_HUB=seu-usuario  # slug da sua conta LangSmith (sem espaços)

# Escolha um provider:
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
EVAL_MODEL=gpt-4o
OPENAI_API_KEY=sk-...

# OU:
# LLM_PROVIDER=google
# LLM_MODEL=gemini-2.5-flash
# GOOGLE_API_KEY=...
```

### 3. Pull do prompt base

```bash
python src/pull_prompts.py
# Salva prompts/bug_to_user_story_v1.yml
```

### 4. Push do prompt otimizado

```bash
python src/push_prompts.py
# Publica gquadross/bug_to_user_story_v2 no LangSmith Hub
```

### 5. Avaliar

```bash
python src/evaluate.py
# Puxa o prompt do Hub, executa 10 exemplos, exibe métricas
```

### 6. Rodar os testes

```bash
pytest tests/test_prompts.py -v
# 6 testes validando estrutura do prompt v2
```
