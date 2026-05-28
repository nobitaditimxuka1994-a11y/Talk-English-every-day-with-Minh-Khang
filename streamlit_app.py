import streamlit as st
import google.generativeai as genai

# 1. Cấu hình API
genai.configure(api_key="AIzaSyCuPAHLEjbYVJxIq3FJr5IiMFhbTbgIIjs")

# SỬA: Thử dùng 'gemini-pro' để có độ ổn định cao nhất nếu flash bị 404
try:
    model = genai.GenerativeModel('gemini-pro')
except:
    model = genai.GenerativeModel('models/gemini-pro')

# 2. Giao diện
st.set_page_config(page_title="AI English Teacher", page_icon="🤖")
st.title("🤖 AI English Teacher")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your teacher. Let's talk!"}
    ]

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
            response = model.generate_content(f"You are an English teacher. Correct and reply: {prompt}")
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
            # Nếu vẫn lỗi 404, app sẽ hướng dẫn bạn cách khắc phục cuối cùng
            st.error(f"Lỗi kết nối: {str(e)}")
            st.info("Mẹo: Hãy kiểm tra file requirements.txt đã có 'google-generativeai>=0.5.0' chưa nhé!")
