import streamlit as st

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
