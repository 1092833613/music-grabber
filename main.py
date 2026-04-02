"""
音乐抓取 App - 主入口
基于 Kivy 的跨平台移动应用

Android 13 兼容版本:
- 移除 Android 14 特定代码
- 使用标准 Kivy 启动流程
- 简化权限处理
"""

import sys
import traceback
import os

# ========== 全局异常捕获 ==========
def handle_exception(exc_type, exc_value, exc_traceback):
    """全局异常处理器 - 记录闪退日志"""
    if issubclass(exc_type, KeyboardInterrupt):
        return
    
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    try:
        log_dir = '/sdcard/music_grabber_logs/'
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'crash.log')
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("Music Grabber App - Crash Log\n")
            f.write("=" * 60 + "\n\n")
            f.write(error_msg)
        
        print(f"Crash log saved to: {log_file}")
    except Exception as e:
        print(f"Failed to save crash log: {e}")

sys.excepthook = handle_exception
# ===========================================

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
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
        
        # 加载 KV 界面
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
        print("创建播放列表功能开发中...")


if __name__ == "__main__":
    MusicGrabberApp().run()
