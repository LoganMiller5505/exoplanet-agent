import streamlit as st
from core import ask

st.set_page_config(page_title="ExoQuery", page_icon="🪐")
st.title("ExoQuery")
st.caption("Ask about confirmed exoplanets from NASA's Exoplanet Archive.")

# How many prior user/assistant exchanges to send back to the model.
HISTORY_EXCHANGES = 3

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about a planet, star, or system"):
    with st.chat_message("user"):
        st.markdown(prompt)

    history = st.session_state.messages[-HISTORY_EXCHANGES * 2:]

    with st.chat_message("assistant"):
        try:
            with st.spinner("Querying the archive..."):
                response = ask(prompt, history=history)
        except Exception as e:
            st.error(f"Could not answer that: {e}")
            st.stop()
        st.markdown(response)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})
