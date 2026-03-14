"""
ClawGame 游戏核心模块
"""

from typing import Optional

import pygame

from config import config
from game.camera import Camera
from game.entity.player import Player
from game.interaction import InteractionSystem
from game.scene import Scene
from game.custom_room_scene import CustomRoomScene
from game.ui.text_input import TextInput
from utils.asset_loader import AssetLoader


class Game:
    """游戏主类"""
    
    def __init__(
        self, 
        screen: pygame.Surface, 
        asset_loader: Optional[AssetLoader] = None,
        use_custom_room: bool = True
    ):
        """
        初始化游戏
        
        Args:
            screen: pygame 显示表面
            asset_loader: 资源管理器实例（可选）
            use_custom_room: 是否使用自定义房间场景（默认True）
        """
        self.screen = screen
        self.asset_loader = asset_loader
        self.use_custom_room = use_custom_room
        
        # 使用配置中的内部渲染尺寸（用于相机和渲染逻辑）
        self.width = config.internal_width
        self.height = config.internal_height
        
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
        
        # 帧率追踪（使用外部传入的 delta time）
        self._last_dt: float = 0.0
        
        # 初始化场景
        if use_custom_room:
            print("[Game] 使用自定义房间场景")
            self.scene = CustomRoomScene()
        else:
            print("[Game] 使用默认TileMap场景")
            self.scene = Scene()
        
        # 初始化玩家
        spawn_x, spawn_y = self.scene.get_spawn_position()
        self.player = Player(spawn_x, spawn_y)
        self.player.set_scene(self.scene)
        self.scene.add_entity(self.player)
        
        # 初始化相机
        scene_width, scene_height = self.scene.get_pixel_size()
        print(f"[Game] 场景尺寸: {scene_width}x{scene_height}px")
        self.camera = Camera(
            width=self.width,
            height=self.height,
            world_width=scene_width,
            world_height=scene_height
        )
        
        # 让相机跟随玩家（不用平滑，立即定位）
        self.camera.follow(self.player.rect, smooth=False)
        self.camera.update()  # 立即更新相机位置到玩家
        
        # 初始化交互系统
        self.interaction_system = InteractionSystem()
        
        # 初始化文本输入框
        self.text_input = TextInput(
            width=350,
            height=45,
            font_size=18,
            placeholder="输入对话内容，回车发送..."
        )
        self.text_input.on_submit = self._on_text_submit
        self.text_input.on_cancel = self._on_text_cancel
        
        # 输入模式状态
        self.input_mode: bool = False
        
        # 默认禁用文本输入模式（避免输入法干扰游戏操作）
        pygame.key.stop_text_input()
        
    def _on_text_submit(self, text: str) -> None:
        """
        文本输入提交回调
        
        Args:
            text: 玩家输入的文本
        """
        self.input_mode = False
        
        # 获取当前可交互的 NPC
        npc = self.interaction_system.nearby_npc
        if npc and npc.use_llm:
            # 发送给 NPC
            npc.interact(text)
    
    def _on_text_cancel(self) -> None:
        """文本输入取消回调"""
        self.input_mode = False
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        处理事件
        
        Args:
            event: pygame 事件
        """
        # 输入模式优先处理
        if self.input_mode:
            handled = self.text_input.handle_event(event)
            if handled:
                return
        
        # 处理输入法事件（只在输入模式下）
        if event.type == pygame.TEXTINPUT:
            # 已经由 text_input.handle_event 处理了
            return
        
        if event.type == pygame.TEXTEDITING:
            # 输入法组合中，只在输入模式下有意义
            # 非输入模式下忽略此事件，让 KEYDOWN 正常处理
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.input_mode:
                    # 输入模式下 ESC 取消输入
                    self.text_input.hide()
                    self.input_mode = False
                else:
                    # 非输入模式下切换暂停
                    self.paused = not self.paused
            elif event.key == pygame.K_q:
                self.running = False
            elif event.key == pygame.K_e:
                # E 键：简单打招呼
                if not self.input_mode:
                    self.interaction_system.handle_key(event.key)
            elif event.key == pygame.K_SPACE:
                # 空格键：打开输入框进行自由对话（仅限有 LLM 的 NPC）
                if not self.input_mode:
                    npc = self.interaction_system.nearby_npc
                    if npc is not None and getattr(npc, 'use_llm', False):
                        self.input_mode = True
                        self.text_input.show()
    
    def update(self, dt: float = 0.0) -> None:
        """
        更新游戏状态
        
        Args:
            dt: 时间增量（秒），默认为0
        """
        if self.paused:
            return
        
        # 保存 delta time
        self._last_dt = dt
        
        # 更新输入框（光标闪烁等）
        if self.input_mode:
            self.text_input.update(dt)
            # 输入模式下不处理玩家移动，但继续更新场景
            self.scene.update(dt)
            self.camera.follow(self.player.rect, smooth=True)
            self.camera.update()
            return
        
        # 处理玩家输入
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        # 更新场景（包括玩家和 NPC）
        self.scene.update(dt)
        
        # 更新交互系统
        self.interaction_system.update(self.player, self.scene.npcs)
        self.interaction_system.update_cooldown(dt)
        
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
        
        # 渲染交互提示（传入玩家对象用于显示 E 和空格按钮）
        self.interaction_system.render_prompt(target, self.camera, self.player)
        
        # 渲染文本输入框
        if self.input_mode:
            self.text_input.render(target)
        
        # 渲染暂停提示
        if self.paused:
            self._render_pause_overlay(target, width, height)
    
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
        # 计算 FPS（基于 delta time）
        fps = int(1.0 / self._last_dt) if self._last_dt > 0 else 0
        fps_text = self.font.render(f"FPS: {fps}", True, self.colors["white"])
        surface.blit(fps_text, (10, 10))
        
        # 显示玩家信息
        player_info = f"Player: ({self.player.x:.0f}, {self.player.y:.0f}) {self.player.get_direction_text()} {self.player.get_speed_text()}"
        player_text = self.font.render(player_info, True, self.colors["white"])
        surface.blit(player_text, (10, 40))
