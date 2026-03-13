"""
ClawGame - 场景管理模块
管理游戏场景，包含地图和实体
"""

from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

import pygame

from game.tilemap import TileMap
from game.entity.npc import NPC

if TYPE_CHECKING:
    from game.camera import Camera


# 木屋室内 Tile 类型定义
class TileType:
    """Tile 类型常量"""
    FLOOR = 10       # 木地板
    WALL = 11        # 墙壁
    WINDOW = 12      # 窗户
    DOOR = 13        # 门
    TABLE = 14       # 桌子
    CHAIR = 15       # 椅子
    BED = 16         # 床
    RUG = 17         # 地毯


# 木屋室内颜色配置
CABIN_COLORS: Dict[int, Tuple[int, int, int]] = {
    TileType.FLOOR: (139, 90, 43),      # 棕色木地板
    TileType.WALL: (101, 67, 33),       # 深棕色墙壁
    TileType.WINDOW: (255, 223, 186),   # 暖黄色窗户
    TileType.DOOR: (139, 69, 19),       # 深棕色门
    TileType.TABLE: (160, 82, 45),      # 赭色桌子
    TileType.CHAIR: (139, 69, 19),      # 深棕色椅子
    TileType.BED: (178, 34, 34),        # 红木床架
    TileType.RUG: (85, 107, 47),        # 橄榄绿地毯
}


# 木屋室内地图数据 (15x12 tiles)
# 10=地板, 11=墙壁, 12=窗户, 13=门, 14=桌子, 15=椅子, 16=床, 17=地毯
CABIN_INDOOR_MAP: List[List[int]] = [
    # y=0  (顶部墙壁)
    [11, 11, 12, 11, 11, 11, 11, 11, 11, 11, 12, 11, 11, 11, 11],
    # y=1
    [11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11],
    # y=2
    [11, 10, 17, 17, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11],
    # y=3
    [11, 10, 17, 17, 10, 10, 10, 14, 14, 10, 10, 10, 10, 10, 11],
    # y=4
    [11, 10, 10, 10, 10, 10, 15, 10, 10, 15, 10, 10, 10, 10, 11],
    # y=5
    [11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11],
    # y=6
    [11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11],
    # y=7
    [11, 10, 10, 14, 14, 10, 10, 10, 10, 10, 10, 16, 16, 10, 11],
    # y=8
    [11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 16, 16, 10, 11],
    # y=9
    [11, 10, 10, 15, 10, 10, 10, 10, 10, 10, 10, 16, 16, 10, 11],
    # y=10
    [11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11],
    # y=11 (底部墙壁，中间有门)
    [11, 11, 11, 11, 11, 11, 11, 13, 11, 11, 11, 11, 11, 11, 11],
]

# 地图尺寸配置
CABIN_MAP_WIDTH = 15   # 格子宽度
CABIN_MAP_HEIGHT = 12  # 格子高度
CABIN_TILE_SIZE = 32   # 每格 32 像素


