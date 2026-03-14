"""
ClawGame - 交互系统模块
管理玩家与 NPC 的交互
"""

import os
from typing import TYPE_CHECKING, List, Optional, Tuple

import pygame

if TYPE_CHECKING:
    from game.entity.player import Player
    from game.entity.npc import NPC
    from game.camera import Camera


def _get_font(size: int) -> pygame.font.Font:
    """
    获取支持中文的字体
    
    优先使用系统字体，兼容 Windows/Linux/macOS
    """
    # 尝试使用 SysFont 查找系统中文字体
    chinese_font_names = [
        'Microsoft YaHei',
        'microsoftyahei',
        'SimHei',
        'simhei',
        'SimSun',
        'simsun',
        'Droid Sans Fallback',
        'droid sans fallback',
        'Noto Sans CJK SC',
        'Noto Sans CJK',
        'noto sans cjk',
        'PingFang SC',
        'PingFang',
    ]
    
    # 首先尝试 SysFont
    for font_name in chinese_font_names:
        try:
            font = pygame.font.SysFont(font_name, size)
            test_surface = font.render('你好', True, (0, 0, 0))
            w, h = test_surface.get_size()
            if w > 15 and h > 5:
                return font
        except Exception:
            continue
    
    # 如果 SysFont 失败，尝试直接加载字体文件
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = pygame.font.Font(font_path, size)
                test_surface = font.render('你好', True, (0, 0, 0))
                w, h = test_surface.get_size()
                if w > 15 and h > 5:
                    return font
            except Exception:
                continue
    
    return pygame.font.Font(None, size)


