# Passo a passo — Aula 4: assistente com contexto + interface web

Hoje o chatbot ganha duas coisas:
1. **Conhecimento próprio:** responde com base num arquivo `contexto.txt`
2. **Cara de site:** abre no navegador com o Streamlit

> **Windows:** use `python` (ou `py`) · **Mac:** use `python3`

---

## 1. O que você já precisa ter (das aulas anteriores)

- [ ] Python e VS Code instalados
- [ ] Key da Groq ([console.groq.com](https://console.groq.com))
- [ ] O chat com memória da aula passada funcionando

Nada de conta nova hoje. A única instalação nova é o **Streamlit**.

---

## 2. Abrir a pasta da aula

1. VS Code → **File → Open Folder…** → `aula-groq-4`
2. **Terminal → New Terminal**
3. Confira que o terminal está dentro de `aula-groq-4`

---

## 3. Instalar tudo de uma vez

Agora as bibliotecas estão listadas no arquivo `requirements.txt`. Um comando instala todas:

```bat
python -m pip install -r requirements.txt
```

```bash
python3 -m pip install -r requirements.txt
```

| Biblioteca | Para quê |
|---|---|
| `requests` | Chamar a API da Groq (já conhecida) |
| `python-dotenv` | Ler a key do `.env` (já conhecida) |
| `streamlit` | **Nova:** transformar o script em página web |

O Streamlit é maior; pode levar 1–2 minutos para instalar.

---

## 4. Colocar a key no `.env`

Copie o `.env` da aula passada para esta pasta, **ou** crie um novo (New File → `.env`):

```
GROQ_API_KEY=cole_sua_key_aqui
```

---

## 5. Testar na ordem

### 5.1 O arquivo de contexto é lido?

```bat
python contexto.py
```

Esperado: o texto do Café Python aparece, e no final `Total de caracteres: ...`.

### 5.2 A Groq ainda responde?

```bat
python llm_memoria.py
```

Esperado: uma frase curta dizendo oi.

### 5.3 Chat no terminal, agora com contexto

```bat
python chat_contexto.py
```

Faça estas perguntas:

```
você> Que horas abre no sábado?
você> Quanto custa um cappuccino com leite de aveia?
você> Vocês vendem pizza?
você> sair
```

| Pergunta | Esperado |
|---|---|
| Sábado | 8h às 14h |
| Cappuccino com aveia | R$ 11,50 (9,50 + 2,00) |
| Pizza | Diz que **não tem essa informação** (não pode inventar) |

### 5.4 A versão web

```bat
python -m streamlit run app.py
```

```bash
python3 -m streamlit run app.py
```

- O navegador abre sozinho em `http://localhost:8501` (se não abrir, copie esse endereço)
- Na **primeira vez**, o Streamlit pode pedir um e-mail no terminal: só aperte **Enter**
- Converse pela caixa de texto no rodapé da página
- Para desligar: volte ao terminal e aperte **Ctrl + C**

---

## 6. Deixar o assistente com a sua cara

1. Abra `contexto.txt` e troque o Café Python pelo **seu tema** (sua loja, seu jogo favorito, um curso, sua cidade…)
2. Abra `prompts.py` e ajuste `NOME_ASSISTENTE` e o texto de `SISTEMA`
3. No app, clique em **Recarregar contexto.txt** (ou pare com Ctrl + C e rode de novo)

Dica: escreva o `contexto.txt` em tópicos curtos. Até ~6.000 caracteres (umas 2 páginas).

---

## 7. Checklist

- [ ] `pip install -r requirements.txt` ok
- [ ] `.env` com a key nesta pasta
- [ ] `contexto.py` mostra o texto
- [ ] `chat_contexto.py` responde sobre o arquivo e recusa a pizza
- [ ] `streamlit run app.py` abre no navegador
- [ ] Meu próprio `contexto.txt` e `prompts.py`

---

## Se algo der errado

| Problema | Solução |
|---|---|
| `API key inválida ou ausente` | Abra o `.env`: tem que ter **um só** `GROQ_API_KEY=` seguido da key (`gsk_...`). Erro comum: `GROQ_API_KEY=GROQ_API_KEY=gsk_...` |
| `No module named streamlit` | Rode de novo o passo 3 |
| `'streamlit' não é reconhecido` | Use sempre `python -m streamlit run app.py` |
| Página não abre | Copie `http://localhost:8501` no navegador |
| Pede e-mail no terminal | Aperte Enter (é opcional) |
| `arquivo 'contexto.txt' não encontrado` | O terminal tem que estar na pasta `aula-groq-4` |
| Acentos estranhos no texto | Salve o `contexto.txt` em UTF-8 (padrão do VS Code) |
| Bot inventa coisas fora do texto | Reforce a regra no `prompts.py` ("use APENAS…") |
| Status `429` | Limite do free tier: espere 1 minuto · deixe o `contexto.txt` menor |
| Mudei o `contexto.txt` e nada mudou | Botão **Recarregar contexto.txt** ou reinicie o app |
