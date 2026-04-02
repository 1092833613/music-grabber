"""
音乐抓取核心 - 下载模块
基于 yt-dlp 实现通用音频下载

改进：
- 改进 3: 完善错误处理
- 改进 4: 添加网络重试机制
- 改进 6: 优化下载目录
"""

import yt_dlp
import os
import logging
from typing import Optional, Callable, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ========== 改进 4: 网络重试机制 ==========
def create_session_with_retry():
    """创建带重试机制的 HTTP Session"""
    session = requests.Session()
    retry = Retry(
        total=3,  # 最多重试 3 次
        backoff_factor=0.3,  # 重试间隔：0.3s, 0.6s, 1.2s
        status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的状态码
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
# ===========================================


class MusicDownloader:
    """通用音频下载器"""
    
    def __init__(self, output_dir: Optional[str] = None):
        # ========== 改进 6: 使用 Android 标准目录 ==========
        if output_dir is None:
            try:
                from android.storage import app_storage_path
                output_dir = os.path.join(app_storage_path(), "Music")
            except ImportError:
                # Desktop fallback
                output_dir = os.path.join(os.path.expanduser("~"), "Music", "music_grabber")
        
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        # ===========================================
        
        # 初始化带重试的 session
        self.session = create_session_with_retry()
        
    def download(self, 
                 url: str, 
                 format: str = "mp3",
                 progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
                 ) -> Dict[str, Any]:
        """
        下载音频
        
        Args:
            url: 视频/音频链接
            format: 输出格式 (mp3/m4a/wav/flac)
            progress_callback: 进度回调函数
            
        Returns:
            下载结果字典
        """
        result = {
            "success": False,
            "filename": None,
            "error": None,
            "info": {}
        }
        
        # yt-dlp 配置
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": format,
                "preferredquality": "192",
            }],
            "outtmpl": os.path.join(self.output_dir, "%(title)s.%(ext)s"),
            "noplaylist": True,  # 单个下载，批量下载用 batch 模块
            "quiet": True,
            "no_warnings": True,
        }
        
        # 添加进度回调
        if progress_callback:
            def hook(d):
                if d["status"] == "downloading":
                    progress_callback({
                        "status": "downloading",
                        "downloaded_bytes": d.get("downloaded_bytes", 0),
                        "total_bytes": d.get("total_bytes", 0),
                        "speed": d.get("speed", 0),
                        "eta": d.get("eta", 0),
                    })
                elif d["status"] == "finished":
                    progress_callback({
                        "status": "finished",
                        "filename": d.get("filename"),
                    })
            
            ydl_opts["progress_hooks"] = [hook]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 提取信息
                info = ydl.extract_info(url, download=True)
                result["info"] = {
                    "title": info.get("title", "Unknown"),
                    "uploader": info.get("uploader", "Unknown"),
                    "duration": info.get("duration", 0),
                    "url": url,
                }
                result["success"] = True
                result["filename"] = os.path.join(
                    self.output_dir, 
                    f"{info.get('title', 'unknown')}.{format}"
                )
        except yt_dlp.utils.DownloadError as e:
            error_msg = f"下载失败：{str(e)}"
            result["error"] = error_msg
            logger.error(error_msg)
            if progress_callback:
                progress_callback({
                    "status": "error",
                    "error": error_msg,
                })
        except Exception as e:
            error_msg = f"未知错误：{str(e)}"
            result["error"] = error_msg
            logger.exception(e)
            if progress_callback:
                progress_callback({
                    "status": "error",
                    "error": error_msg,
                })
        
        return result
    
    def get_info(self, url: str) -> Dict[str, Any]:
        """获取视频/音频信息（不下载）"""
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    "success": True,
                    "title": info.get("title", "Unknown"),
                    "uploader": info.get("uploader", "Unknown"),
                    "duration": info.get("duration", 0),
                    "thumbnail": info.get("thumbnail", ""),
                    "url": url,
                }
        except yt_dlp.utils.DownloadError as e:
            error_msg = f"获取信息失败：{str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
            }
        except Exception as e:
            error_msg = f"未知错误：{str(e)}"
            logger.exception(e)
            return {
                "success": False,
                "error": error_msg,
            }


# 测试
if __name__ == "__main__":
    downloader = MusicDownloader()
    
    # 测试获取信息
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    info = downloader.get_info(test_url)
    print(f"信息获取: {info}")
