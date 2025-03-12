import streamlit as st
import openai
import os

from dotenv import load_dotenv

load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure you have set this in your environment variables

st.title("🤖 Streamlit OpenAI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Ask something...")
if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get AI response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Change to a different model if needed
        messages=st.session_state.messages
    )
    reply = response["choices"][0]["message"]["content"]
    
    # Append AI response
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
