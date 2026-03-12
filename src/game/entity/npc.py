"""
ClawGame - NPC 类模块
非玩家角色类，继承自 Entity
"""

from enum import Enum
from typing import TYPE_CHECKING, Optional, Tuple

import math
import pygame

from game.entity.entity import Entity

if TYPE_CHECKING:
    from game.camera import Camera


class NPCState(Enum):
    """NPC 状态枚举"""
    IDLE = 0      # 闲置
    TALKING = 1   # 对话中


class NPC(Entity):
    """
    NPC 类
    
    卡通小动物角色（与玩家风格一致，不同颜色）。
    支持闲置呼吸动画和交互反馈。
    """
    
    # 动画参数
    IDLE_FLOAT_AMPLITUDE: float = 1.5   # 闲置浮动幅度（比玩家小）
    IDLE_FLOAT_SPEED: float = 3.0       # 闲置浮动速度
    
    # 精灵尺寸
    SPRITE_SIZE: int = 24  # 与玩家相同
    
    # NPC 颜色配置（不同颜色方案）
    COLOR_SCHEMES = {
        'pink': {
            'body': (255, 182, 193),        # 粉色身体（与玩家相同）
            'ear': (255, 150, 170),         # 深粉色耳朵
            'eye': (40, 40, 40),            # 深灰色眼睛
            'eye_highlight': (255, 255, 255),
            'cheek': (255, 130, 150),       # 腮红
        },
        'green': {
            'body': (144, 238, 144),        # 浅绿色身体
            'ear': (60, 179, 113),          # 中绿色耳朵
            'eye': (40, 40, 40),
            'eye_highlight': (255, 255, 255),
            'cheek': (152, 251, 152),       # 浅绿腮红
        },
        'blue': {
            'body': (173, 216, 230),        # 浅蓝色身体
            'ear': (70, 130, 180),          # 钢蓝色耳朵
            'eye': (40, 40, 40),
            'eye_highlight': (255, 255, 255),
            'cheek': (135, 206, 250),       # 浅蓝腮红
        },
        'yellow': {
            'body': (255, 255, 224),        # 浅黄色身体
            'ear': (240, 230, 140),         # 卡其色耳朵
            'eye': (40, 40, 40),
            'eye_highlight': (255, 255, 255),
            'cheek': (255, 228, 181),       # 木瓜鞭腮红
        },
    }
    
    # 对话气泡配置
    BUBBLE_DURATION: float = 2.0  # 气泡显示时长（秒）
    
    def __init__(
        self, 
        x: float, 
        y: float, 
        color_scheme: str = 'pink',
        name: str = "NPC"
    ):
        """
        初始化 NPC
        
        Args:
            x: 世界 X 坐标（像素）
            y: 世界 Y 坐标（像素）
            color_scheme: 颜色方案名称
            name: NPC 名称
        """
        # 调用父类初始化
        super().__init__(x, y, self.SPRITE_SIZE, self.SPRITE_SIZE)
        
        # NPC 基本信息
        self.name = name
        self.color_scheme = color_scheme
        
        # 获取颜色配置
        colors = self.COLOR_SCHEMES.get(color_scheme, self.COLOR_SCHEMES['pink'])
        self.body_color = colors['body']
        self.ear_color = colors['ear']
        self.eye_color = colors['eye']
        self.eye_highlight = colors['eye_highlight']
        self.cheek_color = colors['cheek']
        
        # 状态
        self.state = NPCState.IDLE
        
        # 动画时间
        self.anim_time: float = 0.0
        
        # 对话气泡
        self.show_bubble: bool = False
        self.bubble_text: str = ""
        self.bubble_timer: float = 0.0
        
        # 调整碰撞盒（比精灵稍小）
        self.hitbox_offset_x = 4
        self.hitbox_offset_y = 6
        self.hitbox_width = self.SPRITE_SIZE - 8
        self.hitbox_height = self.SPRITE_SIZE - 10
    
    def show_dialog(self, text: str = "你好！") -> None:
        """
        显示对话气泡
        
        Args:
            text: 对话文本
        """
        self.show_bubble = True
        self.bubble_text = text
        self.bubble_timer = self.BUBBLE_DURATION
        self.state = NPCState.TALKING
    
    def hide_dialog(self) -> None:
        """隐藏对话气泡"""
        self.show_bubble = False
        self.bubble_text = ""
        self.bubble_timer = 0.0
        self.state = NPCState.IDLE
    
    def interact(self) -> str:
        """
        被交互时调用
        
        Returns:
            对话文本
        """
        import random
        greetings = ["你好！", "Hi!", "欢迎！", "嘿！"]
        text = random.choice(greetings)
        self.show_dialog(text)
        return text
    
    def update(self, dt: float) -> None:
        """
        更新 NPC 状态
        
        Args:
            dt: 时间增量（秒）
        """
        if not self.active:
            return
        
        # 更新动画时间
        self.anim_time += dt
        
        # 更新对话气泡计时器
        if self.show_bubble:
            self.bubble_timer -= dt
            if self.bubble_timer <= 0:
                self.hide_dialog()
    
    def render(
        self, 
        surface: pygame.Surface, 
        camera: Optional['Camera'] = None
    ) -> None:
        """
        渲染 NPC 精灵
        
        Args:
            surface: 目标渲染表面
            camera: 相机对象
        """
        if not self.visible:
            return
        
        # 获取屏幕坐标
        screen_x, screen_y = self._get_screen_position(camera)
        
        # 绘制影子
        self._draw_shadow(surface, screen_x, screen_y)
        
        # 计算闲置浮动偏移
        offset_y = math.sin(self.anim_time * self.IDLE_FLOAT_SPEED * 2 * math.pi) * self.IDLE_FLOAT_AMPLITUDE
        
        # 绘制 NPC 精灵
        self._draw_sprite(surface, screen_x, int(screen_y + offset_y))
        
        # 绘制对话气泡
        if self.show_bubble:
            self._draw_bubble(surface, screen_x, int(screen_y + offset_y), camera)
    
    def _draw_sprite(
        self, 
        surface: pygame.Surface, 
        x: int, 
        y: int
    ) -> None:
        """
        绘制 NPC 精灵
        
        与玩家风格一致的卡通小动物形象。
        
        Args:
            surface: 目标渲染表面
            x: 屏幕 X 坐标
            y: 屏幕 Y 坐标
        """
        center_x = x + self.SPRITE_SIZE // 2
        center_y = y + self.SPRITE_SIZE // 2
        
        # === 绘制身体（椭圆）===
        body_width = 20
        body_height = 18
        body_rect = pygame.Rect(
            center_x - body_width // 2,
            center_y - body_height // 2,
            body_width,
            body_height
        )
        pygame.draw.ellipse(surface, self.body_color, body_rect)
        
        # === 绘制耳朵 ===
        ear_width = 5
        ear_height = 6
        ear_y = center_y - body_height // 2 - ear_height // 2
        
        # 左耳
        pygame.draw.ellipse(
            surface, 
            self.ear_color,
            pygame.Rect(center_x - body_width // 3, ear_y, ear_width, ear_height)
        )
        # 右耳
        pygame.draw.ellipse(
            surface, 
            self.ear_color,
            pygame.Rect(center_x + body_width // 6, ear_y, ear_width, ear_height)
        )
        
        # === 绘制眼睛（看向玩家，默认向下）===
        eye_y = center_y - 2
        eye_spacing = 6
        
        self._draw_eye(surface, center_x - 3, eye_y)
        self._draw_eye(surface, center_x + 3, eye_y)
        
        # === 绘制腮红 ===
        cheek_y = center_y + 4
        pygame.draw.circle(
            surface, 
            self.cheek_color,
            (center_x - body_width // 3, cheek_y),
            2
        )
        pygame.draw.circle(
            surface, 
            self.cheek_color,
            (center_x + body_width // 3, cheek_y),
            2
        )
    
    def _draw_shadow(
        self, 
        surface: pygame.Surface, 
        x: int, 
        y: int
    ) -> None:
        """
        绘制 NPC 影子
        
        Args:
            surface: 目标渲染表面
            x: 屏幕 X 坐标
            y: 屏幕 Y 坐标
        """
        shadow_width = self.SPRITE_SIZE - 4
        shadow_height = 6
        
        # 创建影子表面
        shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
        shadow_color = (50, 50, 50, 80)
        pygame.draw.ellipse(shadow_surface, shadow_color, (0, 0, shadow_width, shadow_height))
        
        # 绘制影子
        shadow_x = x + (self.SPRITE_SIZE - shadow_width) // 2
        shadow_y = y + self.SPRITE_SIZE - 4
        surface.blit(shadow_surface, (shadow_x, shadow_y))
    
    def _draw_eye(
        self, 
        surface: pygame.Surface, 
        x: int, 
        y: int
    ) -> None:
        """
        绘制单只眼睛
        
        Args:
            surface: 目标渲染表面
            x: 眼睛 X 坐标
            y: 眼睛 Y 坐标
        """
        # 眼白
        pygame.draw.circle(surface, self.eye_highlight, (x, y), 2)
        
        # 眼珠（居中）
        pygame.draw.circle(surface, self.eye_color, (x, y), 1)
    
    def _draw_bubble(
        self, 
        surface: pygame.Surface, 
        x: int, 
        y: int,
        camera: Optional['Camera'] = None
    ) -> None:
        """
        绘制对话气泡
        
        Args:
            surface: 目标渲染表面
            x: NPC 屏幕 X 坐标
            y: NPC 屏幕 Y 坐标
            camera: 相机对象
        """
        # 气泡位置（NPC 头顶）
        bubble_x = x + self.SPRITE_SIZE // 2
        bubble_y = y - 20
        
        # 气泡文本
        font = pygame.font.Font(None, 20)
        text_surface = font.render(self.bubble_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        
        # 气泡尺寸（留出内边距）
        padding = 8
        bubble_width = text_rect.width + padding * 2
        bubble_height = text_rect.height + padding * 2
        
        # 气泡矩形
        bubble_rect = pygame.Rect(
            bubble_x - bubble_width // 2,
            bubble_y - bubble_height,
            bubble_width,
            bubble_height
        )
        
        # 绘制气泡背景（白色圆角矩形）
        pygame.draw.rect(
            surface, 
            (255, 255, 255), 
            bubble_rect, 
            border_radius=6
        )
        
        # 绘制气泡边框
        pygame.draw.rect(
            surface, 
            (100, 100, 100), 
            bubble_rect, 
            width=1, 
            border_radius=6
        )
        
        # 绘制小三角（指向 NPC）
        triangle_points = [
            (bubble_x - 4, bubble_y),
            (bubble_x + 4, bubble_y),
            (bubble_x, bubble_y + 6)
        ]
        pygame.draw.polygon(surface, (255, 255, 255), triangle_points)
        
        # 绘制文本
        text_pos = (
            bubble_rect.centerx - text_rect.width // 2,
            bubble_rect.centery - text_rect.height // 2
        )
        surface.blit(text_surface, text_pos)
    
    def __repr__(self) -> str:
        """字符串表示"""
        return f"NPC(name={self.name}, x={self.x:.1f}, y={self.y:.1f}, color={self.color_scheme})"
