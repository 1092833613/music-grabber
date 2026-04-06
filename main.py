"""
音乐抓取 App - 修复中文乱码 v2.1.1
注册 Android 系统中文字体
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.text import LabelBase
import os
import json
from datetime import datetime

# ========== 注册中文字体 ==========
try:
    # Android 系统中文字体
    LabelBase.register(
        name='DroidSansFallback',
        fn_regular='/system/fonts/DroidSansFallback.ttf'
    )
    # 备用字体
    LabelBase.register(
        name='NotoSansSC',
        fn_regular='/system/fonts/NotoSansSC-Regular.ttf'
    )
except Exception as e:
    print(f"字体注册失败：{e}")
# ==================================

# 设置窗口背景色为白色
Window.clearcolor = (0.95, 0.95, 0.95, 1)

# 数据文件路径
DATA_FILE = '/sdcard/music_grabber_data.json'


class MusicGrabberApp(App):
    """音乐抓取 App"""
    
    download_history = []
    
    def build(self):
        self.title = "音乐抓取"
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical')
        
        # 滚动区域
        scroll = ScrollView()
        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15,
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))
        scroll.add_widget(layout)
        main_layout.add_widget(scroll)
        
        # 1. 标题 - 使用中文字体
        title = Label(
            text='🎵 音乐抓取',
            font_name='DroidSansFallback',
            font_size='28sp',
            size_hint_y=None,
            height=70,
            bold=True,
            color=(0.2, 0.2, 0.8, 1)
        )
        layout.add_widget(title)
        
        # 2. 说明
        desc = Label(
            text='支持 YouTube、B 站、抖音等平台',
            font_name='DroidSansFallback',
            font_size='16sp',
            size_hint_y=None,
            height=35,
            color=(0.4, 0.4, 0.4, 1)
        )
        layout.add_widget(desc)
        
        # 3. URL 输入框
        input_label = Label(
            text='视频链接:',
            font_name='DroidSansFallback',
            font_size='18sp',
            size_hint_y=None,
            height=35,
            halign='left',
            color=(0.2, 0.2, 0.2, 1)
        )
        layout.add_widget(input_label)
        
        self.url_input = TextInput(
            hint_text='粘贴视频链接到这里...',
            multiline=False,
            size_hint_y=None,
            height=55,
            font_size='16sp',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        layout.add_widget(self.url_input)
        
        # 4. 格式选择
        format_label = Label(
            text='输出格式:',
            font_name='DroidSansFallback',
            font_size='18sp',
            size_hint_y=None,
            height=35,
            halign='left',
            color=(0.2, 0.2, 0.2, 1)
        )
        layout.add_widget(format_label)
        
        self.format_btn = Button(
            text='MP3 (音频)',
            size_hint_y=None,
            height=50,
            font_size='18sp'
        )
        self.format_btn.bind(on_press=self.toggle_format)
        layout.add_widget(self.format_btn)
        self.current_format = 'mp3'
        
        # 5. 按钮区域
        btn_layout = BoxLayout(
            size_hint_y=None,
            height=55,
            spacing=15
        )
        
        info_btn = Button(
            text='📊 获取信息',
            font_size='18sp',
            background_color=(0.3, 0.6, 0.9, 1)
        )
        info_btn.bind(on_press=self.get_info)
        btn_layout.add_widget(info_btn)
        
        download_btn = Button(
            text='⬇️ 下载',
            font_size='18sp',
            background_color=(0.3, 0.9, 0.6, 1)
        )
        download_btn.bind(on_press=self.download)
        btn_layout.add_widget(download_btn)
        
        layout.add_widget(btn_layout)
        
        # 6. 状态显示
        self.status = Label(
            text='状态：就绪',
            font_name='DroidSansFallback',
            size_hint_y=None,
            height=45,
            color=(0, 0.6, 0, 1),
            font_size='16sp',
            bold=True
        )
        layout.add_widget(self.status)
        
        # 7. 分隔线
        separator = Label(
            text='━━━━━━━━━━━━━━━━━━━━',
            size_hint_y=None,
            height=30,
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(separator)
        
        # 8. 历史记录标题
        history_title = Label(
            text='📋 下载历史',
            font_name='DroidSansFallback',
            font_size='22sp',
            size_hint_y=None,
            height=50,
            bold=True,
            color=(0.2, 0.2, 0.8, 1)
        )
        layout.add_widget(history_title)
        
        # 9. 历史记录列表
        self.history_layout = BoxLayout(
            orientation='vertical',
            spacing=10
        )
        layout.add_widget(self.history_layout)
        
        # 10. 清空历史按钮
        clear_btn = Button(
            text='🗑️ 清空历史',
            size_hint_y=None,
            height=50,
            font_size='18sp',
            background_color=(0.9, 0.3, 0.3, 1)
        )
        clear_btn.bind(on_press=self.clear_history)
        layout.add_widget(clear_btn)
        
        # 加载历史数据
        Clock.schedule_once(lambda dt: self.load_history(), 0.5)
        
        return main_layout
    
    def toggle_format(self, instance):
        """切换格式"""
        if self.current_format == 'mp3':
            self.current_format = 'mp4'
            self.format_btn.text = 'MP4 (视频)'
            self.format_btn.background_color = (0.9, 0.6, 0.3, 1)
        else:
            self.current_format = 'mp3'
            self.format_btn.text = 'MP3 (音频)'
            self.format_btn.background_color = (0.3, 0.6, 0.9, 1)
    
    def get_info(self, instance):
        """获取信息"""
        url = self.url_input.text.strip()
        if not url:
            self.status.text = '状态：请输入链接'
            self.status.color = (1, 0, 0, 1)
            return
        
        self.status.text = '状态：获取信息中...'
        self.status.color = (0, 0, 1, 1)
        
        Clock.schedule_once(lambda dt: self._show_info(url), 1)
    
    def _show_info(self, url):
        """显示信息"""
        self.status.text = f'状态：准备下载 ({self.current_format.upper()})'
        self.status.color = (0, 0.6, 0, 1)
    
    def download(self, instance):
        """下载"""
        url = self.url_input.text.strip()
        if not url:
            self.status.text = '状态：请输入链接'
            self.status.color = (1, 0, 0, 1)
            return
        
        self.status.text = '状态：下载中...'
        self.status.color = (0, 0, 1, 1)
        
        Clock.schedule_once(lambda dt: self._download_complete(url), 2)
    
    def _download_complete(self, url):
        """下载完成"""
        self.save_to_history(url)
        
        self.status.text = '状态：下载完成！'
        self.status.color = (0, 0.8, 0, 1)
        self.url_input.text = ''
    
    def save_to_history(self, url):
        """保存到历史"""
        record = {
            'url': url,
            'format': self.current_format,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        self.download_history.insert(0, record)
        
        if len(self.download_history) > 20:
            self.download_history = self.download_history[:20]
        
        try:
            os.makedirs('/sdcard/', exist_ok=True)
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.download_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存失败：{e}")
        
        self.refresh_history()
    
    def load_history(self):
        """加载历史"""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.download_history = json.load(f)
                self.refresh_history()
        except Exception as e:
            print(f"加载失败：{e}")
    
    def refresh_history(self):
        """刷新历史显示"""
        self.history_layout.clear_widgets()
        
        if not self.download_history:
            label = Label(
                text='暂无历史记录',
                font_name='DroidSansFallback',
                size_hint_y=None,
                height=40,
                color=(0.6, 0.6, 0.6, 1)
            )
            self.history_layout.add_widget(label)
            return
        
        for record in self.download_history:
            item_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=70,
                padding=10
            )
            
            url_label = Label(
                text=f"🔗 {record['url'][:50]}...",
                font_name='DroidSansFallback',
                font_size='14sp',
                size_hint_y=None,
                height=35,
                halign='left',
                color=(0.2, 0.2, 0.2, 1)
            )
            item_layout.add_widget(url_label)
            
            info_label = Label(
                text=f"{record['format'].upper()} · {record['time']}",
                font_name='DroidSansFallback',
                font_size='12sp',
                size_hint_y=None,
                height=25,
                halign='left',
                color=(0.5, 0.5, 0.5, 1)
            )
            item_layout.add_widget(info_label)
            
            self.history_layout.add_widget(item_layout)
    
    def clear_history(self, instance):
        """清空历史"""
        self.download_history = []
        try:
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
        except Exception as e:
            print(f"删除失败：{e}")
        self.refresh_history()
        self.status.text = '状态：历史已清空'
        self.status.color = (0.6, 0.6, 0.6, 1)


if __name__ == "__main__":
    MusicGrabberApp().run()
