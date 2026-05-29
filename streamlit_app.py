import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang (Phải đặt ở đầu file)
st.set_page_config(page_title="AI Teacher", page_icon="🤖")

# 2. Cấu hình API Key bảo mật
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Thiếu API Key! Vui lòng vào: Settings -> Secrets và dán: GOOGLE_API_KEY = 'Mã_của_bạn'")
    st.stop()

API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

# 3. Khởi tạo Model với cơ chế xử lý lỗi chặt chẽ hơn
@st.cache_resource
def load_model():
    try:
        return genai.GenerativeModel(
            model_name="gemini-1.0-pro"
            system_instruction="You are a friendly and helpful English teacher. Correct the student's grammar mistakes if any, then reply to their message in English."
        )
    except Exception as e:
        st.error(f"Không thể khởi tạo AI: {e}")
        return None

model = load_model()

# 4. Giao diện người dùng
st.title("🤖 AI English Teacher")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your English teacher. Let's practice!"}]

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Xử lý tin nhắn
if prompt := st.chat_input("Type here..."):
    # Lưu và hiển thị tin nhắn user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gọi AI phản hồi
    with st.chat_message("assistant"):
        if model:
            try:
                # Tạo hiệu ứng đang xử lý
                with st.spinner("Teacher is thinking..."):
                    response = model.generate_content(prompt)
                    ai_reply = response.text
                
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
                # Tính năng phát âm (TTS) - Đã xử lý ký tự đặc biệt tốt hơn
                clean_reply = ai_reply.replace("'", "\\'").replace("\n", " ").replace("\r", "")
                st.components.v1.html(
                    f"""<script>
                    var msg = new SpeechSynthesisUtterance('{clean_reply}');
                    msg.lang = 'en-US';
                    window.speechSynthesis.speak(msg);
                    </script>""", height=0
                )
            except Exception as e:
                error_msg = str(e)
                st.error(f"Đã xảy ra lỗi: {error_msg}")
                if "404" in error_msg:
                    st.info("Mẹo: Hãy kiểm tra xem file requirements.txt đã có google-generativeai>=0.7.2 chưa.")
        else:
            st.error("Model chưa được tải thành công.")
