"""
ClawGame 游戏核心模块
"""

from typing import Optional

import pygame

from game.camera import Camera
from game.entity.player import Player
from game.interaction import InteractionSystem
from game.scene import Scene
from utils.asset_loader import AssetLoader


class Game:
    """游戏主类"""
    
    def __init__(
        self, 
        screen: pygame.Surface, 
        asset_loader: Optional[AssetLoader] = None
    ):
        """
        初始化游戏
        
        Args:
            screen: pygame 显示表面
            asset_loader: 资源管理器实例（可选）
        """
        self.screen = screen
        self.asset_loader = asset_loader
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # 游戏状态
        self.running = True
        self.paused = False
        
        # 颜色定义 - 温馨暖色调
        self.colors = {
            "background": (45, 35, 25),      # 深棕色背景
            "ambient": (255, 200, 150),      # 暖色环境光
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "green": (34, 139, 34),
        }
        
        # 初始化字体
        self.font = pygame.font.Font(None, 36)
        
        # 帧率追踪
        self._clock = pygame.time.Clock()
        
        # 初始化场景
        self.scene = Scene()
        
        # 初始化玩家
        spawn_x, spawn_y = self.scene.get_spawn_position()
        self.player = Player(spawn_x, spawn_y)
        self.player.set_scene(self.scene)
        self.scene.add_entity(self.player)
        
        # 初始化相机
        scene_width, scene_height = self.scene.get_pixel_size()
        self.camera = Camera(
            width=self.width,
            height=self.height,
            world_width=scene_width,
            world_height=scene_height
        )
        
        # 让相机跟随玩家
        self.camera.follow(self.player.rect, smooth=True)
        
        # 初始化交互系统
        self.interaction_system = InteractionSystem()
        
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
            elif event.key == pygame.K_e:
                # 尝试交互
                self.interaction_system.handle_key(event.key)
    
    def update(self) -> None:
        """更新游戏状态"""
        if self.paused:
            return
        
        # 处理玩家输入
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        # 更新场景（包括玩家和 NPC）
        dt = self._clock.get_time() / 1000.0  # 转换为秒
        self.scene.update(dt)
        
        # 更新交互系统
        self.interaction_system.update(self.player, self.scene.npcs)
        
        # 更新相机跟随
        self.camera.follow(self.player.rect, smooth=True)
        self.camera.update()
    
    def render(self, surface: Optional[pygame.Surface] = None) -> None:
        """
        渲染游戏画面
        
        Args:
            surface: 可选的目标渲染表面，默认使用 self.screen
        """
        target = surface if surface is not None else self.screen
        
        # 获取目标表面尺寸
        width = target.get_width()
        height = target.get_height()
        
        # 清屏 - 使用深色背景
        target.fill(self.colors["background"])
        
        # 渲染场景（使用相机）
        self.scene.render(target, self.camera)
        
        # 渲染交互提示
        self.interaction_system.render_prompt(target, self.camera)
        
        # 渲染暂停提示
        if self.paused:
            self._render_pause_overlay(target, width, height)
        
        # 渲染调试信息
        self._render_debug_info(target)
    
    def _render_pause_overlay(
        self, 
        surface: pygame.Surface, 
        width: int, 
        height: int
    ) -> None:
        """渲染暂停覆盖层"""
        # 半透明遮罩
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(128)
        overlay.fill(self.colors["black"])
        surface.blit(overlay, (0, 0))
        
        # 暂停文字
        text = self.font.render("PAUSED - Press ESC to continue", True, self.colors["white"])
        text_rect = text.get_rect(center=(width // 2, height // 2))
        surface.blit(text, text_rect)
    
    def _render_debug_info(self, surface: pygame.Surface) -> None:
        """渲染调试信息"""
        fps_text = self.font.render(f"FPS: {int(self._clock.get_fps())}", True, self.colors["black"])
        surface.blit(fps_text, (10, 10))
        
        # 显示玩家信息
        player_info = f"Player: ({self.player.x:.0f}, {self.player.y:.0f}) {self.player.get_direction_text()} {self.player.get_speed_text()}"
        player_text = self.font.render(player_info, True, self.colors["black"])
        surface.blit(player_text, (10, 40))
