import streamlit as st
import google.generativeai as genai

# 1. Cấu hình API
genai.configure(api_key="AIzaSyCuPAHLEjbYVJxIq3FJr5IiMFhbTbgIIjs")

# SỬA: Dùng bản -latest để server tự chọn bản ổn định nhất
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.set_page_config(page_title="AI English Teacher", page_icon="🤖")
st.title("🤖 AI English Teacher")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm ready. Let's talk!"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Gửi tin nhắn cho AI
            response = model.generate_content(f"You are an English teacher. Correct and reply in English: {prompt}")
            ai_reply = response.text
            st.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
            # Đọc thành tiếng
            st.components.v1.html(
                f"""<script>
                var msg = new SpeechSynthesisUtterance('{ai_reply.replace("'", "\\'")}');
                msg.lang = 'en-US';
                window.speechSynthesis.speak(msg);
                </script>""", height=0
            )
        except Exception as e:
            st.error(f"Lỗi: {str(e)}")
