"""
音乐抓取 App - 修复字体问题
"""

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
import os

# ========== 添加中文字体支持 ==========
# 注册 DroidSansFallback（Android 系统中文字体）
LabelBase.register(
    name='DroidSansFallback',
    fn_regular='/system/fonts/DroidSansFallback.ttf',
    fn_bold='/system/fonts/DroidSansFallback.ttf'
)
# ======================================


class TestApp(App):
    """测试 App"""
    
    def build(self):
        self.title = "Test"
        
        # 最简单的 UI
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 使用系统字体
        label1 = Label(
            text='If you can see this, it works!',
            font_size='20sp',
            font_name='DroidSansFallback'
        )
        
        label2 = Label(
            text=f'Android Version: {os.popen("getprop ro.build.version.release").read().strip()}',
            font_size='16sp',
            font_name='DroidSansFallback'
        )
        
        label3 = Label(
            text='Kivy is working!',
            font_size='18sp',
            font_name='DroidSansFallback'
        )
        
        layout.add_widget(label1)
        layout.add_widget(label2)
        layout.add_widget(label3)
        
        return layout


if __name__ == "__main__":
    TestApp().run()