class Scene:
    """
    场景管理类
    
    管理游戏场景，包含地图和实体列表。
    负责场景的加载、更新和渲染。
    """
    
    def __init__(self, tile_size: int = CABIN_TILE_SIZE):
        """
        初始化场景
        
        Args:
            tile_size: 单个 tile 的像素尺寸
        """
        self.tile_size = tile_size
        
        # 创建 tile 地图
        self.tilemap = TileMap(tile_size)
        
        # 扩展 TileMap 的颜色配置
        self._setup_colors()
        
        # 实体列表（玩家和 NPC 等）
        self.entities: List = []
        
        # NPC 列表（便于单独访问）
        self.npcs: List[NPC] = []
        
        # 场景名称
        self.name = "木屋室内"
        
        # 加载默认场景
        self.load_cabin_scene()
        
        # 初始化测试 NPC
        self._init_test_npcs()
    
    def _setup_colors(self) -> None:
        """设置 Tile 颜色配置"""
        # 合并木屋室内颜色到 TileMap
        for tile_type, color in CABIN_COLORS.items():
            self.tilemap.TILE_COLORS[tile_type] = color
    
    def load_cabin_scene(self) -> None:
        """加载木屋室内场景"""
        self.tilemap.load_from_array(CABIN_INDOOR_MAP)
        self.name = "木屋室内"
    
    def load_from_array(self, data: List[List[int]], name: str = "自定义场景") -> None:
        """
        从数组加载场景
        
        Args:
            data: 2D 数组地图数据
            name: 场景名称
        """
        self.tilemap.load_from_array(data)
        self.name = name
    
    def add_entity(self, entity) -> None:
        """
        添加实体到场景
        
        Args:
            entity: 实体对象
        """
        self.entities.append(entity)
    
    def remove_entity(self, entity) -> None:
        """
        从场景移除实体
        
        Args:
            entity: 实体对象
        """
        if entity in self.entities:
            self.entities.remove(entity)
    
    def update(self, dt: float) -> None:
        """
        更新场景
        
        Args:
            dt: 时间增量（秒）
        """
        # 更新所有实体
        for entity in self.entities:
            if hasattr(entity, 'update'):
                entity.update(dt)
    
    def render(
        self, 
        surface: pygame.Surface, 
        camera: Optional['Camera'] = None,
        offset: Tuple[int, int] = (0, 0)
    ) -> None:
        """
        渲染场景
        
        Args:
            surface: 目标渲染表面
            camera: 相机对象
            offset: 渲染偏移量
        """
        # 渲染 tile 地图
        self.tilemap.render(surface, camera, offset)
        
        # 渲染实体（按 Y 坐标排序，实现深度效果）
        sorted_entities = sorted(
            self.entities,
            key=lambda e: getattr(e, 'y', 0)
        )
        for entity in sorted_entities:
            if hasattr(entity, 'render'):
                entity.render(surface, camera)
    
    def get_spawn_position(self) -> Tuple[float, float]:
        """
        获取玩家出生位置（门的前方中央区域）
        
        Returns:
            (x, y) 像素坐标
        """
        # 在地图中找到门的位置
        for y, row in enumerate(CABIN_INDOOR_MAP):
            for x, tile_type in enumerate(row):
                if tile_type == TileType.DOOR:
                    # 返回门前方两格的中心位置（避免与墙壁碰撞）
                    return (
                        (x * self.tile_size) + (self.tile_size // 2),
                        ((y - 2) * self.tile_size) + (self.tile_size // 2)
                    )
        
        # 默认返回地图中心
        return (
            (CABIN_MAP_WIDTH * self.tile_size) // 2,
            (CABIN_MAP_HEIGHT * self.tile_size) // 2
        )
    
    def get_walkable_tiles(self) -> List[Tuple[int, int]]:
        """
        获取所有可通行的格子坐标
        
        Returns:
            可通行格子坐标列表
        """
        walkable = []
        for y, row in enumerate(CABIN_INDOOR_MAP):
            for x, tile_type in enumerate(row):
                if tile_type != TileType.WALL:
                    walkable.append((x, y))
        return walkable
    
    def get_pixel_size(self) -> Tuple[int, int]:
        """
        获取场景的像素尺寸
        
        Returns:
            (宽度, 高度) 像素
        """
        return self.tilemap.get_pixel_size()
    
    def get_grid_size(self) -> Tuple[int, int]:
        """
        获取场景的格子尺寸
        
        Returns:
            (宽度, 高度) 格子数
        """
        return self.tilemap.get_grid_size()
    
    def is_position_walkable(self, x: float, y: float) -> bool:
        """
        检查指定像素位置是否可通行
        
        Args:
            x: X 像素坐标
            y: Y 像素坐标
            
        Returns:
            是否可通行
        """
        grid_x = int(x // self.tile_size)
        grid_y = int(y // self.tile_size)
        
        tile = self.tilemap.get_tile(grid_x, grid_y)
        if tile is None:
            return False
        
        # 墙壁和家具不可通行
        return tile.tile_type not in (
            TileType.WALL,
            TileType.TABLE,
            TileType.BED,
        )
    
    def add_npc(self, npc: NPC) -> None:
        """
        添加 NPC 到场景
        
        Args:
            npc: NPC 对象
        """
        self.npcs.append(npc)
        self.entities.append(npc)
    
    def remove_npc(self, npc: NPC) -> None:
        """
        从场景移除 NPC
        
        Args:
            npc: NPC 对象
        """
        if npc in self.npcs:
            self.npcs.remove(npc)
        if npc in self.entities:
            self.entities.remove(npc)
    
    def _init_test_npcs(self) -> None:
        """
        初始化测试 NPC
        
        在场景中放置 3 个不同颜色的 NPC。
        """
        # NPC 位置（避开墙壁和家具，选择空旷位置）
        # 格式: (grid_x, grid_y, color_scheme, name)
        npc_configs = [
            (3, 6, 'green', '小绿'),    # 左侧区域
            (7, 3, 'blue', '小蓝'),      # 上方区域（桌子旁边）
            (11, 5, 'yellow', '小黄'),   # 右侧区域（床边）
        ]
        
        for grid_x, grid_y, color, name in npc_configs:
            # 转换为像素坐标（格子中心）
            x = grid_x * self.tile_size + self.tile_size // 2 - 12  # 减去精灵宽度的一半
            y = grid_y * self.tile_size + self.tile_size // 2 - 12  # 减去精灵高度的一半
            
            # 创建 NPC
            npc = NPC(x, y, color, name)
            self.add_npc(npc)
