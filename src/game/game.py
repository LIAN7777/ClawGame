"""
ClawGame 游戏核心模块
"""

import pygame
from typing import Optional


class Game:
    """游戏主类"""
    
    def __init__(self, screen: pygame.Surface):
        """
        初始化游戏
        
        Args:
            screen: pygame 显示表面
        """
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # 游戏状态
        self.running = True
        self.paused = False
        
        # 颜色定义
        self.colors = {
            "background": (135, 206, 235),  # 天蓝色
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "green": (34, 139, 34),
        }
        
        # 初始化字体
        self.font = pygame.font.Font(None, 36)
        
        # TODO: 初始化游戏对象
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        处理事件
        
        Args:
            event: pygame 事件
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
            elif event.key == pygame.K_q:
                self.running = False
    
    def update(self) -> None:
        """更新游戏状态"""
        if self.paused:
            return
            
        # TODO: 更新游戏逻辑
        pass
    
    def render(self) -> None:
        """渲染游戏画面"""
        # 清屏
        self.screen.fill(self.colors["background"])
        
        # TODO: 渲染游戏对象
        
        # 渲染暂停提示
        if self.paused:
            self._render_pause_overlay()
        
        # 渲染调试信息
        self._render_debug_info()
    
    def _render_pause_overlay(self) -> None:
        """渲染暂停覆盖层"""
        # 半透明遮罩
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(self.colors["black"])
        self.screen.blit(overlay, (0, 0))
        
        # 暂停文字
        text = self.font.render("PAUSED - Press ESC to continue", True, self.colors["white"])
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)
    
    def _render_debug_info(self) -> None:
        """渲染调试信息"""
        fps_text = self.font.render(f"FPS: {int(pygame.time.Clock().get_fps())}", True, self.colors["black"])
        self.screen.blit(fps_text, (10, 10))
