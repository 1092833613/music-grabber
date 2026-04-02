"""
歌词下载模块
支持自动匹配和下载歌词（LRC 格式）
"""

import requests
import os
import re
from typing import Optional, Dict, Any


class LyricsDownloader:
    """歌词下载器"""
    
    def __init__(self, output_dir: str = "./downloads"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def search_lyrics(self, 
                      title: str, 
                      artist: str = ""
                      ) -> Optional[str]:
        """
        搜索歌词
        
        Args:
            title: 歌曲名
            artist: 歌手名
            
        Returns:
            歌词文本（LRC 格式）或 None
        """
        # 方法 1: 使用网易云音乐 API（公开接口）
        lyrics = self._search_netease(title, artist)
        if lyrics:
            return lyrics
        
        # 方法 2: 使用 QQ 音乐 API
        lyrics = self._search_qq(title, artist)
        if lyrics:
            return lyrics
        
        return None
    
    def _search_netease(self, title: str, artist: str) -> Optional[str]:
        """从网易云音乐搜索歌词"""
        try:
            # 搜索歌曲
            search_url = "https://music.163.com/api/search/get"
            params = {
                "s": f"{title} {artist}",
                "type": 1,
                "limit": 1,
            }
            
            headers = {
                "Referer": "https://music.163.com/",
                "User-Agent": "Mozilla/5.0",
            }
            
            resp = requests.get(search_url, params=params, headers=headers, timeout=5)
            data = resp.json()
            
            if data["result"]["songCount"] > 0:
                song_id = data["result"]["songs"][0]["id"]
                
                # 获取歌词
                lyrics_url = "https://music.163.com/api/song/lyric"
                params = {"id": song_id, "lv": 1}
                
                resp = requests.get(lyrics_url, params=params, headers=headers, timeout=5)
                data = resp.json()
                
                if "lrc" in data and data["lrc"]["lyric"]:
                    return data["lrc"]["lyric"]
        except Exception as e:
            print(f"网易云歌词搜索失败：{e}")
        
        return None
    
    def _search_qq(self, title: str, artist: str) -> Optional[str]:
        """从 QQ 音乐搜索歌词"""
        try:
            search_url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
            params = {
                "w": f"{title} {artist}",
                "format": "json",
            }
            
            headers = {
                "Referer": "https://y.qq.com/",
                "User-Agent": "Mozilla/5.0",
            }
            
            resp = requests.get(search_url, params=params, headers=headers, timeout=5)
            text = resp.text[9:-1]  # 去掉 JSONP 包装
            data = eval(text)
            
            if data["data"]["song"]["total"] > 0:
                songmid = data["data"]["song"]["list"][0]["songmid"]
                
                # 获取歌词
                lyrics_url = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg"
                params = {"songmid": songmid, "format": "json"}
                
                resp = requests.get(lyrics_url, params=params, headers=headers, timeout=5)
                text = resp.text[18:-1]
                data = eval(text)
                
                import base64
                if "lyric" in data:
                    lyrics = base64.b64decode(data["lyric"]).decode("utf-8")
                    return lyrics
        except Exception as e:
            print(f"QQ 音乐歌词搜索失败：{e}")
        
        return None
    
    def download_lyrics(self, 
                        title: str, 
                        artist: str = "",
                        output_file: Optional[str] = None
                        ) -> Dict[str, Any]:
        """
        下载歌词并保存
        
        Args:
            title: 歌曲名
            artist: 歌手名
            output_file: 输出文件路径（默认自动生成）
            
        Returns:
            下载结果
        """
        result = {
            "success": False,
            "filename": None,
            "error": None,
        }
        
        # 搜索歌词
        lyrics = self.search_lyrics(title, artist)
        
        if not lyrics:
            result["error"] = "未找到歌词"
            return result
        
        # 保存歌词
        if output_file is None:
            safe_title = re.sub(r'[^\w\s-]', '', title).strip()
            safe_artist = re.sub(r'[^\w\s-]', '', artist).strip()
            filename = f"{safe_artist} - {safe_title}.lrc"
            output_file = os.path.join(self.output_dir, filename)
        
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(lyrics)
            
            result["success"] = True
            result["filename"] = output_file
            
        except Exception as e:
            result["error"] = f"保存失败：{str(e)}"
        
        return result
    
    def parse_lrc(self, lyrics_text: str) -> list:
        """
        解析 LRC 歌词
        
        Args:
            lyrics_text: LRC 格式歌词文本
            
        Returns:
            解析后的歌词列表 [(时间，文本), ...]
        """
        parsed = []
        
        # LRC 时间格式：[mm:ss.xx]
        time_pattern = re.compile(r'\[(\d{2}):(\d{2})\.(\d{2,3})\]')
        
        for line in lyrics_text.split("\n"):
            match = time_pattern.search(line)
            if match:
                minutes = int(match.group(1))
                seconds = int(match.group(2))
                milliseconds = int(match.group(3).ljust(3, '0'))
                time_ms = minutes * 60000 + seconds * 1000 + milliseconds
                
                text = time_pattern.sub("", line).strip()
                if text:
                    parsed.append((time_ms, text))
        
        return parsed


# 测试
if __name__ == "__main__":
    downloader = LyricsDownloader()
    
    # 测试搜索
    lyrics = downloader.search_lyrics("七里香", "周杰伦")
    if lyrics:
        print("找到歌词！")
        print(lyrics[:200])  # 打印前 200 字符
    else:
        print("未找到歌词")
