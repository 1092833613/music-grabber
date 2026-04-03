"""
音乐抓取 App - 不使用 ScreenManager 的版本
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.lang import Builder


# 主界面 KV
MAIN_KV = """
BoxLayout:
    orientation: 'vertical'
    padding: 20
    spacing: 10
    
    Label:
        text: '🎵 音乐抓取'
        font_size: 24
        size_hint_y: None
        height: 50
    
    TextInput:
        id: url_input
        hint_text: '粘贴视频链接...'
        multiline: False
        size_hint_y: None
        height: 50
    
    BoxLayout:
        size_hint_y: None
        height: 50
        spacing: 10
        
        Button:
            text: '搜索'
            on_release: app.on_search()
        
        Button:
            text: '下载'
            on_release: app.on_download()
    
    Label:
        id: status
        text: '状态：就绪'
        size_hint_y: None
        height: 30
"""


class MainLayout(BoxLayout):
    """主界面"""
    pass


class MusicGrabberApp(App):
    """音乐抓取 App"""
    
    def build(self):
        self.title = "🎵 音乐抓取"
        Builder.load_string(MAIN_KV)
        return MainLayout()
    
    def on_search(self):
        print("搜索功能开发中...")
    
    def on_download(self):
        print("下载功能开发中...")


if __name__ == "__main__":
    MusicGrabberApp().run()
