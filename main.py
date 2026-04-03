"""
音乐抓取 App - 测试 KV 文件加载
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label

# 加载 KV 字符串
KV = """
BoxLayout:
    orientation: 'vertical'
    Label:
        text: 'KV Works!'
        font_size: 24
"""


class MusicGrabberApp(App):
    def build(self):
        self.title = "KV Test"
        Builder.load_string(KV)
        return Label(text='Test')


if __name__ == "__main__":
    MusicGrabberApp().run()
