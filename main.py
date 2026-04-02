"""
音乐抓取 App - 仅主界面版本
用于定位闪退问题
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config
from kivy.lang import Builder

# 移动端配置
Config.set("graphics", "width", "360")
Config.set("graphics", "height", "640")

# 仅导入主界面
from ui.main_screen import MainScreen, KV as MAIN_KV


class MusicGrabberApp(App):
    def build(self):
        self.title = "🎵 音乐抓取"
        
        # 仅加载主界面
        Builder.load_string(MAIN_KV)
        
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        
        return sm
    
    def on_pause(self):
        return True


if __name__ == "__main__":
    MusicGrabberApp().run()
