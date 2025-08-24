import streamlit as st
import asyncio #lib para resolver o problema 'assincrono (ADK) vs sincrono (streamlit)', veja se faz sentido após alterações
from agent import remote_session, remote_app_sa, USER_ID

st.set_page_config(page_title="Doquinha", page_icon="🤖", layout="centered")

st.title("🤖 Doquinha")
st.caption("Pergunte algo sobre os projetos e o agente irá buscar a resposta!.")

# histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_session" not in st.session_state:
    st.session_state.agent_session = remote_session

# ações de UI
cols = st.columns(2)
with cols[0]:
    if st.button("🧹 Limpar conversa"):
        st.session_state.messages = []
        st.rerun()

# exibição das mensagens anteriores para contexto
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


async def responder(mensagem):
    resposta = ""
    async for evento in remote_app_sa.async_stream_query(
        user_id=USER_ID,
        session_id=remote_session["id"],
        message=mensagem
    ):
        try:
            texto = evento["content"]["parts"][0]["text"]
            resposta += texto
        except (KeyError, IndexError):
            pass
    return resposta


# Interface Streamlit

# Versao 1, pega e da uma resposta mais trabalhada.
prompt = st.chat_input("Digite sua pergunta")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # chamada assíncrona ao agente
    async def get_agent_response():
        response = await responder(prompt)
        return response

    response = asyncio.run(get_agent_response())

    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


# Versao 0, mais simples. Apenas le e responde em baixo
#st.title("Chat simples")

# msg = st.text_input("Mensagem")

# if st.button("Enviar") and msg:
#     resposta = asyncio.run(responder(msg))
#     st.write("Resposta:", resposta)