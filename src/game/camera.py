"""
ClawGame - 相机系统模块
负责视口管理和坐标转换
"""

from typing import Optional, Tuple

import pygame


class Camera:
    """
    相机类 - 管理游戏视口
    
    负责将世界坐标转换为屏幕坐标，支持跟随目标移动和边界限制。
    """
    
    def __init__(
        self, 
        width: int, 
        height: int,
        world_width: Optional[int] = None,
        world_height: Optional[int] = None
    ):
        """
        初始化相机
        
        Args:
            width: 视口宽度（像素）
            height: 视口高度（像素）
            world_width: 世界宽度（像素），用于边界限制，None 表示无限制
            world_height: 世界高度（像素），用于边界限制，None 表示无限制
        """
        # 视口尺寸
        self.width = width
        self.height = height
        
        # 世界边界
        self.world_width = world_width
        self.world_height = world_height
        
        # 相机位置（左上角的世界坐标）
        self.x = 0
        self.y = 0
        
        # 跟随目标
        self._target: Optional[pygame.Rect] = None
        
        # 平滑跟随参数
        self.smooth: bool = False
        self.smooth_speed: float = 0.1  # 平滑系数 (0-1)
    
    @property
    def rect(self) -> pygame.Rect:
        """获取相机在世界的矩形区域"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    @property
    def center(self) -> Tuple[float, float]:
        """获取相机中心点的世界坐标"""
        return (self.x + self.width / 2, self.y + self.height / 2)
    
    def follow(self, target: pygame.Rect, smooth: bool = False) -> None:
        """
        设置跟随目标
        
        Args:
            target: 跟随目标的矩形区域（世界坐标）
            smooth: 是否启用平滑跟随
        """
        self._target = target
        self.smooth = smooth
    
    def unfollow(self) -> None:
        """取消跟随目标"""
        self._target = None
    
    def update(self) -> None:
        """
        更新相机位置
        
        如果设置了跟随目标，则移动相机以保持目标在视口中心。
        应用边界限制，确保相机不会超出世界边界。
        """
        if self._target is None:
            return
        
        # 计算目标中心点
        target_center_x = self._target.centerx
        target_center_y = self._target.centery
        
        # 计算相机理想位置（使目标居中）
        ideal_x = target_center_x - self.width / 2
        ideal_y = target_center_y - self.height / 2
        
        if self.smooth:
            # 平滑插值
            self.x += (ideal_x - self.x) * self.smooth_speed
            self.y += (ideal_y - self.y) * self.smooth_speed
        else:
            # 直接跟随
            self.x = ideal_x
            self.y = ideal_y
        
        # 应用边界限制
        self._apply_bounds()
    
    def _apply_bounds(self) -> None:
        """应用边界限制，确保相机不超出世界边界"""
        # 左边界
        if self.x < 0:
            self.x = 0
        
        # 上边界
        if self.y < 0:
            self.y = 0
        
        # 右边界（如果定义了世界宽度）
        if self.world_width is not None:
            max_x = self.world_width - self.width
            if self.x > max_x:
                self.x = max_x
        
        # 下边界（如果定义了世界高度）
        if self.world_height is not None:
            max_y = self.world_height - self.height
            if self.y > max_y:
                self.y = max_y
    
    def apply(self, entity: pygame.Rect) -> pygame.Rect:
        """
        将实体的世界坐标转换为屏幕坐标
        
        Args:
            entity: 实体的矩形区域（世界坐标）
            
        Returns:
            转换后的屏幕坐标矩形
        """
        return pygame.Rect(
            entity.x - self.x,
            entity.y - self.y,
            entity.width,
            entity.height
        )
    
    def apply_point(self, point: Tuple[float, float]) -> Tuple[float, float]:
        """
        将世界坐标点转换为屏幕坐标
        
        Args:
            point: 世界坐标点 (x, y)
            
        Returns:
            屏幕坐标点 (x, y)
        """
        return (point[0] - self.x, point[1] - self.y)
    
    def screen_to_world(self, point: Tuple[float, float]) -> Tuple[float, float]:
        """
        将屏幕坐标转换为世界坐标
        
        Args:
            point: 屏幕坐标点 (x, y)
            
        Returns:
            世界坐标点 (x, y)
        """
        return (point[0] + self.x, point[1] + self.y)
    
    def is_visible(self, rect: pygame.Rect) -> bool:
        """
        检查实体是否在视口内（用于渲染优化）
        
        Args:
            rect: 实体的世界坐标矩形
            
        Returns:
            是否可见
        """
        return self.rect.colliderect(rect)
    
    def move(self, dx: float, dy: float) -> None:
        """
        手动移动相机
        
        Args:
            dx: X 轴移动量（像素）
            dy: Y 轴移动量（像素）
        """
        self.x += dx
        self.y += dy
        self._apply_bounds()
    
    def set_position(self, x: float, y: float) -> None:
        """
        设置相机位置
        
        Args:
            x: X 坐标（世界坐标）
            y: Y 坐标（世界坐标）
        """
        self.x = x
        self.y = y
        self._apply_bounds()
    
    def set_center(self, x: float, y: float) -> None:
        """
        设置相机中心位置
        
        Args:
            x: 中心 X 坐标（世界坐标）
            y: 中心 Y 坐标（世界坐标）
        """
        self.x = x - self.width / 2
        self.y = y - self.height / 2
        self._apply_bounds()
