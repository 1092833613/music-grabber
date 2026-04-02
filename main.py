"""
音乐抓取 App - 主入口
基于 Kivy 的跨平台移动应用

Android 14 紧急修复:
- 移除权限请求（Android 14 太严格）
- 简化启动流程
- 添加更多日志点
"""

import sys
import traceback
import os
import logging

# ========== 改进 1: 启动错误捕获 ==========
def handle_exception(exc_type, exc_value, exc_traceback):
    """全局异常处理器 - 记录闪退日志"""
    if issubclass(exc_type, KeyboardInterrupt):
        return
    
    # 格式化错误信息
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    # 保存到文件（尝试多个位置）
    try:
        # Android 外部存储
        log_dir = '/sdcard/music_grabber_logs/'
        if not os.path.exists(log_dir):
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

# 设置全局异常处理器
sys.excepthook = handle_exception
# ===========================================

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
from kivy.clock import Clock

# 移动端配置
Config.set("graphics", "width", "360")
Config.set("graphics", "height", "640")
Config.set("input", "mouse", "mouse,multitouch_on_demand")

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 导入界面
from ui.main_screen import MainScreen, KV as MAIN_KV
from ui.search_screen import SearchScreen, KV as SEARCH_KV
from ui.history_screen import HistoryScreen, KV as HISTORY_KV
from ui.playlist_screen import PlaylistScreen, KV as PLAYLIST_KV


class MusicGrabberApp(App):
    """音乐抓取 App"""
    
    def build(self):
        logger.info("App starting...")
        
        try:
            self.title = "🎵 音乐抓取"
            
            # 加载所有 KV 界面
            logger.info("Loading KV files...")
            Builder.load_string(MAIN_KV)
            Builder.load_string(SEARCH_KV)
            Builder.load_string(HISTORY_KV)
            Builder.load_string(PLAYLIST_KV)
            
            # 创建屏幕管理器
            logger.info("Creating screen manager...")
            sm = ScreenManager(transition=SlideTransition())
            sm.add_widget(MainScreen(name="main"))
            sm.add_widget(SearchScreen(name="search"))
            sm.add_widget(HistoryScreen(name="history"))
            sm.add_widget(PlaylistScreen(name="playlist"))
            
            logger.info("App build completed!")
            return sm
            
        except Exception as e:
            logger.error(f"Build failed: {e}")
            logger.exception(e)
            raise
    
    def on_start(self):
        """App 启动时执行"""
        logger.info("App on_start called")
        
        # ⚠️ Android 14 修复：移除权限请求
        # Android 14 对权限请求非常严格，可能导致闪退
        # 改为在使用时动态请求
        logger.info("Skipping permission request for Android 14 compatibility")
        
        # 延迟初始化（避免启动时崩溃）
        Clock.schedule_once(self._init_downloader, 0.5)
    
    def _init_downloader(self, dt):
        """延迟初始化下载器"""
        try:
            logger.info("Initializing downloader...")
            # 延迟初始化核心模块
            from core.downloader import MusicDownloader
            self.downloader = MusicDownloader()
            logger.info("Downloader initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize downloader: {e}")
            logger.exception(e)
    
    def on_pause(self):
        """Android 后台运行"""
        logger.info("App paused")
        return True
    
    def on_resume(self):
        """Android 恢复运行"""
        logger.info("App resumed")
        pass
    
    def on_stop(self):
        """App 停止"""
        logger.info("App stopped")
    
    def show_create_playlist_dialog(self):
        """显示创建播放列表对话框"""
        logger.info("Create playlist dialog requested")
        # TODO: 实现对话框
        print("创建播放列表功能开发中...")


if __name__ == "__main__":
    logger.info("Launching Music Grabber App...")
    try:
        MusicGrabberApp().run()
    except Exception as e:
        logger.error(f"App launch failed: {e}")
        logger.exception(e)
        raise
