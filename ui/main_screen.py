"""
音乐抓取 App - 主界面
基于 Kivy 的移动端 UI
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
import os

from core.downloader import MusicDownloader
from core.converter import AudioConverter
from core.batch import BatchDownloader


class MainScreen(Screen):
    """主界面"""
    
    # 状态属性
    url_input = StringProperty("")
    status_text = StringProperty("就绪")
    progress_value = NumericProperty(0)
    progress_max = NumericProperty(100)
    is_downloading = BooleanProperty(False)
    
    # 格式选项
    selected_format = StringProperty("mp3")
    output_dir = StringProperty("./downloads")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.downloader = MusicDownloader(self.output_dir)
        self.converter = AudioConverter()
        self.batch_downloader = BatchDownloader(self.output_dir)
        
    def start_download(self):
        """开始下载"""
        if not self.url_input:
            self.status_text = "请输入 URL"
            return
        
        if self.is_downloading:
            self.status_text = "正在下载中..."
            return
        
        self.is_downloading = True
        self.progress_value = 0
        self.status_text = "正在获取信息..."
        
        # 异步下载（避免阻塞 UI）
        Clock.schedule_once(lambda dt: self._download_task(), 0.1)
    
    def _download_task(self):
        """下载任务（后台执行）"""
        def progress_callback(data):
            """进度回调"""
            if data["status"] == "downloading":
                total = data.get("total_bytes", 0)
                downloaded = data.get("downloaded_bytes", 0)
                if total > 0:
                    progress = (downloaded / total) * 100
                    Clock.schedule_once(
                        lambda dt: self._update_progress(progress, data),
                        0
                    )
            elif data["status"] == "finished":
                Clock.schedule_once(
                    lambda dt: self._download_complete(True, "下载完成"),
                    0
                )
            elif data["status"] == "error":
                Clock.schedule_once(
                    lambda dt: self._download_complete(False, data.get("error", "未知错误")),
                    0
                )
        
        # 执行下载
        result = self.downloader.download(
            url=self.url_input,
            format=self.selected_format,
            progress_callback=progress_callback,
        )
        
        if result["success"]:
            self._download_complete(True, f"下载完成：{result['info'].get('title', '未知')}")
        else:
            self._download_complete(False, result.get("error", "下载失败"))
    
    def _update_progress(self, progress, data):
        """更新进度"""
        self.progress_value = progress
        speed = data.get("speed", 0)
        eta = data.get("eta", 0)
        
        speed_mb = speed / 1024 / 1024 if speed else 0
        eta_str = f"{eta}秒" if eta else "?"
        
        self.status_text = f"下载中... {speed_mb:.1f}MB/s, 剩余{eta_str}"
    
    def _download_complete(self, success, message):
        """下载完成"""
        self.is_downloading = False
        self.progress_value = 100 if success else self.progress_value
        self.status_text = message
        
        # 重置进度条
        if success:
            Clock.schedule_once(lambda dt: self._reset_progress(), 2)
    
    def _reset_progress(self):
        """重置进度"""
        self.progress_value = 0
        self.status_text = "就绪"
    
    def get_info(self):
        """获取视频信息"""
        if not self.url_input:
            self.status_text = "请输入 URL"
            return
        
        self.status_text = "正在获取信息..."
        
        def callback(dt):
            info = self.downloader.get_info(self.url_input)
            if info["success"]:
                title = info.get("title", "未知")
                uploader = info.get("uploader", "未知")
                duration = info.get("duration", 0)
                duration_str = f"{duration // 60}:{duration % 60:02d}"
                self.status_text = f"{title} - {uploader} ({duration_str})"
            else:
                self.status_text = f"获取失败：{info.get('error', '未知错误')}"
        
        Clock.schedule_once(callback, 0.1)
    
    def convert_file(self, file_path, output_format):
        """转换文件格式"""
        if not os.path.exists(file_path):
            self.status_text = "文件不存在"
            return
        
        self.status_text = "正在转换..."
        
        def callback(dt):
            result = self.converter.convert(file_path, output_format)
            if result["success"]:
                self.status_text = f"转换完成：{os.path.basename(result['output_file'])}"
            else:
                self.status_text = f"转换失败：{result.get('error', '未知错误')}"
        
        Clock.schedule_once(callback, 0.1)
    
    def download_playlist(self, url, max_count=None):
        """下载歌单"""
        self.status_text = "正在下载歌单..."
        self.is_downloading = True
        
        def callback(dt):
            result = self.batch_downloader.download_playlist(
                url, 
                format=self.selected_format,
                max_count=max_count,
            )
            
            if result["success"]:
                self.status_text = f"歌单下载完成：{result['downloaded']}/{result['total']} 首"
            else:
                self.status_text = f"歌单下载失败：{result.get('errors', ['未知错误'])[0]}"
            
            self.is_downloading = False
        
        Clock.schedule_once(callback, 0.1)


# KV 界面定义（内嵌）
KV = """
<MainScreen>:
    name: "main"
    
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 15
        
        # 标题
        Label:
            text: "🎵 音乐抓取"
            font_size: "28sp"
            bold: True
            size_hint_y: None
            height: "50dp"
        
        # URL 输入框
        TextInput:
            id: url_input
            hint_text: "粘贴视频/音频链接..."
            multiline: False
            text: root.url_input
            on_text: root.url_input = self.text
            size_hint_y: None
            height: "50dp"
            font_size: "16sp"
        
        # 格式选择
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            spacing: 10
            
            Label:
                text: "格式:"
                size_hint_x: None
                width: "60dp"
            
            Spinner:
                id: format_spinner
                text: root.selected_format
                values: ["mp3", "wav", "flac", "m4a", "ogg"]
                on_text: root.selected_format = self.text
                size_hint_x: None
                width: "100dp"
        
        # 获取信息按钮
        Button:
            text: "📊 获取信息"
            size_hint_y: None
            height: "45dp"
            on_release: root.get_info()
        
        # 下载按钮
        Button:
            text: "⬇️ 下载" if not root.is_downloading else "下载中..."
            disabled: root.is_downloading
            size_hint_y: None
            height: "50dp"
            bold: True
            on_release: root.start_download()
        
        # 进度条
        BoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: "60dp"
            spacing: 5
            
            Label:
                text: root.status_text
                size_hint_y: None
                height: "25dp"
            
            ProgressBar:
                max: root.progress_max
                value: root.progress_value
                size_hint_y: None
                height: "25dp"
        
        # 批量下载按钮
        BoxLayout:
            size_hint_y: None
            height: "45dp"
            spacing: 10
            
            Button:
                text: "📁 歌单下载"
                on_release: app.show_playlist_dialog()
            
            Button:
                text: "🔄 格式转换"
                on_release: app.show_convert_dialog()
        
        # 版权提示
        Label:
            text: "⚠️ 仅用于下载无版权或自有内容"
            color: 0.7, 0.7, 0.7, 1
            font_size: "12sp"
            size_hint_y: None
            height: "30dp"
"""
