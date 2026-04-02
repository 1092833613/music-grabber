"""
音乐抓取核心 - 格式转换模块
基于 pydub 实现音频格式转换
"""

from pydub import AudioSegment
import os
from typing import Optional, Dict, Any


class AudioConverter:
    """音频格式转换器"""
    
    SUPPORTED_FORMATS = ["mp3", "wav", "flac", "m4a", "ogg", "aac"]
    
    def __init__(self):
        pass
    
    def convert(self, 
                input_file: str, 
                output_format: str = "mp3",
                bitrate: str = "192k",
                output_dir: Optional[str] = None
                ) -> Dict[str, Any]:
        """
        转换音频格式
        
        Args:
            input_file: 输入文件路径
            output_format: 输出格式
            bitrate: 比特率
            output_dir: 输出目录（默认同输入文件）
            
        Returns:
            转换结果
        """
        result = {
            "success": False,
            "output_file": None,
            "error": None,
        }
        
        if output_format not in self.SUPPORTED_FORMATS:
            result["error"] = f"不支持的格式：{output_format}"
            return result
        
        if not os.path.exists(input_file):
            result["error"] = f"文件不存在：{input_file}"
            return result
        
        try:
            # 加载音频
            audio = AudioSegment.from_file(input_file)
            
            # 确定输出路径
            if output_dir is None:
                output_dir = os.path.dirname(input_file)
            
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(output_dir, f"{base_name}.{output_format}")
            
            # 导出
            audio.export(
                output_file, 
                format=output_format,
                bitrate=bitrate,
            )
            
            result["success"] = True
            result["output_file"] = output_file
            
        except Exception as e:
            result["error"] = f"转换失败：{str(e)}"
        
        return result
    
    def get_audio_info(self, file_path: str) -> Dict[str, Any]:
        """获取音频信息"""
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": "文件不存在",
            }
        
        try:
            audio = AudioSegment.from_file(file_path)
            return {
                "success": True,
                "duration_seconds": len(audio) / 1000,
                "channels": audio.channels,
                "sample_rate": audio.frame_rate,
                "format": os.path.splitext(file_path)[1][1:],
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }


# 测试
if __name__ == "__main__":
    converter = AudioConverter()
    print(f"支持格式：{converter.SUPPORTED_FORMATS}")
