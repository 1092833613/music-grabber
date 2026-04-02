"""
音乐抓取 App - 主入口
基于 Kivy 的跨平台移动应用

功能：
- 🌐 通用音频抓取
- 🎵 格式转换
- 📁 批量下载
- 🔍 音乐搜索
- 📝 歌词下载
- 🖼️ 封面下载
- 📋 历史记录
- 🎵 播放列表
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder

# 移动端配置
Config.set("graphics", "width", "360")
Config.set("graphics", "height", "640")
Config.set("input", "mouse", "mouse,multitouch_on_demand")

# 导入界面
from ui.main_screen import MainScreen, KV as MAIN_KV
from ui.search_screen import SearchScreen, KV as SEARCH_KV
from ui.history_screen import HistoryScreen, KV as HISTORY_KV
from ui.playlist_screen import PlaylistScreen, KV as PLAYLIST_KV


class MusicGrabberApp(App):
    """音乐抓取 App"""
    
    def build(self):
        self.title = "🎵 音乐抓取"
        
        # 加载所有 KV 界面
        Builder.load_string(MAIN_KV)
        Builder.load_string(SEARCH_KV)
        Builder.load_string(HISTORY_KV)
        Builder.load_string(PLAYLIST_KV)
        
        # 创建屏幕管理器
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SearchScreen(name="search"))
        sm.add_widget(HistoryScreen(name="history"))
        sm.add_widget(PlaylistScreen(name="playlist"))
        
        return sm
    
    def on_pause(self):
        """Android 后台运行"""
        return True
    
    def on_resume(self):
        """Android 恢复运行"""
        pass
    
    def show_create_playlist_dialog(self):
        """显示创建播放列表对话框"""
        # TODO: 实现对话框
        print("创建播放列表功能开发中...")


if __name__ == "__main__":
    MusicGrabberApp().run()
