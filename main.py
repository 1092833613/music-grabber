"""
音乐抓取 App - 最基础测试
测试 Kivy 能否正常加载 UI
"""

from kivy.app import App
from kivy.uix.label import Label


class MusicGrabberApp(App):
    def build(self):
        self.title = "Music"
        return Label(text='Test')


if __name__ == "__main__":
    MusicGrabberApp().run()
