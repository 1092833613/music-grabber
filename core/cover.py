"""
封面图下载模块
支持自动下载专辑封面并嵌入 ID3 标签
"""

import yt_dlp
import requests
import os
import re
from typing import Optional, Dict, Any


class CoverDownloader:
    """封面图下载器"""
    
    def __init__(self, output_dir: str = "./downloads"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def get_cover_from_url(self, url: str) -> Dict[str, Any]:
        """
        从视频/音频链接获取封面
        
        Args:
            url: 视频/音频链接
            
        Returns:
            封面信息
        """
        result = {
            "success": False,
            "cover_url": None,
            "error": None,
        }
        
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # 获取封面 URL
                cover_url = info.get("thumbnail")
                
                if cover_url:
                    result["success"] = True
                    result["cover_url"] = cover_url
                    result["title"] = info.get("title", "Unknown")
                else:
                    result["error"] = "未找到封面"
                    
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def download_cover(self, 
                       cover_url: str, 
                       output_file: Optional[str] = None,
                       title: str = "cover"
                       ) -> Dict[str, Any]:
        """
        下载封面图
        
        Args:
            cover_url: 封面图 URL
            output_file: 输出文件路径
            title: 标题（用于自动生成文件名）
            
        Returns:
            下载结果
        """
        result = {
            "success": False,
            "filename": None,
            "error": None,
        }
        
        try:
            # 下载图片
            resp = requests.get(cover_url, timeout=10)
            resp.raise_for_status()
            
            # 确定输出路径
            if output_file is None:
                safe_title = re.sub(r'[^\w\s-]', '', title).strip()
                output_file = os.path.join(self.output_dir, f"{safe_title}_cover.jpg")
            
            # 保存图片
            with open(output_file, "wb") as f:
                f.write(resp.content)
            
            result["success"] = True
            result["filename"] = output_file
            
        except Exception as e:
            result["error"] = f"下载失败：{str(e)}"
        
        return result
    
    def embed_cover_to_audio(self, 
                             audio_file: str, 
                             cover_file: str,
                             title: str = "",
                             artist: str = ""
                             ) -> Dict[str, Any]:
        """
        将封面嵌入音频文件（ID3 标签）
        
        Args:
            audio_file: 音频文件路径
            cover_file: 封面文件路径
            title: 歌曲名
            artist: 歌手名
            
        Returns:
            处理结果
        """
        result = {
            "success": False,
            "error": None,
        }
        
        try:
            from mutagen.id3 import ID3, APIC, TIT2, TPE1, ID3NoHeaderError
            from mutagen.mp3 import MP3
            
            # 检查文件
            if not os.path.exists(audio_file):
                result["error"] = "音频文件不存在"
                return result
            
            if not os.path.exists(cover_file):
                result["error"] = "封面文件不存在"
                return result
            
            # 读取音频文件
            try:
                audio = MP3(audio_file, ID3=ID3)
            except ID3NoHeaderError:
                audio = MP3(audio_file)
                audio.add_tags()
            
            # 读取封面图片
            with open(cover_file, "rb") as f:
                cover_data = f.read()
            
            # 设置 ID3 标签
            audio.tags["APIC"] = APIC(
                encoding=3,
                mime="image/jpeg",
                type=3,  # 封面
                desc="Cover",
                data=cover_data
            )
            
            if title:
                audio.tags["TIT2"] = TIT2(encoding=3, text=title)
            
            if artist:
                audio.tags["TPE1"] = TPE1(encoding=3, text=artist)
            
            # 保存
            audio.save()
            
            result["success"] = True
            
        except ImportError:
            result["error"] = "需要安装 mutagen 库：pip install mutagen"
        except Exception as e:
            result["error"] = f"嵌入失败：{str(e)}"
        
        return result
    
    def download_and_embed(self,
                           url: str,
                           audio_file: str,
                           title: str = "",
                           artist: str = ""
                           ) -> Dict[str, Any]:
        """
        一站式：下载封面并嵌入音频
        
        Args:
            url: 视频/音频链接
            audio_file: 音频文件路径
            title: 歌曲名
            artist: 歌手名
            
        Returns:
            处理结果
        """
        result = {
            "success": False,
            "cover_file": None,
            "error": None,
        }
        
        # 获取封面 URL
        cover_info = self.get_cover_from_url(url)
        if not cover_info["success"]:
            result["error"] = cover_info.get("error", "获取封面失败")
            return result
        
        # 下载封面
        cover_result = self.download_cover(
            cover_info["cover_url"],
            title=title or cover_info.get("title", "cover")
        )
        
        if not cover_result["success"]:
            result["error"] = cover_result.get("error", "下载封面失败")
            return result
        
        result["cover_file"] = cover_result["filename"]
        
        # 嵌入封面到音频
        embed_result = self.embed_cover_to_audio(
            audio_file,
            cover_result["filename"],
            title,
            artist
        )
        
        if not embed_result["success"]:
            result["error"] = embed_result.get("error", "嵌入封面失败")
            return result
        
        result["success"] = True
        return result


# 测试
if __name__ == "__main__":
    downloader = CoverDownloader()
    print("封面下载模块已加载")
