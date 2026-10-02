# Aula 4 — Contexto + interface web + demo (3h) · roteiro do instrutor

**Objetivo:** cada aluno sai com um assistente "sobre algo seu", rodando numa página web, e apresenta para a turma.
**Pré-requisito:** chat com memória da aula passada (Groq) funcionando.
**Entrega:** `contexto.txt` + `prompts.py` personalizados e `app.py` rodando.

---

## Alerta: o que muda no projeto dos alunos

| Arquivo | Muda? |
|---|---|
| `llm_memoria.py` | **Não muda.** Pode copiar o da aula passada |
| `.env` | Não muda. Copiar para a pasta nova |
| `prompts.py` | **Ganha** `NOME_ASSISTENTE` e a função `montar_sistema(contexto)` |
| `contexto.txt` / `contexto.py` | **Novos** |
| `chat_contexto.py` | Evolução do `chat_memoria.py` (o system agora vem do arquivo) |
| `app.py` | **Novo** — a interface web |
| `requirements.txt` | **Novo** — instala tudo com um comando |

Nada quebra: `perguntar(mensagens)` continua igual.

---

## Antes da aula

- [ ] Rodar o [`PASSO_A_PASSO.md`](./PASSO_A_PASSO.md) inteiro no seu computador
- [ ] Testar `python -m streamlit run app.py` na rede do local da aula
- [ ] Avisar a turma para trazer uma **ideia de tema** para o próprio assistente (loja, jogo, banda, curso, cidade)
- [ ] Ter a pasta `aula-groq-4` em `.zip` para distribuir (**sem** o seu `.env`)

---

## Tempo

| Bloco | Tempo | Tema |
|--:|--:|---|
| 0 | 15 min | Recap + o que vamos construir |
| 1 | 25 min | Ler arquivo com Python (`open`, `with`) |
| 2 | 25 min | Colocar o arquivo no prompt (`montar_sistema`) |
| — | 10 min | Intervalo |
| 3 | 15 min | Instalar Streamlit + "olá mundo" |
| 4 | 35 min | `app.py`: o chat no navegador |
| 5 | 20 min | Personalizar (tema de cada um) |
| 6 | 35 min | Demo day |

---

## Bloco 0 — Recap e destino (15)

1. Rodar o `chat_memoria.py` da aula passada e perguntar: **"Que horas o Café Python abre?"**
   O modelo não sabe (ou inventa). Perguntar à turma: *por quê?*
   > Ele só sabe o que aprendeu no treino. Não conhece o nosso negócio.
2. Mostrar o resultado final: `app.py` aberto no navegador respondendo sobre o café.
   > Hoje: o bot vai **ler um arquivo nosso** e ganhar **cara de site**.

---

## Bloco 1 — Ler arquivo (25)

Conceito novo: **abrir arquivo de texto**.

Ao vivo, num arquivo de rascunho:

```python
with open("contexto.txt", encoding="utf-8") as arquivo:
    texto = arquivo.read()

print(texto)
print(len(texto))
```

Pontos a explicar:
- `open(caminho)` abre o arquivo; `.read()` devolve o conteúdo como **uma string só**
- `with` fecha o arquivo sozinho no final do bloco
- `encoding="utf-8"` evita acentos quebrados no **Windows**
- O caminho é relativo à pasta onde o terminal está

Depois mostrar `contexto.py`:
- `try/except FileNotFoundError` (o mesmo `try/except` da Aula 2) → se o arquivo não existir, avisa e segue
- `LIMITE_CARACTERES` → o free tier da Groq tem limite de tokens; arquivo gigante estoura

**Teste:** `python contexto.py`. Depois renomear o arquivo de propósito → aparece o aviso, sem traceback.

---

## Bloco 2 — Contexto no prompt (25)

Ideia central (escrever no quadro):

> A IA não "lê" o arquivo sozinha. **Nós colamos o texto dentro da mensagem `system`.**

Mostrar `montar_sistema` em `prompts.py`:
- f-string grande com o personagem + as regras + o texto entre marcações
- A regra **"use APENAS… se não estiver no texto, diga que não sabe"** é o que evita inventar

Rodar `python prompts.py` para a turma **ver** o system pronto, com o texto dentro.

Depois `chat_contexto.py`: comparar com o `chat_memoria.py`. A única diferença real é `novo_historico()`, que lê o arquivo e monta o system.

**Teste em sala (3 perguntas):**

