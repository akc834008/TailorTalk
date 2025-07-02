# frontend/app.py
import streamlit as st
import requests

st.title("📅 TailorTalk - Calendar Booking Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.chat_input("Type your message...")


if user_input:
    st.session_state.chat.append(("You", user_input))
    response = requests.post("http://127.0.0.1:8000/chat", json={"message": user_input})
    reply = response.json()["response"]
    st.session_state.chat.append(("Bot", reply))

for sender, msg in st.session_state.chat:
    st.chat_message(sender).write(msg)
