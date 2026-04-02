# 核心模块
from .downloader import MusicDownloader
from .converter import AudioConverter
from .batch import BatchDownloader
from .searcher import MusicSearcher
from .lyrics import LyricsDownloader
from .cover import CoverDownloader
from .history import DownloadHistory
from .playlist import PlaylistManager

__all__ = [
    "MusicDownloader",
    "AudioConverter", 
    "BatchDownloader",
    "MusicSearcher",
    "LyricsDownloader",
    "CoverDownloader",
    "DownloadHistory",
    "PlaylistManager",
]
