import streamlit as st
import streamlit as st
import google.generativeai as genai

# 1. Cấu hình AI (Dán API Key của bạn vào đây)
genai.configure(api_key="THAY_API_KEY_CUA_BAN_TAI_DAY")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AI English Teacher", page_icon="🤖")
st.title("🤖 AI English Teacher")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Talk to me in English..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Yêu cầu AI đóng vai giáo viên tiếng Anh
        full_prompt = f"You are a friendly English teacher. Correct the user's grammar if it's wrong, then reply to their message in English: {prompt}"
        
        response = model.generate_content(full_prompt)
        ai_reply = response.text
        
        st.markdown(ai_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})


# Cấu hình giao diện
st.set_page_config(page_title="English Chat AI", page_icon="🗣️")

st.title("🗣️ English Practice Partner")
st.markdown("Talk to me all day to improve your English!")

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your English teacher. How can I help you today?"}
    ]

# Hiển thị các tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ô nhập liệu cho người dùng
if prompt := st.chat_input("Type your English sentence here..."):
    # Thêm tin nhắn của bạn vào lịch sử
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI phản hồi (Tạm thời là phản hồi tự động, rất nhẹ)
    with st.chat_message("assistant"):
        full_response = f"That's great! You said: '{prompt}'. Keep going, you're doing well!"
        st.markdown(full_response)
    
    # Lưu phản hồi của AI
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    # Đoạn code giúp trình duyệt tự động đọc câu trả lời của AI
if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
    last_reply = st.session_state.messages[-1]["content"].replace("'", "\\'")
    st.components.v1.html(
        f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{last_reply}');
        msg.lang = 'en-US';
        window.speechSynthesis.speak(msg);
        </script>
        """,
        height=0,
    )

