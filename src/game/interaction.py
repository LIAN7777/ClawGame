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
        camera: Optional['Camera'] = None
    ) -> None:
        """
        渲染交互提示
        
        在可交互 NPC 头顶显示 "Press E to talk"。
        
        Args:
            surface: 目标渲染表面
            camera: 相机对象
        """
        if not self.show_prompt or self.nearby_npc is None:
            return
        
        npc = self.nearby_npc
        
        # 计算 NPC 屏幕位置
        if camera:
            screen_x = int(npc.x - camera.x)
            screen_y = int(npc.y - camera.y)
        else:
            screen_x = int(npc.x)
            screen_y = int(npc.y)
        
        # 提示框位置（NPC 头顶）
        prompt_x = screen_x + npc.width // 2
        prompt_y = screen_y - 35
        
        # 使用支持中文的字体
        font = _get_font(self.PROMPT_FONT_SIZE)
        text_surface = font.render(self.INTERACTION_PROMPT, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        
        # 提示框尺寸
        padding = 6
        box_width = text_rect.width + padding * 2
        box_height = text_rect.height + padding * 2
        
        # 提示框矩形
        box_rect = pygame.Rect(
            prompt_x - box_width // 2,
            prompt_y - box_height,
            box_width,
            box_height
        )
        
        # 绘制提示框背景（浅黄色，更醒目）
        pygame.draw.rect(
            surface, 
            (255, 255, 200), 
            box_rect, 
            border_radius=4
        )
        
        # 绘制提示框边框
        pygame.draw.rect(
            surface, 
            (180, 180, 100), 
            box_rect, 
            width=1, 
            border_radius=4
        )
        
        # 绘制文本
        text_pos = (
            box_rect.centerx - text_rect.width // 2,
            box_rect.centery - text_rect.height // 2
        )
        surface.blit(text_surface, text_pos)
    
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
