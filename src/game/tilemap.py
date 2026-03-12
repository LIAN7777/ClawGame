"""
ClawGame - Tile 地图模块
管理 tile 地图的加载和渲染
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

import pygame

if TYPE_CHECKING:
    from game.camera import Camera


@dataclass
class Tile:
    """
    Tile 数据类
    
    存储单个 tile 的信息。
    """
    # Tile 在地图中的位置（格子坐标）
    grid_x: int
    grid_y: int
    
    # Tile 类型标识（用于区分不同的 tile）
    tile_type: int
    
    # 是否可通行
    walkable: bool = True
    
    # 自定义属性（用于存储额外数据）
    properties: Optional[Dict] = None
    
    @property
    def position(self) -> Tuple[int, int]:
        """获取格子坐标"""
        return (self.grid_x, self.grid_y)


class TileMap:
    """
    Tile 地图类
    
    管理 tile 地图的加载、存储和渲染。
    支持从 2D 数组加载地图数据。
    """
    
    # 预定义的 Tile 类型颜色（用于渲染占位）
    TILE_COLORS: Dict[int, Tuple[int, int, int]] = {
        0: (34, 139, 34),    # 草地 - 绿色
        1: (139, 90, 43),    # 泥土 - 棕色
        2: (128, 128, 128),  # 石头 - 灰色
        3: (0, 100, 200),    # 水 - 蓝色
        4: (255, 255, 0),    # 沙子 - 黄色
        5: (0, 100, 0),      # 森林 - 深绿色
        -1: (50, 50, 50),    # 空白/未定义 - 深灰色
    }
    
    def __init__(self, tile_size: int = 32):
        """
        初始化 Tile 地图
        
        Args:
            tile_size: 单个 tile 的像素尺寸
        """
        self.tile_size = tile_size
        
        # 地图数据
        self.width: int = 0   # 地图宽度（格子数）
        self.height: int = 0  # 地图高度（格子数）
        self._tiles: Dict[Tuple[int, int], Tile] = {}
        
        # 地图尺寸（像素）
        self.pixel_width: int = 0
        self.pixel_height: int = 0
    
    def load_from_array(self, data: List[List[int]]) -> None:
        """
        从 2D 数组加载地图数据
        
        Args:
            data: 2D 数组，每个元素是 tile 类型 ID
                  data[y][x] 表示第 y 行第 x 列的 tile
        """
        # 清空现有数据
        self._tiles.clear()
        
        # 获取地图尺寸
        self.height = len(data)
        self.width = len(data[0]) if self.height > 0 else 0
        
        # 计算像素尺寸
        self.pixel_width = self.width * self.tile_size
        self.pixel_height = self.height * self.tile_size
        
        # 创建 tile 对象
        for y, row in enumerate(data):
            for x, tile_type in enumerate(row):
                tile = Tile(
                    grid_x=x,
                    grid_y=y,
                    tile_type=tile_type,
                    walkable=self._is_walkable(tile_type)
                )
                self._tiles[(x, y)] = tile
    
    def _is_walkable(self, tile_type: int) -> bool:
        """
        判断 tile 类型是否可通行
        
        Args:
            tile_type: tile 类型 ID
            
        Returns:
            是否可通行
        """
        # 水 (3) 不可通行
        return tile_type != 3
    
    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """
        获取指定位置的 tile
        
        Args:
            x: X 格子坐标
            y: Y 格子坐标
            
        Returns:
            Tile 对象，如果不存在则返回 None
        """
        return self._tiles.get((x, y))
    
    def get_tile_at_pixel(self, pixel_x: float, pixel_y: float) -> Optional[Tile]:
        """
        获取指定像素坐标的 tile
        
        Args:
            pixel_x: X 像素坐标
            pixel_y: Y 像素坐标
            
        Returns:
            Tile 对象，如果不存在则返回 None
        """
        grid_x = int(pixel_x // self.tile_size)
        grid_y = int(pixel_y // self.tile_size)
        return self.get_tile(grid_x, grid_y)
    
    def get_tiles_in_rect(self, rect: pygame.Rect) -> List[Tile]:
        """
        获取矩形区域内的所有 tile
        
        Args:
            rect: 矩形区域（像素坐标）
            
        Returns:
            Tile 列表
        """
        # 计算格子范围
        start_x = max(0, rect.left // self.tile_size)
        start_y = max(0, rect.top // self.tile_size)
        end_x = min(self.width, (rect.right // self.tile_size) + 1)
        end_y = min(self.height, (rect.bottom // self.tile_size) + 1)
        
        tiles = []
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.get_tile(x, y)
                if tile:
                    tiles.append(tile)
        
        return tiles
    
    def render(
        self, 
        surface: pygame.Surface, 
        camera: Optional['Camera'] = None,  # type: ignore
        offset: Tuple[int, int] = (0, 0)
    ) -> None:
        """
        渲染 tile 地图
        
        只渲染相机视口内的 tile，优化性能。
        
        Args:
            surface: 目标渲染表面
            camera: 相机对象（用于视口裁剪）
            offset: 渲染偏移量（像素）
        """
        # 计算渲染范围
        if camera:
            # 根据相机视口计算可见范围
            start_x = max(0, int(camera.x // self.tile_size))
            start_y = max(0, int(camera.y // self.tile_size))
            end_x = min(self.width, int((camera.x + camera.width) // self.tile_size) + 1)
            end_y = min(self.height, int((camera.y + camera.height) // self.tile_size) + 1)
        else:
            # 无相机，渲染全部
            start_x, start_y = 0, 0
            end_x, end_y = self.width, self.height
        
        # 渲染可见 tile
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.get_tile(x, y)
                if tile:
                    self._render_tile(surface, tile, camera, offset)
    
    def _render_tile(
        self, 
        surface: pygame.Surface, 
        tile: Tile, 
        camera: Optional['Camera'],
        offset: Tuple[int, int]
    ) -> None:
        """
        渲染单个 tile
        
        Args:
            surface: 目标渲染表面
            tile: 要渲染的 tile
            camera: 相机对象
            offset: 渲染偏移量
        """
        # 计算屏幕位置
        screen_x = tile.grid_x * self.tile_size + offset[0]
        screen_y = tile.grid_y * self.tile_size + offset[1]
        
        # 应用相机偏移
        if camera:
            screen_x -= camera.x
            screen_y -= camera.y
        
        # 获取颜色
        color = self.TILE_COLORS.get(tile.tile_type, self.TILE_COLORS[-1])
        
        # 绘制矩形
        rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)
        pygame.draw.rect(surface, color, rect)
        
        # 绘制边框（可选，用于调试）
        # pygame.draw.rect(surface, (0, 0, 0), rect, 1)
    
    def set_tile(self, x: int, y: int, tile_type: int) -> None:
        """
        设置指定位置的 tile 类型
        
        Args:
            x: X 格子坐标
            y: Y 格子坐标
            tile_type: 新的 tile 类型
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            tile = Tile(
                grid_x=x,
                grid_y=y,
                tile_type=tile_type,
                walkable=self._is_walkable(tile_type)
            )
            self._tiles[(x, y)] = tile
    
    def get_pixel_size(self) -> Tuple[int, int]:
        """
        获取地图的像素尺寸
        
        Returns:
            (宽度, 高度) 像素
        """
        return (self.pixel_width, self.pixel_height)
    
    def get_grid_size(self) -> Tuple[int, int]:
        """
        获取地图的格子尺寸
        
        Returns:
            (宽度, 高度) 格子数
        """
        return (self.width, self.height)
    
    def is_walkable(self, x: int, y: int) -> bool:
        """
        检查指定位置是否可通行
        
        Args:
            x: X 格子坐标
            y: Y 格子坐标
            
        Returns:
            是否可通行
        """
        tile = self.get_tile(x, y)
        return tile.walkable if tile else False



