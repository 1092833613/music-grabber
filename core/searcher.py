"""
音乐搜索模块
支持多音源搜索：YouTube、SoundCloud、网易云等
"""

import yt_dlp
from typing import List, Dict, Any, Optional


class MusicSearcher:
    """音乐搜索器"""
    
    # 支持的搜索音源
    SUPPORTED_SITES = {
        "youtube": "ytsearch",
        "soundcloud": "scsearch",
        "bandcamp": "bcsearch",
    }
    
    def __init__(self):
        pass
    
    def search(self, 
               query: str, 
               site: str = "youtube",
               max_results: int = 20
               ) -> Dict[str, Any]:
        """
        搜索音乐
        
        Args:
            query: 搜索关键词
            site: 音源（youtube/soundcloud/bandcamp）
            max_results: 最大结果数
            
        Returns:
            搜索结果列表
        """
        result = {
            "success": False,
            "results": [],
            "error": None,
        }
        
        # 获取搜索前缀
        site_prefix = self.SUPPORTED_SITES.get(site, "ytsearch")
        search_query = f"{site_prefix}{max_results}:{query}"
        
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,  # 只提取基本信息，不获取详情
            "default_search": site_prefix,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                
                entries = info.get("entries", [])
                for entry in entries:
                    if entry:
                        result["results"].append({
                            "id": entry.get("id", ""),
                            "title": entry.get("title", "Unknown"),
                            "uploader": entry.get("uploader", "Unknown"),
                            "duration": entry.get("duration", 0),
                            "url": f"https://www.youtube.com/watch?v={entry.get('id', '')}",
                            "thumbnail": entry.get("thumbnail", ""),
                        })
                
                result["success"] = True
                result["total"] = len(result["results"])
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def search_all_sites(self, 
                         query: str, 
                         max_results: int = 10
                         ) -> Dict[str, Any]:
        """
        在所有音源搜索
        
        Args:
            query: 搜索关键词
            max_results: 每个音源最大结果数
            
        Returns:
            所有音源的搜索结果
        """
        all_results = {
            "success": True,
            "query": query,
            "by_site": {},
            "total": 0,
        }
        
        for site in self.SUPPORTED_SITES.keys():
            result = self.search(query, site, max_results)
            if result["success"]:
                all_results["by_site"][site] = result["results"]
                all_results["total"] += len(result["results"])
        
        return all_results
    
    def get_search_suggestions(self, query: str) -> List[str]:
        """
        获取搜索建议（简单实现）
        
        Args:
            query: 输入关键词
            
        Returns:
            建议列表
        """
        # 简单实现：返回常见组合
        suggestions = [
            query,
            f"{query} 完整版",
            f"{query} 现场版",
            f"{query} MV",
            f"{query} 歌词",
        ]
        return suggestions


# 测试
if __name__ == "__main__":
    searcher = MusicSearcher()
    
    # 测试搜索
    result = searcher.search("周杰伦 七里香", max_results=5)
    print(f"搜索结果：{result['total']} 条")
    for item in result["results"][:3]:
        print(f"  - {item['title']} ({item['uploader']})")
