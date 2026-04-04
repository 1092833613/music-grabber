"""
音乐抓取 App - 修复黑屏问题 v2.0.8
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle


class MainLayout(BoxLayout):
    """主布局"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        # 设置白色背景
        with self.canvas.before:
            Color(1, 1, 1, 1)  # 白色
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MusicGrabberApp(App):
    """音乐抓取 App"""
    
    def build(self):
        self.title = "🎵 音乐抓取"
        
        # 创建主布局
        layout = MainLayout()
        
        # 标题
        title = Label(
            text='🎵 音乐抓取',
            font_size='24sp',
            size_hint_y=None,
            height=50,
            bold=True
        )
        layout.add_widget(title)
        
        # URL 输入
        self.url_input = TextInput(
            hint_text='粘贴视频链接...',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.url_input)
        
        # 按钮
        btn_layout = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=10
        )
        
        info_btn = Button(text='获取信息')
        info_btn.bind(on_press=self.get_info)
        btn_layout.add_widget(info_btn)
        
        download_btn = Button(text='下载')
        download_btn.bind(on_press=self.download)
        btn_layout.add_widget(download_btn)
        
        layout.add_widget(btn_layout)
        
        # 状态
        self.status_label = Label(
            text='状态：就绪',
            size_hint_y=None,
            height=30
        )
        layout.add_widget(self.status_label)
        
        return layout
    
    def get_info(self, instance):
        """获取信息"""
        self.status_label.text = '状态：获取中...'
        print("获取信息...")
    
    def download(self, instance):
        """下载"""
        self.status_label.text = '状态：下载中...'
        print("下载...")


if __name__ == "__main__":
    MusicGrabberApp().run()
