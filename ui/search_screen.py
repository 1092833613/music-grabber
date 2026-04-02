"""
音乐搜索界面
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from core.searcher import MusicSearcher


class SearchScreen(Screen):
    """搜索界面"""
    
    search_query = StringProperty("")
    search_results = ListProperty([])
    is_searching = BooleanProperty(False)
    selected_site = StringProperty("youtube")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.searcher = MusicSearcher()
    
    def start_search(self):
        """开始搜索"""
        if not self.search_query:
            return
        
        if self.is_searching:
            return
        
        self.is_searching = True
        self.search_results = []
        
        Clock.schedule_once(lambda dt: self._search_task(), 0.1)
    
    def _search_task(self):
        """搜索任务"""
        result = self.searcher.search(
            query=self.search_query,
            site=self.selected_site,
            max_results=20,
        )
        
        if result["success"]:
            Clock.schedule_once(
                lambda dt: self._search_complete(result["results"]),
                0
            )
        else:
            Clock.schedule_once(
                lambda dt: self._search_error(result.get("error", "搜索失败")),
                0
            )
    
    def _search_complete(self, results):
        """搜索完成"""
        self.search_results = results
        self.is_searching = False
    
    def _search_error(self, error):
        """搜索错误"""
        self.search_results = [{"title": f"错误：{error}"}]
        self.is_searching = False
    
    def on_result_select(self, result):
        """选择搜索结果"""
        # 通知主界面下载
        if self.parent and hasattr(self.parent, 'on_search_result'):
            self.parent.on_search_result(result)


# KV 定义
KV = """
<SearchScreen>:
    name: "search"
    
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 15
        
        Label:
            text: "🔍 搜索音乐"
            font_size: "28sp"
            bold: True
            size_hint_y: None
            height: "50dp"
        
        # 搜索框
        TextInput:
            id: search_input
            hint_text: "输入歌曲名或歌手..."
            multiline: False
            text: root.search_query
            on_text: root.search_query = self.text
            on_text_validate: root.start_search()
            size_hint_y: None
            height: "50dp"
            font_size: "16sp"
        
        # 音源选择
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            spacing: 10
            
            Label:
                text: "音源:"
                size_hint_x: None
                width: "60dp"
            
            Spinner:
                text: root.selected_site
                values: ["youtube", "soundcloud", "bandcamp"]
                on_text: root.selected_site = self.text
                size_hint_x: None
                width: "120dp"
        
        # 搜索按钮
        Button:
            text: "🔍 搜索" if not root.is_searching else "搜索中..."
            disabled: root.is_searching
            size_hint_y: None
            height: "50dp"
            bold: True
            on_release: root.start_search()
        
        # 搜索结果列表
        Label:
            text: f"找到 {len(root.search_results)} 条结果"
            size_hint_y: None
            height: "30dp"
        
        RecycleView:
            viewclass: "OneLineListItem"
            
            RecycleBoxLayout:
                default_size: None, "48dp"
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: "vertical"
                spacing: "2dp"
                
                data: root.search_results
"""
