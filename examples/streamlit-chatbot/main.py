from openai import OpenAI

import os
from dotenv import load_dotenv
import streamlit as st

st.title("ChatGPT-like clone")
# Load environment variables from .env file
load_dotenv()

# Access the secret
secret_key = os.getenv("GITHUB_TOKEN")

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key= secret_key
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history in a bordered container
with st.container():
    st.subheader("Chat History")
    if not st.session_state.messages:
        st.info("No messages yet. Start the conversation!")
    else:
        for message in st.session_state.messages:
            with st.expander(f"{message['role'].capitalize()} says:"):
                st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
