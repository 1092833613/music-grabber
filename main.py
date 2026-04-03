"""
音乐抓取 App - 测试完整 UI 组件
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

# 完整 UI 的 KV 字符串
KV = """
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 10
    
    Label:
        text: 'Music Grabber Test'
        font_size: 24
        size_hint_y: None
        height: 50
    
    TextInput:
        id: url_input
        hint_text: 'Paste URL here...'
        multiline: False
        size_hint_y: None
        height: 50
    
    Button:
        text: 'Download'
        size_hint_y: None
        height: 50
    
    Label:
        text: 'Status: Ready'
        size_hint_y: None
        height: 30
"""


class MusicGrabberApp(App):
    def build(self):
        self.title = "Music Test"
        Builder.load_string(KV)
        return BoxLayout(orientation='vertical')


if __name__ == "__main__":
    MusicGrabberApp().run()
