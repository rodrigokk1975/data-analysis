# PRD — Análise de Dados com Gráficos (Dataset Gapminder)

**Status:** Aprovado para Execução  
**Versão:** 1.0  
**Repositório:** `data-analysis`  
**Stack Principal:** Python 3.11+, pandas, Matplotlib, Seaborn, Jupyter Notebook  

---

## 1. Visão Geral e Objetivo

Construir um projeto completo, reproduzível e bem documentado de **análise exploratória de dados (EDA) com visualizações** utilizando um dataset público aberto. O projeto combina código Python modular e testável (`src/`) com uma narrativa interativa em notebook (`notebooks/`) e conclusões executivas ilustradas com gráficos de alta resolução no `README.md`.

### Público-Alvo
- Recrutadores técnicos e pares avaliando portfólio de análise de dados e engenharia analítica.
- Estudantes ou profissionais buscando uma referência limpa de pipeline de EDA reproduzível com versionamento disciplinado.

### Valor Entregue
- Pipeline reproduzível de ponta a ponta (download -> validação -> limpeza -> análise -> geração de gráficos) sem dependência de logins ou passos manuais.
- Visualizações claras, acessíveis e orientadas a perguntas concretas de análise.
- Histórico Git limpo e auditável, com **um commit atômico por etapa concluída**.

---

## 2. Perguntas de Análise

Toda a exploração, as métricas calculadas e os gráficos produzidos devem responder objetivamente às cinco perguntas abaixo:

1. **Evolução Temporal:** Como evoluiu a expectativa de vida global e por continente entre 1952 e 2007?
2. **Relação Renda vs. Longevidade:** Qual é a relação entre PIB per capita e expectativa de vida, e como ela se comporta em escala linear versus logarítmica?
3. **Maiores Avanços Relativos:** Quais continentes e países registraram o maior ganho absoluto e percentual em expectativa de vida e PIB per capita no período?
4. **Desigualdade Intra-Continental:** Como variou a dispersão (desigualdade) da expectativa de vida e da renda dentro de cada continente ao longo das décadas?
5. **Anomalias e Outliers Históricos:** Quais países apresentaram quedas abruptas ou saltos atípicos na série histórica (ex.: guerras, crises sanitárias ou boom econômico) e o que os dados revelam sobre esses eventos?

---

## 3. Dataset Público e Fonte dos Dados

- **Nome:** Gapminder Dataset (compilação histórica 1952–2007)
- **Origem:** Gapminder Foundation (repositório público estável `jennybc/gapminder`, arquivo `gapminder.tsv` / CSV derivado)
- **URL Pública Direta:** `https://raw.githubusercontent.com/jennybc/gapminder/main/inst/extdata/gapminder.tsv`
- **Licença:** CC-BY 4.0 (uso público aberto com atribuição)
- **Volumetria Esperada:** 1.704 registros, 142 países, 5 continentes, 12 recortes temporais (de 5 em 5 anos entre 1952 e 2007)

### Schema Esperado (`data/raw/gapminder.tsv`)

| Coluna | Tipo | Descrição | Regra de Validação |
| :--- | :--- | :--- | :--- |
| `country` | `string` | Nome do país | Não nulo, 142 valores únicos |
| `continent` | `string` | Continente (`Africa`, `Americas`, `Asia`, `Europe`, `Oceania`) | Não nulo, 5 valores únicos |
| `year` | `int64` | Ano da observação | Entre `1952` e `2007`, passo de 5 anos |
| `lifeExp` | `float64` | Expectativa de vida ao nascer (anos) | `> 0` e `< 100` |
| `pop` | `int64` | População total | `> 0` |
| `gdpPercap` | `float64` | PIB per capita (USD ajustado por PPP) | `> 0` |

### Política de Imutabilidade dos Dados
- `data/raw/` armazena exclusivamente o dado bruto baixado da fonte original e **nunca** é editado manualmente.
- Qualquer transformação, tipagem ou coluna derivada é salva em `data/processed/`.

