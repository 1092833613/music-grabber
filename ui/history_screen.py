"""
下载历史界面
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.clock import Clock
from core.history import DownloadHistory


class HistoryScreen(Screen):
    """历史界面"""
    
    history_items = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history_manager = DownloadHistory()
    
    def on_enter(self):
        """进入界面时刷新列表"""
        self.refresh()
    
    def refresh(self):
        """刷新历史列表"""
        def callback(dt):
            items = self.history_manager.get_all(limit=50)
            self.history_items = [
                {
                    "text": f"{item['title']} - {item.get('artist', 'Unknown')}",
                    "secondary_text": f"{item['downloaded_at'][:10]} | {item['format']}",
                    "id": item["id"],
                }
                for item in items
            ]
        
        Clock.schedule_once(callback, 0.1)
    
    def clear_history(self):
        """清空历史"""
        self.history_manager.clear()
        self.refresh()


# KV 定义
KV = """
<HistoryScreen>:
    name: "history"
    
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 15
        
        BoxLayout:
            size_hint_y: None
            height: "50dp"
            
            Label:
                text: "📋 下载历史"
                font_size: "28sp"
                bold: True
            
            Button:
                text: "🗑️ 清空"
                size_hint_x: None
                width: "100dp"
                on_release: root.clear_history()
        
        Label:
            text: f"共 {len(root.history_items)} 条记录"
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
                
                data: root.history_items
        
        Label:
            text: "⚠️ 历史记录仅保存在本地"
            color: 0.7, 0.7, 0.7, 1
            font_size: "12sp"
            size_hint_y: None
            height: "30dp"
"""
