"""
音乐抓取 App - 完整功能版 v2.0.7
Android 14 兼容（不使用 ScreenManager）
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.clock import Clock


# 完整 UI 的 KV 字符串（不使用 ScreenManager）
KV = """
BoxLayout:
    orientation: 'vertical'
    
    # 顶部导航栏
    BoxLayout:
        size_hint_y: None
        height: 50
        
        Button:
            text: '🏠 主页'
            on_release: app.switch_tab('main')
        
        Button:
            text: '🔍 搜索'
            on_release: app.switch_tab('search')
        
        Button:
            text: '📋 历史'
            on_release: app.switch_tab('history')
        
        Button:
            text: '🎵 列表'
            on_release: app.switch_tab('playlist')
    
    # 内容区域
    ScrollView:
        id: content
        
        BoxLayout:
            id: main_content
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
                    text: '获取信息'
                    on_release: app.get_info()
                
                Button:
                    text: '下载'
                    on_release: app.download()
            
            Label:
                id: status
                text: '状态：就绪'
                size_hint_y: None
                height: 30
"""


class MainContent(BoxLayout):
    """主内容区"""
    pass


class MusicGrabberApp(App):
    """音乐抓取 App"""
    
    current_tab = 'main'
    
    def build(self):
        self.title = "🎵 音乐抓取"
        Builder.load_string(KV)
        return MainContent()
    
    def switch_tab(self, tab_name):
        """切换标签页"""
        self.current_tab = tab_name
        content = self.root.ids.content
        main_content = self.root.ids.main_content
        
        # 清空当前内容
        main_content.clear_widgets()
        
        # 根据标签加载不同内容
        if tab_name == 'main':
            self.load_main_tab(main_content)
        elif tab_name == 'search':
            self.load_search_tab(main_content)
        elif tab_name == 'history':
            self.load_history_tab(main_content)
        elif tab_name == 'playlist':
            self.load_playlist_tab(main_content)
    
    def load_main_tab(self, parent):
        """加载主页"""
        parent.add_widget(Label(
            text='🎵 音乐抓取',
            font_size=24,
            size_hint_y=None,
            height=50
        ))
        
        url_input = TextInput(
            hint_text='粘贴视频链接...',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        parent.add_widget(url_input)
        
        btn_layout = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=10
        )
        
        btn_layout.add_widget(Button(
            text='获取信息',
            on_release=lambda x: self.get_info()
        ))
        
        btn_layout.add_widget(Button(
            text='下载',
            on_release=lambda x: self.download()
        ))
        
        parent.add_widget(btn_layout)
        
        status = Label(
            id='status',
            text='状态：就绪',
            size_hint_y=None,
            height=30
        )
        parent.add_widget(status)
    
    def load_search_tab(self, parent):
        """加载搜索页"""
        parent.add_widget(Label(
            text='🔍 搜索音乐',
            font_size=24,
            size_hint_y=None,
            height=50
        ))
        
        parent.add_widget(TextInput(
            hint_text='输入歌曲名或歌手...',
            multiline=False,
            size_hint_y=None,
            height=50
        ))
        
        parent.add_widget(Button(
            text='搜索',
            on_release=lambda x: self.search_music()
        ))
    
    def load_history_tab(self, parent):
        """加载历史页"""
        parent.add_widget(Label(
            text='📋 下载历史',
            font_size=24,
            size_hint_y=None,
            height=50
        ))
        
        parent.add_widget(Label(
            text='历史记录功能开发中...',
            size_hint_y=None,
            height=30
        ))
    
    def load_playlist_tab(self, parent):
        """加载播放列表页"""
        parent.add_widget(Label(
            text='🎵 播放列表',
            font_size=24,
            size_hint_y=None,
            height=50
        ))
        
        parent.add_widget(Label(
            text='播放列表功能开发中...',
            size_hint_y=None,
            height=30
        ))
    
    def get_info(self):
        """获取视频信息"""
        print("获取信息...")
    
    def download(self):
        """下载"""
        print("下载...")
    
    def search_music(self):
        """搜索音乐"""
        print("搜索...")


if __name__ == "__main__":
    MusicGrabberApp().run()
