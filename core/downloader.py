"""
音乐抓取核心 - 下载模块
基于 yt-dlp 实现通用音频下载
"""

import yt_dlp
import os
from typing import Optional, Callable, Dict, Any


class MusicDownloader:
    """通用音频下载器"""
    
    def __init__(self, output_dir: str = "./downloads"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
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
        except Exception as e:
            result["error"] = str(e)
            if progress_callback:
                progress_callback({
                    "status": "error",
                    "error": str(e),
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
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }


# 测试
if __name__ == "__main__":
    downloader = MusicDownloader()
    
    # 测试获取信息
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    info = downloader.get_info(test_url)
    print(f"信息获取: {info}")
