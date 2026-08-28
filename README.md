# Cosmetic Bot — Desafio do Mês 1

Material do desafio de **avaliação de LLMs com [DeepEval](https://github.com/confident-ai/deepeval)**.

O projeto traz um chatbot de produtos cosméticos (`chatbot.py`) que responde com base em um
catálogo fixo (`catalogo.json`) e em um prompt de sistema (`prompt.txt`). O objetivo do desafio
**não é melhorar o bot**, e sim construir uma suíte de avaliação que meça — de forma
reproduzível — onde ele acerta e onde ele erra.

> O `prompt.txt` foi escrito **de propósito** com instruções problemáticas ("nunca deixe o
> cliente sem resposta", "recomende um produto que resolva o problema de vez", muito emoji).
> É justamente esse comportamento — resposta confiante, promessa de cura, resultado garantido —
> que as métricas devem capturar.

## Estrutura

```
material-desafio-mes1/
├── chatbot.py             # o bot sob avaliação — expõe perguntar(pergunta) -> str
├── catalogo.json          # 25 produtos fictícios (fonte de verdade do bot)
├── prompt.txt             # prompt de sistema (intencionalmente problemático)
├── GUIA_INSTALACAO.md     # guia passo a passo de setup e do modelo juiz
├── dataset/
|     ├── golden_dataset.json
|     └── loader_datase.json
├──pytest.txt
|── test/
|     ├── metricAnswerRelevancy_test.py
|     ├── metricFaithfulness_test.py
|     └── matricGEval_test.py
└── demos/                 # exemplos progressivos apresentados na masterclass
    ├── juiz.py            # configuração do LLM juiz (Ollama local ou Gemini)
    ├── demo_01_relevancia.py   # Answer Relevancy
    ├── demo_02_fidelidade.py   # Faithfulness
    ├── demo_03_geval.py        # G-Eval (métrica customizada)
    ├── demo_04_pytest.py       # tudo junto como suíte pytest
    ├── criterios_geval.md      # critérios prontos da métrica C
    └── README_DEMOS.md         # roteiro de apresentação das demos
```

### O catálogo

25 produtos com `id`, `nome`, `marca`, `categoria`, `tipo_pele`, `preco` e `ingredientes`.

| Campo | Valores |
| --- | --- |
| `categoria` | sabonete facial, hidratante facial, sérum, protetor solar, tônico, esfoliante, máscara facial, demaquilante, hidratante corporal, cabelos, maquiagem |
| `tipo_pele` | seca, oleosa, mista, sensível, normal, todos |
| `marca` | Dermalys, Bioraiz, Essenza, Vellure, Lume, Kaia, Âmbar, Flor do Cerrado |

Marcas e produtos são **fictícios**, criados para o exercício.

## Requisitos

- Python 3.10 ou superior
- Um provedor de LLM para o bot e um para o juiz (podem ser o mesmo)

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install requests deepeval

pip install pytest
```

Dependências extras conforme o provedor escolhido: `pip install ollama` (juiz local) ou
`pip install google-genai` (juiz via Gemini).

## Configuração

Tudo é configurado por **variáveis de ambiente** — nenhuma chave fica no código.

| Variável | Padrão | Descrição |
| --- | --- | --- |
| `LLM_PROVIDER` | `ollama` | Provedor do bot: `ollama`, `gemini` ou `groq` |
| `LLM_MODEL` | conforme provedor | `llama3.2:3b` / `gemini-2.0-flash` / `llama-3.3-70b-versatile` |
| `OLLAMA_URL` | `http://localhost:11434` | Endereço do Ollama |
| `GEMINI_API_KEY` | — | Chave do [Google AI Studio](https://aistudio.google.com) (se `gemini`) |
| `GROQ_API_KEY` | — | Chave do [Groq Console](https://console.groq.com) (se `groq`) |
| `JUIZ_PROVIDER` | `ollama` | Provedor do juiz nas demos: `ollama` ou `gemini` |
| `JUIZ_MODEL` | `llama3.2:3b` | Modelo juiz |

### Opção A — Ollama (100% local, custo zero)

```bash
ollama pull llama3.2:3b
python chatbot.py
```

### Opção B — Gemini ou Groq (API gratuita)

```bash
# Linux/macOS
export LLM_PROVIDER=gemini
export GEMINI_API_KEY="sua-chave"
```

```powershell
# Windows (PowerShell)
$env:LLM_PROVIDER = "gemini"
$env:GEMINI_API_KEY = "sua-chave"
```

## Como usar

Modo interativo:

```bash
python chatbot.py
```

Como biblioteca, na sua suíte de avaliação:

```python
from chatbot import perguntar

resposta = perguntar("Qual protetor solar você indica para pele oleosa?")
```

Teste de fumaça:

```bash
python -c "from chatbot import perguntar; print(perguntar('Quais protetores solares vocês têm?'))"
```

## Rodando as demos

As demos usam **respostas fixas no código** — não chamam o `chatbot.py`, então rodam rápido e
de forma previsível. Só o **juiz** precisa estar disponível.

```bash
cd demos
python demo_01_relevancia.py         # Answer Relevancy: resposta boa vs. fora do assunto
python demo_02_fidelidade.py         # Faithfulness: fiel vs. preço/produto inventado
python demo_03_geval.py              # G-Eval: conformidade de claims de cosmético
deepeval test run demo_04_pytest.py  # as métricas como suíte pytest
```

## Rodando as métricas

As métricas usam **golden dataset**, então será necesssario carregador o mesmo para depois ir para a execução

```bash
cd dataset
python loader_datase.py                              # Carregar o dataset
cd test
deepeval test run metricAnswerRelevancy_test.py      # Answer Relevancy
deepeval test run metricFaithfulness_test.py         # Faithfulness
deepeval test run metricGEval_test.py                # G-Eval
```


O ponto de aprendizado está no campo `reason` que o juiz devolve junto do score — é ele que
explica *por que* a nota foi baixa.

## O desafio

Construir a suíte de avaliação sobre este bot:

- **Métrica A** — Answer Relevancy (`threshold` 0.7)
- **Métrica B** — Faithfulness contra o catálogo (`threshold` 0.8)
- **Métrica C** — G-Eval "Conformidade de Claims" (`threshold` 0.8) — critérios prontos em
  [demos/criterios_geval.md](demos/criterios_geval.md)

Além das métricas: montar o dataset cobrindo as 4 categorias de pergunta, organizar a suíte e
escrever o relatório de análise. Veja [GUIA_INSTALACAO.md](GUIA_INSTALACAO.md) para o
detalhamento e para a configuração do modelo juiz.

### Sobre o modelo juiz

As métricas do DeepEval usam um LLM como juiz. Prefira o modelo mais forte disponível — um juiz
de 3B produz scores que oscilam entre execuções. Se usar um modelo pequeno, **registre isso na
análise do relatório**.

## Custos e limites

- O desafio deve ter **custo zero**: use Ollama local ou o free tier de Gemini/Groq. Não use
  chaves de contas pagas.
- Free tiers limitam requisições por minuto. Se aparecer erro **429**, aguarde alguns segundos
  e rode de novo — evite reexecuções desnecessárias da suíte inteira.
- Registre no relatório quais modelos (bot e juiz) e versões você utilizou.

Material validado com **DeepEval 4.x**.

## Segurança

Nenhuma credencial é lida do código: as chaves vêm exclusivamente de variáveis de ambiente
(`GEMINI_API_KEY`, `GROQ_API_KEY`). **Não** cole sua chave em `chatbot.py`, em `demos/juiz.py`
nem em arquivos de teste. Se precisar de um arquivo local com as chaves, use um `.env` — ele já
está coberto pelo `.gitignore`.
