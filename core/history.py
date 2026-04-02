"""
下载历史记录模块
记录所有下载历史，支持查询和重新下载
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional


class DownloadHistory:
    """下载历史管理器"""
    
    def __init__(self, data_file: str = "./data/history.json"):
        self.data_file = data_file
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """加载历史记录"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_history(self):
        """保存历史记录"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add(self, 
            url: str, 
            title: str, 
            filename: str,
            artist: str = "",
            duration: int = 0,
            format: str = "mp3"
            ):
        """
        添加下载记录
        
        Args:
            url: 原始链接
            title: 标题
            filename: 保存的文件名
            artist: 歌手
            duration: 时长（秒）
            format: 格式
        """
        record = {
            "id": len(self.history) + 1,
            "url": url,
            "title": title,
            "artist": artist,
            "filename": filename,
            "duration": duration,
            "format": format,
            "downloaded_at": datetime.now().isoformat(),
            "file_exists": os.path.exists(filename),
        }
        
        self.history.insert(0, record)  # 新记录在前
        self._save_history()
    
    def get_all(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取所有历史记录"""
        return self.history[:limit]
    
    def search(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索历史记录"""
        keyword = keyword.lower()
        return [
            record for record in self.history
            if keyword in record["title"].lower() or 
               keyword in record.get("artist", "").lower()
        ]
    
    def delete(self, record_id: int) -> bool:
        """删除记录"""
        for i, record in enumerate(self.history):
            if record["id"] == record_id:
                del self.history[i]
                self._save_history()
                return True
        return False
    
    def clear(self):
        """清空历史"""
        self.history = []
        self._save_history()
    
    def get_recent(self, days: int = 7) -> List[Dict[str, Any]]:
        """获取最近 N 天的记录"""
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        return [
            record for record in self.history
            if datetime.fromisoformat(record["downloaded_at"]).timestamp() > cutoff
        ]
    
    def count(self) -> int:
        """获取记录总数"""
        return len(self.history)


# 测试
if __name__ == "__main__":
    history = DownloadHistory()
    
    # 测试添加
    history.add(
        url="https://example.com/video",
        title="测试歌曲",
        artist="测试歌手",
        filename="./downloads/test.mp3",
        duration=180,
    )
    
    print(f"历史记录总数：{history.count()}")
