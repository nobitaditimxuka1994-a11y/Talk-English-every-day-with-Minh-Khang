import streamlit as st
import google.generativeai as genai

st.title("🤖 AI English Teacher")

# Lấy Key từ Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Chưa có API Key trong Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Say something..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # Prompt đơn giản để AI không bị quá tải
        response = model.generate_content(f"You are an English teacher. Correct and reply: {prompt}")
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        st.error(f"Lỗi: {str(e)}")
