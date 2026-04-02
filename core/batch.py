"""
音乐抓取核心 - 批量下载模块
支持歌单、专辑、列表批量下载
"""

import yt_dlp
import os
from typing import List, Optional, Callable, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed


class BatchDownloader:
    """批量下载器"""
    
    def __init__(self, output_dir: str = "./downloads"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def download_playlist(self, 
                          url: str, 
                          format: str = "mp3",
                          max_count: Optional[int] = None,
                          progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
                          ) -> Dict[str, Any]:
        """
        下载歌单/专辑
        
        Args:
            url: 歌单链接
            format: 输出格式
            max_count: 最大下载数量（None=全部）
            progress_callback: 进度回调
            
        Returns:
            批量下载结果
        """
        result = {
            "success": False,
            "total": 0,
            "downloaded": 0,
            "failed": 0,
            "files": [],
            "errors": [],
        }
        
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": format,
                "preferredquality": "192",
            }],
            "outtmpl": os.path.join(self.output_dir, "%(playlist)s/%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "noplaylist": False,  # 下载整个歌单
        }
        
        if max_count:
            ydl_opts["playlistend"] = max_count
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 提取歌单信息
                info = ydl.extract_info(url, download=True)
                
                entries = info.get("entries", [])
                result["total"] = len(entries)
                
                # 统计结果
                for entry in entries:
                    if entry:
                        result["downloaded"] += 1
                        filename = os.path.join(
                            self.output_dir,
                            info.get("title", "playlist"),
                            f"{entry.get('title', 'unknown')}.{format}"
                        )
                        result["files"].append({
                            "title": entry.get("title", "Unknown"),
                            "filename": filename,
                        })
                
                result["success"] = True
                
        except Exception as e:
            result["errors"].append(str(e))
        
        return result
    
    def download_list(self, 
                      urls: List[str], 
                      format: str = "mp3",
                      max_workers: int = 3,
                      progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
                      ) -> Dict[str, Any]:
        """
        批量下载多个独立链接
        
        Args:
            urls: URL 列表
            format: 输出格式
            max_workers: 并发数
            progress_callback: 进度回调
            
        Returns:
            批量下载结果
        """
        from .downloader import MusicDownloader
        
        result = {
            "success": True,
            "total": len(urls),
            "downloaded": 0,
            "failed": 0,
            "files": [],
            "errors": [],
        }
        
        downloader = MusicDownloader(self.output_dir)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(downloader.download, url, format): url 
                for url in urls
            }
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    res = future.result()
                    if res["success"]:
                        result["downloaded"] += 1
                        result["files"].append(res)
                    else:
                        result["failed"] += 1
                        result["errors"].append({
                            "url": url,
                            "error": res["error"],
                        })
                except Exception as e:
                    result["failed"] += 1
                    result["errors"].append({
                        "url": url,
                        "error": str(e),
                    })
                
                if progress_callback:
                    progress_callback({
                        "total": result["total"],
                        "downloaded": result["downloaded"],
                        "failed": result["failed"],
                    })
        
        return result


# 测试
if __name__ == "__main__":
    batch = BatchDownloader()
    print("批量下载模块已加载")
