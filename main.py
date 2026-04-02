"""
音乐抓取 App - 最简化测试版本
用于诊断闪退问题
"""

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class TestApp(App):
    """最简化测试 App"""
    
    def build(self):
        self.title = "Test - 音乐抓取"
        
        # 最简单的 UI
        layout = BoxLayout(orientation='vertical')
        
        label1 = Label(
            text='如果能看到这个说明正常！',
            font_size='20sp'
        )
        
        label2 = Label(
            text='Android 版本测试',
            font_size='16sp'
        )
        
        layout.add_widget(label1)
        layout.add_widget(label2)
        
        return layout


if __name__ == "__main__":
    TestApp().run()