| Pergunta | Esperado |
|---|---|
| Que horas abre no sábado? | 8h às 14h |
| Cappuccino com leite de aveia? | R$ 11,50 (precisa somar!) |
| Vocês vendem pizza? | Não tem essa informação |

**Experimento rápido:** editar o `contexto.txt` (ex.: mudar o preço do expresso), digitar `recarregar`, perguntar de novo. O bot muda a resposta sem mexer em código.

> Isso tem nome no mercado: dar contexto ao modelo (a versão simples de **RAG**). Chatbots de empresa funcionam assim.

---

## Bloco 3 — Streamlit: primeiro contato (15)

```bat
python -m pip install -r requirements.txt
```

Explicar `requirements.txt`: a "lista de compras" do projeto.

"Olá mundo" ao vivo (arquivo de rascunho `ola.py`):

```python
import streamlit as st

st.title("Olá, Streamlit!")
nome = st.text_input("Seu nome")
if nome:
    st.write(f"Oi, {nome}!")
```

```bat
python -m streamlit run ola.py
```

Pontos:
- Roda com `streamlit run`, não com `python ola.py`
- Abre em `localhost:8501` (o "site" está no seu computador)
- **Cada interação roda o arquivo inteiro de novo**, de cima para baixo (mostrar digitando o nome)
- Ctrl + C no terminal para desligar
- No primeiro uso pode pedir e-mail: Enter

---

## Bloco 4 — `app.py` (35)

Construir junto, por partes, rodando a cada etapa:

1. **Título + `set_page_config`** → rodar
2. **`session_state`**
   > Como o arquivo roda de novo a cada clique, uma lista normal seria zerada. `st.session_state` é a "gaveta" que guarda o histórico entre as execuções.
3. **Desenhar o histórico** com `st.chat_message` (pulando o `system`)
4. **`st.chat_input`** → `append` do user → `perguntar(...)` → `append` do assistant
   Mesma ordem do chat de terminal da Aula 3
5. **`st.spinner`** ("Pensando...")
6. **Barra lateral:** botões Limpar e Recarregar (`st.rerun()` redesenha a página)

Reforçar o reaproveitamento:
> `app.py` importa `novo_historico` e `historico_para_envio` do `chat_contexto.py` e `perguntar` do `llm_memoria.py`. **Não reescrevemos a lógica — só trocamos o `input()`/`print()` por caixa de texto e balões.**

**Checkpoint:** as 3 perguntas do Bloco 2, agora no navegador.

---

## Bloco 5 — Personalização (20)

Cada aluno (ou dupla):
1. Reescreve o `contexto.txt` com o próprio tema (tópicos curtos, até ~2 páginas)
2. Ajusta `NOME_ASSISTENTE` e `SISTEMA` no `prompts.py`
3. Ajusta o `st.caption` no `app.py`
4. Prepara **3 perguntas** para o demo: 2 que estão no texto e 1 que **não** está

Circular pela sala. Erros comuns: terminal fora da pasta, `contexto.txt` salvo com outro nome, esquecer de recarregar.

---

## Bloco 6 — Demo day (35)

Cada aluno/dupla, **2–3 min**:
1. Qual é o tema do assistente
2. As 3 perguntas ao vivo (inclusive a que ele **não** deve saber)
3. Uma coisa que mudaria se tivesse mais tempo

Encerramento do curso (5 min):
- Linha do tempo: Colab → `if/else` → API → memória → contexto → site
- Próximos passos para quem quiser continuar: publicar no Streamlit Community Cloud, bot no Telegram, IA que usa ferramentas (function calling)

---

## Plano B

| Situação | Ajuste |
|---|---|
| Streamlit não instala (rede/lab) | Fazer o demo day com `chat_contexto.py` no terminal; a parte de contexto já é a entrega principal |
| Muitos `429` (limite Groq) | Diminuir o `contexto.txt`; perguntas mais curtas; cada aluno com a própria key |
| Turma rápida | Desafio: dois arquivos de contexto e um `st.selectbox` para escolher qual usar |
| Turma lenta | Pular o "olá mundo" e ir direto ao `app.py` pronto, explicando por partes |

---

## Critério de sucesso

- [ ] Explicar por que o bot "não sabia" antes e como o arquivo resolve
- [ ] Ler arquivo com `open`/`with`
- [ ] Bot recusa perguntas fora do contexto
- [ ] `app.py` rodando no navegador
- [ ] Cada aluno com tema próprio apresentado
