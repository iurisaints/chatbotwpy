# Códigos da pasta `aula-groq-4` — o que cada arquivo faz

Esta aula **reaproveita** o chat com memória da aula passada e adiciona:
- um arquivo de conhecimento (`contexto.txt`)
- uma interface web (`app.py`, com Streamlit)

---

## Visão geral

```
aula-groq-4/
├── .env.example        → modelo do .env (sem a key)
├── .gitignore          → não versionar .env e __pycache__
├── requirements.txt    → NOVO: lista de bibliotecas do projeto
├── llm_memoria.py      → igual à aula passada: perguntar(mensagens)
├── contexto.txt        → NOVO: o "conhecimento" do assistente
├── contexto.py         → NOVO: lê o contexto.txt
├── prompts.py          → personalidade + NOVO montar_sistema(contexto)
├── chat_contexto.py    → chat no terminal usando o contexto
├── app.py              → NOVO: o mesmo chat no navegador
├── PASSO_A_PASSO.md    → guia do aluno
├── ROTEIRO.md          → roteiro do instrutor
└── CODIGOS.md          → este arquivo
```

Como os arquivos se conectam:

```
contexto.txt ──► contexto.py ──► prompts.py (montar_sistema)
                                      │
                                      ▼
                     chat_contexto.py (novo_historico, historico_para_envio)
                        │                        │
              (terminal: input/print)    app.py (navegador: Streamlit)
                        │                        │
                        └──────► llm_memoria.py (perguntar) ──► Groq
```

---

## `requirements.txt`

```
requests
python-dotenv
streamlit
```

Lista o que o projeto precisa. Em vez de lembrar cada nome:

```bat
python -m pip install -r requirements.txt
```

É o jeito padrão de compartilhar projetos Python.

---

## `llm_memoria.py` (sem mudanças)

O mesmo da aula passada: recebe a lista de mensagens, chama a Groq (`openai/gpt-oss-20b`) e devolve o texto da resposta, ou uma mensagem de erro amigável (`401`, `429`, sem internet).

Ponto didático: **uma função bem feita não precisa mudar** quando o projeto cresce.

---

## `contexto.txt`

Texto comum, em tópicos, com tudo que o assistente deve "saber". No exemplo: horários, cardápio, preços, pagamento e delivery do fictício **Café Python**.

É o arquivo que cada aluno troca pelo próprio tema.

---

## `contexto.py`

```python
with open(caminho, encoding="utf-8") as arquivo:
    texto = arquivo.read().strip()
```

| Peça | O que faz |
|---|---|
| `open(caminho, encoding="utf-8")` | Abre o arquivo; `utf-8` garante acentos certos no Windows |
| `with ... as arquivo:` | Fecha o arquivo sozinho ao sair do bloco |
| `.read()` | Devolve o conteúdo inteiro como **uma string** |
| `.strip()` | Tira linhas em branco do começo e do fim |
| `except FileNotFoundError` | Se o arquivo não existir, avisa e devolve `""` (o bot segue sem contexto) |
| `LIMITE_CARACTERES = 6000` | Corta textos grandes: o free tier da Groq limita tokens por minuto |

Rodar sozinho (`python contexto.py`) mostra o texto lido e o tamanho.

---

## `prompts.py`

Agora tem três coisas:

- `NOME_ASSISTENTE`: o nome que aparece no terminal e no título da página
- `SISTEMA`: a personalidade (igual à aula passada)
- `montar_sistema(contexto)`: **o coração da aula**

```python
return f"""{SISTEMA}

Use APENAS as informações entre as marcações abaixo para responder.
Se a resposta não estiver no texto, diga que não tem essa informação ...

--- INÍCIO DAS INFORMAÇÕES ---
{contexto}
--- FIM DAS INFORMAÇÕES ---"""
```

A IA não abre arquivos sozinha: **nós colamos o texto dentro da mensagem `system`**. As marcações separam "regras" de "informações", e a frase "use APENAS" reduz respostas inventadas.

Se o contexto vier vazio, devolve só o `SISTEMA`.

---

## `chat_contexto.py`

Evolução do `chat_memoria.py`. O que mudou:

| Função / comando | O que faz |
|---|---|
| `novo_historico()` | Lê o arquivo, monta o system e devolve `[{"role": "system", ...}]` |
| `historico_para_envio()` | Igual à aula passada: system + últimas 20 mensagens |
| `limpar` | Zera a conversa (lê o arquivo de novo) |
| `recarregar` | Relê o `contexto.txt` depois de editar, sem fechar o programa |

O loop (`append` user → `perguntar` → `print` → `append` assistant) é o mesmo da Aula 3.

---

## `app.py` — Streamlit

Rodar com:

```bat
python -m streamlit run app.py
```

### A ideia que mais confunde: o arquivo roda de novo a cada clique

Toda vez que o usuário envia uma mensagem ou clica num botão, o Streamlit **executa o `app.py` inteiro, de cima para baixo**. Por isso uma variável comum (`historico = []`) seria zerada a cada mensagem.

A solução é o `st.session_state`, uma "gaveta" que sobrevive entre as execuções:

```python
if "historico" not in st.session_state:
    st.session_state.historico = novo_historico()
```

Só cria o histórico **na primeira vez**.

### Peças usadas

| Código | Na tela |
|---|---|
| `st.set_page_config(page_title=...)` | Título da aba do navegador |
| `st.title(...)` / `st.caption(...)` | Título e subtítulo da página |
| `st.sidebar` + `st.button(...)` | Barra lateral com os botões Limpar e Recarregar |
| `st.rerun()` | Redesenha a página na hora (depois de limpar) |
| `st.chat_message("user" / "assistant")` | Balão de conversa com ícone |
| `st.markdown(texto)` | Escreve o texto (aceita negrito, listas…) |
| `st.chat_input(...)` | Caixa de mensagem fixa no rodapé; devolve o texto ou `None` |
| `st.spinner("Pensando...")` | Animação enquanto espera a Groq |

### O fluxo de uma mensagem

1. Redesenha todas as mensagens antigas (pulando o `system`)
2. `st.chat_input` recebe a pergunta
3. `append` da mensagem do usuário + balão na tela
4. `perguntar(historico_para_envio(...))` com spinner
5. Balão da resposta + `append` da mensagem do assistente

É **exatamente** a lógica do chat de terminal. Só trocamos `input()` por `st.chat_input` e `print()` por `st.chat_message`.

### Reaproveitamento

```python
from chat_contexto import historico_para_envio, novo_historico
from llm_memoria import perguntar
```

Importar do `chat_contexto.py` funciona porque o `main()` dele está protegido por `if __name__ == "__main__":` — o chat de terminal não abre quando o `app.py` importa o arquivo.

---

## O que mudou desde a aula passada

| | Aula passada | Aula 4 |
|---|---|---|
| Conhecimento | Só o treino do modelo | + `contexto.txt` |
| System | Texto fixo | `montar_sistema(contexto)` |
| Interface | Terminal | Terminal **e** navegador |
| Instalação | `pip install requests python-dotenv` | `pip install -r requirements.txt` |
| `perguntar()` | `perguntar(mensagens)` | **igual** |
