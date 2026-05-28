import streamlit as st
import google.generativeai as genai

# 1. Cấu hình AI với API Key của bạn
genai.configure(api_key="AIzaSyCuPAHLEjbYVJxIq3FJr5IiMFhbTbgIIjs")

# SỬA Ở ĐÂY: Thêm tiền tố models/ để tránh lỗi 404 trên Streamlit Cloud
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 2. Cấu hình giao diện
st.set_page_config(page_title="AI English Teacher", page_icon="🤖")
st.title("🤖 AI English Teacher")
st.markdown("Talk to me all day to improve your English! I will correct your grammar and speak to you.")

# 3. Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your English teacher. Let's talk about anything you like!"}
    ]

# 4. Hiển thị lại toàn bộ các tin nhắn cũ lên màn hình
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Xử lý khi người dùng nhập câu chat và nhấn Gửi
if prompt := st.chat_input("Talk to me in English..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gọi AI phản hồi thực tế
    with st.chat_message("assistant"):
        try:
            full_prompt = f"You are a friendly English teacher. Correct the user's grammar if it's wrong, then reply to their message in English: {prompt}"
            
            response = model.generate_content(full_prompt)
            ai_reply = response.text
            
            st.markdown(ai_reply)
            
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
            # Tính năng phát âm qua trình duyệt điện thoại
            st.components.v1.html(
                f"""
                <script>
                var msg = new SpeechSynthesisUtterance('{ai_reply.replace("'", "\\'").replace("\n", " ")}');
                msg.lang = 'en-US';
                window.speechSynthesis.speak(msg);
                </script>
                """,
                height=0,
            )
        except Exception as e:
            st.error(f"Something went wrong with AI: {str(e)}")
