# app.py — o mesmo chatbot, agora com interface web (Streamlit)
# Rodar com:  python -m streamlit run app.py
import streamlit as st

from chat_contexto import historico_para_envio, novo_historico
from llm_memoria import perguntar
from prompts import NOME_ASSISTENTE

st.set_page_config(page_title=NOME_ASSISTENTE)
st.title(NOME_ASSISTENTE)
st.caption("Pergunte sobre horários, cardápio, preços e delivery.")

# O Streamlit roda o arquivo inteiro de novo a cada interação;
# session_state é o que sobrevive entre essas execuções.
if "historico" not in st.session_state:
    st.session_state.historico = novo_historico()

with st.sidebar:
    st.header("Opções")
    if st.button("Limpar conversa"):
        st.session_state.historico = novo_historico()
        st.rerun()
    if st.button("Recarregar contexto.txt"):
        st.session_state.historico = novo_historico()
        st.rerun()

for mensagem in st.session_state.historico:
    if mensagem["role"] == "system":
        continue
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

pergunta = st.chat_input("Digite sua pergunta...")

if pergunta:
    st.session_state.historico.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = perguntar(historico_para_envio(st.session_state.historico))
        st.markdown(resposta)

    st.session_state.historico.append({"role": "assistant", "content": resposta})
