import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

# Cấu hình màu sắc giao diện
Window.clearcolor = (0.95, 0.95, 0.95, 1)

class ChatApp(App):
    def build(self):
        self.title = "English Daily Chat"
        
        # Layout chính
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Vùng hiển thị nội dung chat
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.chat_history = Label(
            text="[color=008080][b]AI:[/b] Hello! Let's practice English together![/color]\n",
            markup=True,
            size_hint_y=None,
            halign='left',
            valign='top',
            color=(0, 0, 0, 1)
        )
        self.chat_history.bind(texture_size=self.chat_history.setter('size'))
        self.scroll_view.add_widget(self.chat_history)
        self.main_layout.add_widget(self.scroll_view)

        # Vùng nhập liệu
        input_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        self.user_input = TextInput(
            hint_text="Type your English here...",
            multiline=False,
            padding_y=(10, 10)
        )
        
        send_button = Button(
            text="Send",
            size_hint=(0.3, 1),
            background_color=(0, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        send_button.bind(on_press=self.send_message)

        input_layout.add_widget(self.user_input)
        input_layout.add_widget(send_button)
        self.main_layout.add_widget(input_layout)

        return self.main_layout

    def send_message(self, instance):
        message = self.user_input.text.strip()
        if message:
            # Hiển thị tin nhắn người dùng
            self.chat_history.text += f"\n[b]You:[/b] {message}\n"
            self.user_input.text = ""
            
            # Giả lập phản hồi từ AI (Bạn có thể thay thế bằng API thực tế)
            self.get_ai_response(message)

    def get_ai_response(self, user_text):
        # Đây là nơi tích hợp OpenAI/Gemini API trong tương lai
        # Hiện tại app sẽ phản hồi tự động để bạn kiểm tra giao diện
        ai_reply = f"AI: I understand you said '{user_text}'. Your English is improving!"
        self.chat_history.text += f"[color=008080]{ai_reply}[/color]\n"
        
        # Tự động cuộn xuống dưới cùng
        self.scroll_view.scroll_y = 0

if __name__ == '__main__':
    ChatApp().run()
