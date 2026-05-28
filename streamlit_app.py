import streamlit as st
import google.generativeai as genai

# 1. Cấu hình API
genai.configure(api_key="AIzaSyCuPAHLEjbYVJxIq3FJr5IiMFhbTbgIIjs")

# Hàm tự động tìm model khả dụng để tránh lỗi 404
@st.cache_resource
def get_working_model():
    # Danh sách các tên model phổ biến
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for name in model_names:
        try:
            m = genai.GenerativeModel(name)
            # Thử tạo một nội dung nhỏ để kiểm tra model có thực sự chạy không
            m.generate_content("test", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    # Nếu không cái nào chạy, thử thêm tiền tố models/
    for name in model_names:
        try:
            m = genai.GenerativeModel(f"models/{name}")
            m.generate_content("test", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    return None

model = get_working_model()

st.set_page_config(page_title="AI Teacher", page_icon="🤖")
st.title("🤖 AI English Teacher")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am ready now. Let's talk!"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model is None:
            st.error("Google AI is currently unavailable in your region or API key. Please check Google AI Studio.")
        else:
            try:
                response = model.generate_content(f"You are an English teacher. Correct and reply in English: {prompt}")
                ai_reply = response.text
                st.markdown(ai_reply)
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
                # Phát âm
                st.components.v1.html(
                    f"""<script>
                    var msg = new SpeechSynthesisUtterance('{ai_reply.replace("'", "\\'")}');
                    msg.lang = 'en-US';
                    window.speechSynthesis.speak(msg);
                    </script>""", height=0
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")
