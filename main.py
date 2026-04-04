"""
音乐抓取 App - 最简化可用版本 v2.0.9
修复白屏和乱码问题
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

# 设置窗口背景色为白色
Window.clearcolor = (1, 1, 1, 1)


class MusicGrabberApp(App):
    """音乐抓取 App"""
    
    def build(self):
        self.title = "Music Grabber"
        
        # 主布局
        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )
        
        # 1. 标题 - 使用英文避免乱码
        title = Label(
            text='Music Grabber',
            font_size='24sp',
            size_hint_y=None,
            height=60,
            bold=True,
            color=(0, 0, 0, 1)  # 黑色文字
        )
        layout.add_widget(title)
        
        # 2. 说明文字
        desc = Label(
            text='Paste video URL to download',
            font_size='16sp',
            size_hint_y=None,
            height=40,
            color=(0.3, 0.3, 0.3, 1)
        )
        layout.add_widget(desc)
        
        # 3. URL 输入框
        self.url_input = TextInput(
            hint_text='https://...',
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        layout.add_widget(self.url_input)
        
        # 4. 按钮区域
        btn_layout = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=15
        )
        
        # 获取信息按钮
        info_btn = Button(
            text='Get Info',
            font_size='18sp'
        )
        info_btn.bind(on_press=self.get_info)
        btn_layout.add_widget(info_btn)
        
        # 下载按钮
        download_btn = Button(
            text='Download',
            font_size='18sp'
        )
        download_btn.bind(on_press=self.download)
        btn_layout.add_widget(download_btn)
        
        layout.add_widget(btn_layout)
        
        # 5. 状态显示
        self.status = Label(
            text='Status: Ready',
            size_hint_y=None,
            height=40,
            color=(0, 0.5, 0, 1),  # 绿色
            font_size='16sp'
        )
        layout.add_widget(self.status)
        
        return layout
    
    def get_info(self, instance):
        """获取信息"""
        url = self.url_input.text
        if url:
            self.status.text = f'Status: Getting info...'
            self.status.color = (0, 0, 1, 1)  # 蓝色
        else:
            self.status.text = 'Status: Please enter URL'
            self.status.color = (1, 0, 0, 1)  # 红色
    
    def download(self, instance):
        """下载"""
        url = self.url_input.text
        if url:
            self.status.text = f'Status: Downloading...'
            self.status.color = (0, 0, 1, 1)  # 蓝色
        else:
            self.status.text = 'Status: Please enter URL'
            self.status.color = (1, 0, 0, 1)  # 红色


if __name__ == "__main__":
    MusicGrabberApp().run()
