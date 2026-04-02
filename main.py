"""
音乐抓取 App - SDL2 配置测试
"""

# 在导入 Kivy 之前配置 SDL2
import os
os.environ['KIVY_VIDEO'] = 'ffpyplayer'
os.environ['KIVY_AUDIO'] = 'ffpyplayer'

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class TestApp(App):
    def build(self):
        self.title = "Test"
        
        layout = BoxLayout(orientation='vertical', padding=20)
        
        label = Label(
            text='Kivy Test - Android 14',
            font_size='24sp'
        )
        
        layout.add_widget(label)
        
        return layout


if __name__ == "__main__":
    TestApp().run()
