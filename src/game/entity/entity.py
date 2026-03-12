"""
ClawGame - Entity 基类模块
所有游戏实体的基类，包含位置、速度、碰撞盒等基础属性
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Tuple

import pygame

if TYPE_CHECKING:
    from game.camera import Camera
    from game.tilemap import TileMap


class Entity(ABC):
    """
    实体基类
    
    所有游戏实体（玩家、NPC、物品等）的基类。
    包含位置、速度、碰撞盒等基础属性和方法。
    """
    
    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
    ):
        """
        初始化实体
        
        Args:
            x: 世界 X 坐标（像素）
            y: 世界 Y 坐标（像素）
            width: 实体宽度（像素）
            height: 实体高度（像素）
        """
        # 位置（像素坐标）
        self.x: float = x
        self.y: float = y
        
        # 尺寸
        self.width: int = width
        self.height: int = height
        
        # 速度（像素/秒）
        self.vx: float = 0.0
        self.vy: float = 0.0
        
        # 碰撞盒（相对于实体左上角的偏移）
        # 默认碰撞盒与实体尺寸相同
        self.hitbox_offset_x: int = 0
        self.hitbox_offset_y: int = 0
        self.hitbox_width: int = width
        self.hitbox_height: int = height
        
        # 是否激活
        self.active: bool = True
        
        # 是否可见
        self.visible: bool = True
    
    @property
    def rect(self) -> pygame.Rect:
        """
        获取实体的矩形区域
        
        Returns:
            pygame.Rect 实体的矩形区域
        """
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    
    @property
    def hitbox(self) -> pygame.Rect:
        """
        获取实体的碰撞盒
        
        Returns:
            pygame.Rect 实体的碰撞盒
        """
        return pygame.Rect(
            int(self.x + self.hitbox_offset_x),
            int(self.y + self.hitbox_offset_y),
            self.hitbox_width,
            self.hitbox_height
        )
    
    @property
    def center(self) -> Tuple[float, float]:
        """
        获取实体中心坐标
        
        Returns:
            (x, y) 中心坐标
        """
        return (self.x + self.width / 2, self.y + self.height / 2)
    
    @property
    def center_x(self) -> float:
        """获取实体中心 X 坐标"""
        return self.x + self.width / 2
    
    @property
    def center_y(self) -> float:
        """获取实体中心 Y 坐标"""
        return self.y + self.height / 2
    
    def set_position(self, x: float, y: float) -> None:
        """
        设置实体位置
        
        Args:
            x: X 坐标
            y: Y 坐标
        """
        self.x = x
        self.y = y
    
    def set_center(self, x: float, y: float) -> None:
        """
        设置实体中心位置
        
        Args:
            x: 中心 X 坐标
            y: 中心 Y 坐标
        """
        self.x = x - self.width / 2
        self.y = y - self.height / 2
    
    def move(self, dx: float, dy: float) -> None:
        """
        移动实体
        
        Args:
            dx: X 方向移动量
            dy: Y 方向移动量
        """
        self.x += dx
        self.y += dy
    
    def set_velocity(self, vx: float, vy: float) -> None:
        """
        设置速度
        
        Args:
            vx: X 方向速度
            vy: Y 方向速度
        """
        self.vx = vx
        self.vy = vy
    
    def collides_with(self, other: 'Entity') -> bool:
        """
        检测是否与另一个实体碰撞
        
        Args:
            other: 另一个实体
            
        Returns:
            是否碰撞
        """
        return self.hitbox.colliderect(other.hitbox)
    
    def collides_with_rect(self, rect: pygame.Rect) -> bool:
        """
        检测是否与矩形碰撞
        
        Args:
            rect: 矩形区域
            
        Returns:
            是否碰撞
        """
        return self.hitbox.colliderect(rect)
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """
        更新实体状态
        
        Args:
            dt: 时间增量（秒）
        """
        pass
    
    @abstractmethod
    def render(
        self, 
        surface: pygame.Surface, 
        camera: Optional['Camera'] = None
    ) -> None:
        """
        渲染实体
        
        Args:
            surface: 目标渲染表面
            camera: 相机对象（用于坐标转换）
        """
        pass
    
    def _get_screen_position(
        self, 
        camera: Optional['Camera'] = None
    ) -> Tuple[int, int]:
        """
        获取屏幕坐标
        
        Args:
            camera: 相机对象
            
        Returns:
            (x, y) 屏幕坐标
        """
        if camera:
            return (
                int(self.x - camera.x),
                int(self.y - camera.y)
            )
        return (int(self.x), int(self.y))
    
    def __repr__(self) -> str:
        """字符串表示"""
        return f"{self.__class__.__name__}(x={self.x:.1f}, y={self.y:.1f})"