---

## 4. Stack Tecnológica e Comandos Executáveis

### Dependências Principais
- **Linguagem:** Python `>= 3.11`
- **Manipulação de Dados:** `pandas`, `numpy`
- **Visualização:** `matplotlib`, `seaborn`
- **Notebook:** `jupyter`, `ipykernel`
- **Qualidade e Testes:** `pytest`, `ruff`

### Comandos Padrão do Projeto (Windows / PowerShell)

```powershell
# Criar e ativar ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt

# Executar pipeline completo (ingestão -> limpeza -> análise -> gráficos)
python -m src.main

# Executar notebook interativo
jupyter notebook notebooks/01_eda_gapminder.ipynb

# Executar testes automatizados
pytest -v

# Verificar formatação e lint
ruff check src tests
```

---

## 5. Arquitetura e Estrutura de Diretórios

```text
data-analysis/
├── PRD.md                           # Especificação e roadmap do projeto (este arquivo)
├── README.md                        # Conclusões documentadas, gráficos e guia de reprodução
├── requirements.txt                 # Dependências fixadas
├── pyproject.toml                   # Configuração de ruff e pytest
├── .gitignore                       # Exclusões de ambiente, cache e artefatos temporários
├── data/
│   ├── raw/                         # Dataset bruto imutável (gapminder.tsv)
│   └── processed/                   # Dataset limpo e enriquecido (gapminder_clean.csv)
├── src/
│   ├── __init__.py
│   ├── data_loader.py               # Download reproduzível e validação de schema
│   ├── data_cleaning.py             # Limpeza, checagem de qualidade e métricas derivadas
│   ├── analysis.py                  # Estatísticas descritivas, correlações, rankings e outliers
│   ├── visualizations.py            # Funções de geração e exportação de gráficos (Matplotlib/Seaborn)
│   └── main.py                      # Orquestrador CLI do pipeline completo
├── notebooks/
│   └── 01_eda_gapminder.ipynb       # Análise exploratória narrativa consumindo módulos de src/
├── outputs/
│   └── figures/                     # Gráficos exportados em PNG (300 DPI) usados no README
└── tests/
    ├── test_data_loader.py          # Testes de carregamento e validação de schema
    ├── test_data_cleaning.py        # Testes de limpeza e colunas derivadas
    └── test_analysis.py             # Testes de cálculos estatísticos e geração de gráficos
```

---

## 6. Padrões de Código, Visualização e Qualidade

### Código Python
- Seguir **PEP 8** verificado via `ruff`.
- Utilizar **type hints** nas assinaturas públicas em `src/`.
- Separar lógica de negócio (`src/`) da apresentação narrativa (`notebooks/`): o notebook importa funções de `src/` em vez de duplicar transformações.
- Funções puras e determinísticas sempre que possível (recebem `pd.DataFrame`, retornam `pd.DataFrame` ou `matplotlib.figure.Figure`).

Exemplo de estilo esperado:

```python
from pathlib import Path
import pandas as pd


def add_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona PIB total e década mantendo o DataFrame original intacto."""
    enriched = df.copy()
    enriched["gdp_total"] = enriched["gdpPercap"] * enriched["pop"]
    enriched["decade"] = (enriched["year"] // 10) * 10
    return enriched
```

