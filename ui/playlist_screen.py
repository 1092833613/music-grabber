"""
播放列表界面
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty
from kivy.clock import Clock
from core.playlist import PlaylistManager


class PlaylistScreen(Screen):
    """播放列表界面"""
    
    playlists = ListProperty([])
    selected_playlist_id = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager = PlaylistManager()
    
    def on_enter(self):
        """进入界面时刷新"""
        self.refresh()
    
    def refresh(self):
        """刷新播放列表"""
        def callback(dt):
            items = self.manager.get_all()
            self.playlists = [
                {
                    "text": item["name"],
                    "secondary_text": f"{len(item['tracks'])} 首歌曲",
                    "id": item["id"],
                }
                for item in items
            ]
        
        Clock.schedule_once(callback, 0.1)
    
    def create_playlist(self, name):
        """创建播放列表"""
        self.manager.create(name)
        self.refresh()


# KV 定义
KV = """
<PlaylistScreen>:
    name: "playlist"
    
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 15
        
        Label:
            text: "🎵 播放列表"
            font_size: "28sp"
            bold: True
            size_hint_y: None
            height: "50dp"
        
        Button:
            text: "➕ 新建播放列表"
            size_hint_y: None
            height: "45dp"
            on_release: app.show_create_playlist_dialog()
        
        Label:
            text: f"共 {len(root.playlists)} 个播放列表"
            size_hint_y: None
            height: "30dp"
        
        RecycleView:
            viewclass: "TwoLineListItem"
            
            RecycleBoxLayout:
                default_size: None, "60dp"
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: "vertical"
                spacing: "5dp"
                
                data: root.playlists
"""
