import streamlit as st
import google.generativeai as genai

# 1. Cấu hình AI với API Key thực tế của bạn
genai.configure(api_key="AIzaSyCuPAHLEjbYVJxIq3FJr5IiMFhbTbgIIjs")
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Cấu hình giao diện (Chỉ gọi duy nhất 1 lần tại đây)
st.set_page_config(page_title="AI English Teacher", page_icon="🤖")
st.title("🤖 AI English Teacher")
st.markdown("Talk to me all day to improve your English! I will correct your grammar and speak to you.")

# 3. Khởi tạo lịch sử chat ban đầu nếu chưa có
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
    # Thêm và hiển thị tin nhắn của người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gọi AI phản hồi thực tế
    with st.chat_message("assistant"):
        try:
            # Gửi Prompt chuẩn dặn dò AI sửa lỗi ngữ pháp
            full_prompt = f"You are a friendly English teacher. Correct the user's grammar if it's wrong, then reply to their message in English: {prompt}"
            
            response = model.generate_content(full_prompt)
            ai_reply = response.text
            
            st.markdown(ai_reply)
            
            # Lưu câu trả lời của AI vào bộ nhớ lịch sử
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
            # Kích hoạt tính năng đọc âm thanh tiếng Anh qua trình duyệt điện thoại
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