class InteractionSystem:
    """
    交互系统类
    
    检测玩家与 NPC 的距离，处理交互触发和提示显示。
    """
    
    # 交互参数
    INTERACTION_RANGE: float = 40.0  # 交互范围（像素）
    
    # 提示文本
    INTERACTION_PROMPT = "Press E to talk"
    
    # 字体大小
    PROMPT_FONT_SIZE = 18
    
    def __init__(self):
        """初始化交互系统"""
        # 当前可交互的 NPC
        self.nearby_npc: Optional['NPC'] = None
        
        # 交互提示显示状态
        self.show_prompt: bool = False
        
        # 防止重复触发交互
        self._interact_cooldown: float = 0.0
    
    def update(
        self, 
        player: 'Player', 
        npcs: List['NPC']
    ) -> Optional['NPC']:
        """
        更新交互系统
        
        检测玩家与所有 NPC 的距离，找出最近的可交互 NPC。
        
        Args:
            player: 玩家对象
            npcs: NPC 列表
            
        Returns:
            当前可交互的 NPC，如果没有则返回 None
        """
        self.nearby_npc = None
        self.show_prompt = False
        
        if not player.active:
            return None
        
        # 获取玩家中心位置
        player_center = player.center
        
        # 遍历所有 NPC，找出最近的
        closest_npc = None
        closest_distance = float('inf')
        
        for npc in npcs:
            if not npc.active:
                continue
            
            # 计算 NPC 中心位置
            npc_center = npc.center
            
            # 计算距离
            distance = self._calculate_distance(player_center, npc_center)
            
            # 如果在交互范围内且更近
            if distance <= self.INTERACTION_RANGE and distance < closest_distance:
                closest_distance = distance
                closest_npc = npc
        
        # 更新状态
        if closest_npc is not None:
            self.nearby_npc = closest_npc
            self.show_prompt = True
        
        return self.nearby_npc
    
    def update_cooldown(self, dt: float) -> None:
        """
        更新交互冷却时间
        
        Args:
            dt: 时间增量（秒）
        """
        if self._interact_cooldown > 0:
            self._interact_cooldown -= dt
    
    def try_interact(self) -> Optional[str]:
        """
        尝试交互
        
        Returns:
            交互结果（对话文本），如果没有可交互的 NPC 则返回 None
        """
        if self.nearby_npc is None:
            return None
        
        # 检查冷却时间
        if self._interact_cooldown > 0:
            return None
        
        # 触发 NPC 交互
        result = self.nearby_npc.interact()
        
        # 设置冷却时间（防止重复触发）
        self._interact_cooldown = 0.5
        
        return result
    
    def handle_key(self, key: int) -> Optional[str]:
        """
        处理按键
        
        Args:
            key: 按键代码
            
        Returns:
            交互结果（如果有）
        """
        if key == pygame.K_e:
            return self.try_interact()
        return None
    
    def render_prompt(
        self, 
        surface: pygame.Surface, 
        camera: Optional['Camera'] = None,
        player: Optional['Player'] = None
    ) -> None:
        """
        渲染交互提示
        
        在玩家上方显示按钮提示（E 和空格）。

        Args:
            surface: 目标渲染表面
            camera: 相机对象
            player: 玩家对象
        """
        if not self.show_prompt or self.nearby_npc is None:
            return
        
        # 获取玩家屏幕位置
        if player is None:
            return
        
        if camera:
            player_screen_x = int(player.x - camera.x)
            player_screen_y = int(player.y - camera.y)
        else:
            player_screen_x = int(player.x)
            player_screen_y = int(player.y)
        
        # 按钮位置（玩家上方居中）
        button_radius = 10  # 圆形半径
        button_spacing = 24  # 按钮间距
        center_x = player_screen_x + player.width // 2
        base_y = player_screen_y - button_radius - 8  # 玩家上方
        
        # 检查是否是有 LLM 的 NPC（如小橘）
        has_llm = getattr(self.nearby_npc, 'use_llm', False)
        
        if has_llm:
            # 显示两个按钮：E 和 空格
            # E 按钮（左侧）
            e_x = center_x - button_spacing // 2
            pygame.draw.circle(surface, (255, 255, 255), (e_x, base_y), button_radius)
            pygame.draw.circle(surface, (100, 100, 100), (e_x, base_y), button_radius, width=2)
            font = pygame.font.Font(None, 16)
            text_surface = font.render("E", True, (50, 50, 50))
            text_rect = text_surface.get_rect(center=(e_x, base_y))
            surface.blit(text_surface, text_rect)
            
            # 空格按钮（右侧）
            space_x = center_x + button_spacing // 2
            pygame.draw.circle(surface, (255, 255, 255), (space_x, base_y), button_radius)
            pygame.draw.circle(surface, (100, 100, 100), (space_x, base_y), button_radius, width=2)
            # 空格用横线表示
            pygame.draw.line(surface, (50, 50, 50), (space_x - 5, base_y), (space_x + 5, base_y), width=2)
        else:
            # 普通 NPC 只显示 E 按钮
            pygame.draw.circle(surface, (255, 255, 255), (center_x, base_y), button_radius)
            pygame.draw.circle(surface, (100, 100, 100), (center_x, base_y), button_radius, width=2)
            font = pygame.font.Font(None, 16)
            text_surface = font.render("E", True, (50, 50, 50))
            text_rect = text_surface.get_rect(center=(center_x, base_y))
            surface.blit(text_surface, text_rect)
    
    def _calculate_distance(
        self, 
        pos1: Tuple[float, float], 
        pos2: Tuple[float, float]
    ) -> float:
        """
        计算两点之间的距离
        
        Args:
            pos1: 第一个点 (x, y)
            pos2: 第二个点 (x, y)
            
        Returns:
            欧几里得距离
        """
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        return (dx * dx + dy * dy) ** 0.5
    
    def get_nearby_npc_name(self) -> Optional[str]:
        """
        获取当前可交互 NPC 的名称
        
        Returns:
            NPC 名称，如果没有则返回 None
        """
        if self.nearby_npc is not None:
            return self.nearby_npc.name
        return None
    
    def __repr__(self) -> str:
        """字符串表示"""
        npc_name = self.nearby_npc.name if self.nearby_npc else "None"
        return f"InteractionSystem(nearby_npc={npc_name}, show_prompt={self.show_prompt})"
