"""
播放列表管理模块
支持创建、编辑、导入/导出播放列表
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional


class PlaylistManager:
    """播放列表管理器"""
    
    def __init__(self, data_file: str = "./data/playlists.json"):
        self.data_file = data_file
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        self.playlists = self._load_playlists()
    
    def _load_playlists(self) -> Dict[str, Any]:
        """加载播放列表"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {"playlists": []}
        return {"playlists": []}
    
    def _save_playlists(self):
        """保存播放列表"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.playlists, f, ensure_ascii=False, indent=2)
    
    def create(self, name: str, description: str = "") -> Dict[str, Any]:
        """
        创建播放列表
        
        Args:
            name: 播放列表名
            description: 描述
            
        Returns:
            播放列表信息
        """
        playlist = {
            "id": len(self.playlists["playlists"]) + 1,
            "name": name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "tracks": [],
        }
        
        self.playlists["playlists"].append(playlist)
        self._save_playlists()
        
        return playlist
    
    def add_track(self, 
                  playlist_id: int, 
                  track: Dict[str, Any]
                  ) -> bool:
        """
        添加歌曲到播放列表
        
        Args:
            playlist_id: 播放列表 ID
            track: 歌曲信息 {title, artist, url, filename, ...}
            
        Returns:
            是否成功
        """
        for playlist in self.playlists["playlists"]:
            if playlist["id"] == playlist_id:
                track["added_at"] = datetime.now().isoformat()
                playlist["tracks"].append(track)
                playlist["updated_at"] = datetime.now().isoformat()
                self._save_playlists()
                return True
        return False
    
    def remove_track(self, 
                     playlist_id: int, 
                     track_index: int
                     ) -> bool:
        """
        从播放列表移除歌曲
        
        Args:
            playlist_id: 播放列表 ID
            track_index: 歌曲索引
            
        Returns:
            是否成功
        """
        for playlist in self.playlists["playlists"]:
            if playlist["id"] == playlist_id:
                if 0 <= track_index < len(playlist["tracks"]):
                    del playlist["tracks"][track_index]
                    playlist["updated_at"] = datetime.now().isoformat()
                    self._save_playlists()
                    return True
        return False
    
    def get_all(self) -> List[Dict[str, Any]]:
        """获取所有播放列表"""
        return self.playlists["playlists"]
    
    def get(self, playlist_id: int) -> Optional[Dict[str, Any]]:
        """获取指定播放列表"""
        for playlist in self.playlists["playlists"]:
            if playlist["id"] == playlist_id:
                return playlist
        return None
    
    def delete(self, playlist_id: int) -> bool:
        """删除播放列表"""
        for i, playlist in enumerate(self.playlists["playlists"]):
            if playlist["id"] == playlist_id:
                del self.playlists["playlists"][i]
                self._save_playlists()
                return True
        return False
    
    def export(self, playlist_id: int, output_file: str) -> Dict[str, Any]:
        """
        导出播放列表
        
        Args:
            playlist_id: 播放列表 ID
            output_file: 输出文件路径
            
        Returns:
            导出结果
        """
        result = {
            "success": False,
            "error": None,
        }
        
        playlist = self.get(playlist_id)
        if not playlist:
            result["error"] = "播放列表不存在"
            return result
        
        try:
            export_data = {
                "name": playlist["name"],
                "description": playlist["description"],
                "created_at": playlist["created_at"],
                "track_count": len(playlist["tracks"]),
                "tracks": playlist["tracks"],
            }
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            result["success"] = True
            result["filename"] = output_file
            
        except Exception as e:
            result["error"] = f"导出失败：{str(e)}"
        
        return result
    
    def import_playlist(self, input_file: str) -> Dict[str, Any]:
        """
        导入播放列表
        
        Args:
            input_file: 输入文件路径
            
        Returns:
            导入结果
        """
        result = {
            "success": False,
            "playlist_id": None,
            "error": None,
        }
        
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 创建新播放列表
            playlist = self.create(
                name=data.get("name", "导入的播放列表"),
                description=data.get("description", "")
            )
            
            # 添加歌曲
            for track in data.get("tracks", []):
                self.add_track(playlist["id"], track)
            
            result["success"] = True
            result["playlist_id"] = playlist["id"]
            
        except Exception as e:
            result["error"] = f"导入失败：{str(e)}"
        
        return result


# 测试
if __name__ == "__main__":
    manager = PlaylistManager()
    
    # 测试创建
    playlist = manager.create("我的最爱", "最喜欢的歌曲")
    print(f"创建播放列表：{playlist['name']}")
    
    # 测试添加歌曲
    manager.add_track(playlist["id"], {
        "title": "测试歌曲",
        "artist": "测试歌手",
        "url": "https://example.com",
    })
    
    print(f"播放列表歌曲数：{len(playlist['tracks'])}")
