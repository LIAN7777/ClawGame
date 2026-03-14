"""
ClawGame - 文本输入框组件
用于玩家输入对话内容
"""

import pygame
from typing import Optional, Callable, List
import os


def _get_chinese_font(size: int) -> pygame.font.Font:
    """获取支持中文的字体"""
    chinese_font_names = [
        'Microsoft YaHei',
        'microsoftyahei',
        'SimHei',
        'simhei',
        'Noto Sans CJK SC',
        'Noto Sans CJK',
        'noto sans cjk',
        'PingFang SC',
        'Droid Sans Fallback',
    ]
    
    for font_name in chinese_font_names:
        try:
            font = pygame.font.SysFont(font_name, size)
            test_surface = font.render('你好', True, (0, 0, 0))
            w, h = test_surface.get_size()
            if w > 15 and h > 5:
                return font
        except Exception:
            continue
    
    # 尝试加载字体文件
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = pygame.font.Font(font_path, size)
                return font
            except Exception:
                continue
    
    return pygame.font.Font(None, size)


class TextInput:
    """
    文本输入框组件
    
    显示在屏幕底部，允许玩家输入对话内容。
    """
    
    def __init__(
        self,
        width: int = 400,
        height: int = 50,
        font_size: int = 20,
        placeholder: str = "输入对话内容...",
        max_length: int = 100
    ):
        """
        初始化输入框
        
        Args:
            width: 输入框宽度
            height: 输入框高度
            font_size: 字体大小
            placeholder: 占位文本
            max_length: 最大字符数
        """
        self.width = width
        self.height = height
        self.font_size = font_size
        self.placeholder = placeholder
        self.max_length = max_length
        
        # 输入状态
        self.text: str = ""
        self.active: bool = False
        self.visible: bool = False
        
        # 光标状态
        self.cursor_visible: bool = True
        self.cursor_timer: float = 0.0
        self.cursor_blink_interval: float = 0.5  # 闪烁间隔
        
        # 字体
        self.font = _get_chinese_font(font_size)
        
        # 颜色
        self.colors = {
            "background": (40, 40, 50),
            "border": (100, 100, 120),
            "border_active": (150, 150, 200),
            "text": (255, 255, 255),
            "placeholder": (150, 150, 150),
            "cursor": (255, 255, 255),
        }
        
        # 回调函数
        self.on_submit: Optional[Callable[[str], None]] = None
        self.on_cancel: Optional[Callable[[], None]] = None
    
    def show(self) -> None:
        """显示输入框"""
        self.visible = True
        self.active = True
        self.text = ""
        self.cursor_visible = True
        self.cursor_timer = 0.0
    
    def hide(self) -> None:
        """隐藏输入框"""
        self.visible = False
        self.active = False
        self.text = ""
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        处理事件
        
        Args:
            event: pygame 事件
            
        Returns:
            是否处理了事件（用于阻止事件传播）
        """
        if not self.visible or not self.active:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # 回车提交
                self._submit()
                return True
            elif event.key == pygame.K_ESCAPE:
                # ESC 取消
                self._cancel()
                return True
            elif event.key == pygame.K_BACKSPACE:
                # 退格删除
                if self.text:
                    self.text = self.text[:-1]
                return True
        
        elif event.type == pygame.TEXTINPUT:
            # 文本输入（包括中文输入法的最终输入）
            if len(self.text) < self.max_length:
                self.text += event.text
            return True
        
        elif event.type == pygame.TEXTEDITING:
            # 输入法组合中（正在输入拼音等）
            # 这个事件表示输入法正在工作，不需要特别处理
            # 但需要返回 True 表示我们在处理输入法事件
            return True
        
        return False
    
    def update(self, dt: float) -> None:
        """
        更新状态
        
        Args:
            dt: 时间增量（秒）
        """
        if not self.visible:
            return
        
        # 光标闪烁
        self.cursor_timer += dt
        if self.cursor_timer >= self.cursor_blink_interval:
            self.cursor_timer = 0.0
            self.cursor_visible = not self.cursor_visible
    
    def render(self, surface: pygame.Surface) -> None:
        """
        渲染输入框
        
        Args:
            surface: 目标渲染表面
        """
        if not self.visible:
            return
        
        # 计算位置（屏幕底部居中）
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        
        x = (screen_width - self.width) // 2
        y = screen_height - self.height - 20  # 底部留20px边距
        
        # 绘制背景
        border_color = self.colors["border_active"] if self.active else self.colors["border"]
        
        # 背景
        bg_rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(surface, self.colors["background"], bg_rect, border_radius=8)
        pygame.draw.rect(surface, border_color, bg_rect, width=2, border_radius=8)
        
        # 文本或占位符
        text_x = x + 15
        text_y = y + (self.height - self.font.get_linesize()) // 2
        
        if self.text:
            # 显示输入的文本
            text_surface = self.font.render(self.text, True, self.colors["text"])
            surface.blit(text_surface, (text_x, text_y))
            
            # 绘制光标
            if self.active and self.cursor_visible:
                cursor_x = text_x + self.font.size(self.text)[0] + 2
                pygame.draw.line(
                    surface,
                    self.colors["cursor"],
                    (cursor_x, text_y),
                    (cursor_x, text_y + self.font.get_linesize()),
                    width=2
                )
        else:
            # 显示占位符
            if self.active:
                # 活动状态显示光标
                if self.cursor_visible:
                    pygame.draw.line(
                        surface,
                        self.colors["cursor"],
                        (text_x, text_y),
                        (text_x, text_y + self.font.get_linesize()),
                        width=2
                    )
            else:
                # 非活动状态显示占位符
                placeholder_surface = self.font.render(
                    self.placeholder, 
                    True, 
                    self.colors["placeholder"]
                )
                surface.blit(placeholder_surface, (text_x, text_y))
    
    def _submit(self) -> None:
        """提交输入"""
        if self.on_submit and self.text.strip():
            self.on_submit(self.text.strip())
        self.hide()
    
    def _cancel(self) -> None:
        """取消输入"""
        if self.on_cancel:
            self.on_cancel()
        self.hide()
    
    def get_text(self) -> str:
        """获取当前输入文本"""
        return self.text.strip()