### Visualizações (Matplotlib + Seaborn)
- **Identidade visual consistente:** tema `seaborn` limpo (`whitegrid` ou `ticks`), remoção de bordas superiores/direitas (`despine`), paleta acessível para daltonismo (`colorblind` / `viridis`).
- **Autoexplicativos:** todo gráfico deve conter título descritivo (com insight ou contexto), subtítulo quando útil, rótulos de eixos com unidade de medida e rodapé com a fonte (`Fonte: Gapminder (1952–2007)`).
- **Exportação:** salvar em `outputs/figures/` no formato `.png` com `dpi=300` e `bbox_inches="tight"`.
- **Conjunto mínimo de 5 gráficos:**
  1. `01_evolucao_expectativa_vida_continentes.png` — Série temporal (linhas) da expectativa de vida média ponderada/simples por continente (1952–2007).
  2. `02_pib_vs_expectativa_vida_2007.png` — Dispersão (scatter/bubble) em escala logarítmica para PIB per capita vs. expectativa de vida (tamanho por população, cor por continente).
  3. `03_distribuicao_expectativa_vida_decadas.png` — Boxplot / Violin plot comparando dispersão e desigualdade por continente em 1952 vs. 2007.
  4. `04_top_paises_ganho_expectativa_vida.png` — Gráfico de barras horizontais com os 10 países de maior ganho absoluto em expectativa de vida entre 1952 e 2007.
  5. `05_outliers_quedas_historicas.png` — Série temporal destacada evidenciando países com maiores quedas abruptas entre recortes consecutivos.

---

## 7. Estratégia de Testes e Verificação

- **Framework:** `pytest` executável via `pytest -v`.
- **Cobertura funcional mínima:**
  - `test_data_loader.py`: valida presença das 6 colunas obrigatórias, tipos esperados, ausência de nulos e erro explícito quando o schema é violado.
  - `test_data_cleaning.py`: valida cálculo correto de métricas derivadas (`gdp_total`, `decade`, variações por país) e ausência de duplicatas.
  - `test_analysis.py`: valida estatísticas agregadas por continente, cálculo de correlação (Pearson/Spearman), detecção de outliers e execução sem erros das funções de plotagem (backend `Agg` em modo headless).
- **Verificação do Notebook:** o notebook deve executar de cima a baixo (`Restart & Run All`) sem erros e com todas as saídas renderizadas.

---

## 8. Limites e Regras (Boundaries)

- **Sempre fazer:**
  - Executar `pytest` e `ruff check` antes de finalizar etapas que alteram código.
  - Realizar **exatamente um commit atômico ao concluir cada etapa** do roadmap abaixo, antes de iniciar a etapa seguinte.
  - Documentar limitações dos dados (ex.: recortes de 5 em 5 anos, ausência de dados pós-2007 no recorte clássico).
- **Perguntar antes:**
  - Trocar o dataset público definido na Seção 3.
  - Adicionar bibliotecas externas fora da stack acordada (ex.: Plotly, Streamlit, scikit-learn).
  - Alterar a ordem ou fundir etapas do roadmap.
- **Nunca fazer:**
  - Pular o commit de uma etapa ou acumular múltiplas etapas em um único commit.
  - Editar manualmente arquivos em `data/raw/`.
  - Commitar ambiente virtual (`.venv/`), caches (`__pycache__/`, `.pytest_cache/`, `.ipynb_checkpoints/`) ou credenciais.

---

## 9. Roadmap de Etapas e Política de Commits

