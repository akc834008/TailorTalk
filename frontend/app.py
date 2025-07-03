import streamlit as st
import requests

st.title("📅 TailorTalk - Calendar Booking Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat.append(("You", user_input))

    try:
        # ✅ Send request to deployed backend on Render
        response = requests.post(
            "https://tailortalk-zg9s.onrender.com/chat",
            json={"message": user_input},
            timeout=30
        )
        reply = response.json()["response"]
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    st.session_state.chat.append(("Bot", reply))

for sender, msg in st.session_state.chat:
    st.chat_message(sender).write(msg)
