import streamlit as st
import google.generativeai as genai

# 1. Cấu hình bảo mật - Lấy key từ Streamlit Secrets
# Bạn cần vào Settings -> Secrets trên Streamlit Cloud dán: GOOGLE_API_KEY = "MÃ_KEY_MỚI_CỦA_BẠN"
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Thiếu API Key! Vui lòng cấu hình GOOGLE_API_KEY trong phần Secrets của Streamlit.")
    st.stop()

# 2. Khởi tạo Model (Sử dụng dòng 1.5 mới nhất)
@st.cache_resource
def load_model():
    # Cấu hình vai trò giáo viên ngay từ đầu
    return genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        system_instruction="You are a friendly and helpful English teacher. Correct the student's grammar mistakes if any, then reply to their message in English."
    )

model = load_model()

# 3. Giao diện người dùng
st.set_page_config(page_title="AI Teacher", page_icon="🤖")
st.title("🤖 AI English Teacher")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your English teacher. Let's practice!"}]

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Xử lý tin nhắn
if prompt := st.chat_input("Type here..."):
    # Lưu và hiển thị tin nhắn user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gọi AI phản hồi
    with st.chat_message("assistant"):
        try:
            # Gửi tin nhắn và nhận phản hồi
            response = model.generate_content(prompt)
            ai_reply = response.text
            
            st.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
            # Tính năng phát âm (TTS)
            clean_reply = ai_reply.replace("'", "\\'").replace("\n", " ")
            st.components.v1.html(
                f"""<script>
                var msg = new SpeechSynthesisUtterance('{clean_reply}');
                msg.lang = 'en-US';
                window.speechSynthesis.speak(msg);
                </script>""", height=0
            )
        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {str(e)}")
            if "location" in str(e).lower():
                st.warning("Lưu ý: Khu vực của bạn hoặc Server Streamlit có thể đang bị Google giới hạn truy cập.")