### Regra de Versionamento por Etapa
- Cada etapa abaixo representa uma unidade fechada de entrega.
- Ao concluir todos os **Critérios de Aceite** e a **Verificação** de uma etapa, deve ser feito **um commit dedicado** seguindo [Conventional Commits](https://www.conventionalcommits.org/) em português.
- Nenhuma etapa seguinte deve começar com arquivos pendentes da etapa anterior no working tree (`git status` deve estar limpo após cada commit).

---

### Etapa 0 — Definição do PRD
- **Escopo:** Criar o documento de requisitos do produto (`PRD.md`) estabelecendo escopo, dataset, stack, padrões, etapas e política de commits.
- **Arquivos:** `PRD.md`
- **Critérios de Aceite:**
  - [ ] `PRD.md` presente na raiz do repositório contendo todas as seções obrigatórias (objetivo, perguntas, dataset, stack, estrutura, padrões, testes, limites, etapas e critérios de sucesso).
  - [ ] Política de 1 commit por etapa claramente especificada.
- **Verificação:** Revisão do documento e `git status`.
- **Commit:**
  ```bash
  git add PRD.md
  git commit -m "docs: adicionar PRD do projeto de análise de dados"
  ```

---

### Etapa 1 — Setup do Ambiente e Estrutura do Repositório
- **Escopo:** Configurar ambiente Python, arquivo de dependências, configuração de ferramentas (`ruff`, `pytest`), `.gitignore` e esqueleto de diretórios do projeto.
- **Arquivos:** `.gitignore`, `requirements.txt`, `pyproject.toml`, `src/__init__.py`, diretórios `data/raw/`, `data/processed/`, `notebooks/`, `outputs/figures/`, `tests/`
- **Critérios de Aceite:**
  - [ ] Ambiente virtual criado e dependências instaladas sem conflitos.
  - [ ] `.gitignore` ignora `.venv/`, `__pycache__/`, `.pytest_cache/`, `.ipynb_checkpoints/`.
  - [ ] `ruff check` e `pytest` executam sem erro de configuração.
- **Verificação:** `python -c "import pandas, matplotlib, seaborn; print('OK')"` e `ruff check .`.
- **Commit:**
  ```bash
  git add .gitignore requirements.txt pyproject.toml src/__init__.py
  git commit -m "chore: configurar ambiente Python e estrutura do projeto"
  ```

---

### Etapa 2 — Ingestão e Validação do Dataset Público
- **Escopo:** Implementar o módulo `src/data_loader.py` para baixar o dataset Gapminder de forma reproduzível (com cache local em `data/raw/gapminder.tsv`) e validar schema, tipos e integridade básica.
- **Arquivos:** `src/data_loader.py`, `data/raw/gapminder.tsv`, `tests/test_data_loader.py`
- **Critérios de Aceite:**
  - [ ] Download automático funciona sem credenciais e salva em `data/raw/gapminder.tsv`.
  - [ ] Validador verifica as 6 colunas obrigatórias, ausência de valores nulos e intervalos válidos.
  - [ ] Testes unitários em `tests/test_data_loader.py` passam 100%.
- **Verificação:** `pytest tests/test_data_loader.py -v` e `ruff check src tests`.
- **Commit:**
  ```bash
  git add src/data_loader.py data/raw/gapminder.tsv tests/test_data_loader.py
  git commit -m "feat(data): implementar ingestão e validação do dataset Gapminder"
  ```

---

### Etapa 3 — Limpeza, Enriquecimento e Qualidade dos Dados
- **Escopo:** Implementar `src/data_cleaning.py` para padronização de tipos, remoção/verificação de duplicatas, criação de métricas derivadas (`gdp_total`, `decade`, variação 1952–2007) e exportação para `data/processed/gapminder_clean.csv`.
- **Arquivos:** `src/data_cleaning.py`, `data/processed/gapminder_clean.csv`, `tests/test_data_cleaning.py`
- **Critérios de Aceite:**
  - [ ] Pipeline gera `data/processed/gapminder_clean.csv` sem alterar `data/raw/gapminder.tsv`.
  - [ ] Métricas derivadas calculadas corretamente e verificadas por testes unitários.
  - [ ] Relatório de qualidade (nulos, duplicatas, tipos) validado sem inconsistências.
- **Verificação:** `pytest tests/test_data_cleaning.py -v` e `ruff check src tests`.
- **Commit:**
  ```bash
  git add src/data_cleaning.py data/processed/gapminder_clean.csv tests/test_data_cleaning.py
  git commit -m "feat(data): adicionar pipeline de limpeza e métricas derivadas"
  ```

---

### Etapa 4 — Análise Exploratória (EDA) e Visualizações
- **Escopo:** Criar `src/visualizations.py` com funções reutilizáveis em Matplotlib + Seaborn para gerar os 5 gráficos definidos na Seção 6 e o notebook narrativo `notebooks/01_eda_gapminder.ipynb` respondendo às 5 perguntas de análise.
- **Arquivos:** `src/visualizations.py`, `notebooks/01_eda_gapminder.ipynb`, `outputs/figures/01_*.png` a `05_*.png`
- **Critérios de Aceite:**
  - [ ] Todos os 5 gráficos exportados em `outputs/figures/` em PNG 300 DPI com título, rótulos de eixos, legenda e fonte.
  - [ ] Notebook executa do início ao fim sem erros, intercalando código limpo, gráficos e interpretações em Markdown.
  - [ ] Visualizações seguem paleta acessível e hierarquia visual clara.
- **Verificação:** Execução completa do notebook e conferência visual dos 5 arquivos PNG em `outputs/figures/`.
- **Commit:**
  ```bash
  git add src/visualizations.py notebooks/01_eda_gapminder.ipynb outputs/figures/
  git commit -m "feat(eda): criar análise exploratória e gráficos com Matplotlib e Seaborn"
  ```

---

### Etapa 5 — Síntese Estatística, Orquestração CLI e Testes do Pipeline
- **Escopo:** Implementar `src/analysis.py` (tabelas-resumo por continente/década, correlações Pearson/Spearman, rankings e detecção de outliers), `src/main.py` (execução de ponta a ponta via CLI) e suíte `tests/test_analysis.py`.
- **Arquivos:** `src/analysis.py`, `src/main.py`, `tests/test_analysis.py`
- **Critérios de Aceite:**
  - [ ] `python -m src.main` executa todo o pipeline do zero (ingestão -> limpeza -> estatísticas -> gráficos) sem erro.
  - [ ] Toda a suíte `pytest -v` passa 100%.
  - [ ] `ruff check src tests` retorna 0 avisos/erros.
- **Verificação:** `python -m src.main && pytest -v && ruff check src tests`.
- **Commit:**
  ```bash
  git add src/analysis.py src/main.py tests/test_analysis.py
  git commit -m "feat(analysis): consolidar métricas estatísticas e testes do pipeline"
  ```

---

### Etapa 6 — Documentação de Conclusões e Portfólio (`README.md`)
- **Escopo:** Redigir o `README.md` final apresentando o contexto do projeto, as 5 perguntas respondidas com os gráficos incorporados de `outputs/figures/`, principais conclusões quantitativas, limitações metodológicas e instruções completas de reprodução.
- **Arquivos:** `README.md`
- **Critérios de Aceite:**
  - [ ] Todas as 5 perguntas da Seção 2 respondidas com números concretos e links/imagens dos gráficos gerados.
  - [ ] Seção dedicada a limitações e próximos passos.
  - [ ] Instruções de instalação e execução testadas e fiéis ao estado atual do repositório.
  - [ ] Todos os links relativos de imagens e arquivos no `README.md` são válidos.
- **Verificação:** Revisão do `README.md` renderizado e conferência do histórico de commits (`git log --oneline`).
- **Commit:**
  ```bash
  git add README.md
  git commit -m "docs: documentar conclusões, gráficos e guia de reprodução no README"
  ```

---

## 10. Critérios de Sucesso do Projeto

O projeto será considerado **concluído** quando todos os itens abaixo forem verdadeiros:

- [ ] Todas as 7 etapas (Etapa 0 a Etapa 6) concluídas na ordem especificada, com **7 commits atômicos correspondentes** no histórico Git (`git log --oneline`).
- [ ] Pipeline reproduzível de ponta a ponta com um único comando (`python -m src.main`).
- [ ] Notebook `notebooks/01_eda_gapminder.ipynb` executa sem erros do início ao fim.
- [ ] Pelo menos 5 gráficos de alta resolução (300 DPI) gerados e incorporados ao `README.md`.
- [ ] Suíte de testes (`pytest -v`) e linter (`ruff check src tests`) passando integralmente.
- [ ] Conclusões claras, embasadas nos dados e documentadas no `README.md`.
