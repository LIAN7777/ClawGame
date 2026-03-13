"""
ClawGame - 自定义室内场景模块
使用用户提供的素材渲染房间
"""

import os
from typing import Dict, List, Optional, Tuple

import pygame

from game.tilemap import TileMap
from game.entity.npc import NPC
from config.tiles import get_scaled_size


class FurnitureItem:
    """家具物品"""
    def __init__(self, name: str, image: pygame.Surface, x: int, y: int, collidable: bool = True):
        self.name = name
        self.image = image
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.collidable = collidable
        
        # 碰撞矩形（相对于位置）
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def get_rect(self) -> pygame.Rect:
        """获取碰撞矩形"""
        return self.rect.copy()
    
    def render(self, surface: pygame.Surface, camera_x: int = 0, camera_y: int = 0):
        """渲染家具"""
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        surface.blit(self.image, (screen_x, screen_y))


class CustomRoomScene:
    """
    自定义室内场景
    
    使用单独的图片文件作为素材，实现分层渲染：
    1. 地板层：木地板tile横竖交叠铺满
    2. 家具层：家具渲染在地板之上
    """
    
    # Tile 类型常量（保持与原有代码兼容）
    class TileType:
        FLOOR = 10
        WALL = 11
        DOOR = 13
        TABLE = 14
        CHAIR = 15
        BED = 16
        BOOKSHELF = 18
        CHEST = 20
        FRIDGE = 30  # 冰箱
        TV = 31      # 电视机
    
    def __init__(self, room_width: int = 720, room_height: int = 480):
        """
        初始化自定义房间场景
        
        Args:
            room_width: 房间宽度（像素）
            room_height: 房间高度（像素）
        """
        self.room_width = room_width
        self.room_height = room_height
        
        # 资源根目录
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.custom_assets_dir = os.path.join(self.base_dir, "assets/images/custom")
        
        # 加载素材
        self._load_assets()
        
        # 计算房间布局
        self._setup_room_layout()
        
        # 家具列表
        self.furniture: List[FurnitureItem] = []
        self._place_furniture()
        
        # 实体列表
        self.entities: List = []
        self.npcs: List[NPC] = []
        
        # 场景名称
        self.name = "温馨小屋"
        
        # 初始化测试NPC
        self._init_test_npcs()
    
    def _load_assets(self):
        """加载所有素材"""
        # 加载地板tiles
        self.floor_tile_h = self._load_image("木地板tile_横.png")
        self.floor_tile_v = self._load_image("木地板tile_竖.png")
        
        # 计算地板tile尺寸
        self.floor_tile_width = self.floor_tile_h.get_width()
        self.floor_tile_height = self.floor_tile_h.get_height()
        
        # 加载家具（并缩放到合适尺寸）
        # 门：缩放到约 80x120
        self.door_img = self._load_and_scale("木门.png", 80, 120)
        # 冰箱：缩放到约 60x100
        self.fridge_img = self._load_and_scale("冰箱.png", 60, 100)
        # 椅子：缩放到约 50x55
        self.chair_img = self._load_and_scale("椅子.png", 50, 55)
        # 桌子：缩放到约 90x60
        self.table_img = self._load_and_scale("桌子.png", 90, 60)
        # 电视机：缩放到约 100x80
        self.tv_img = self._load_and_scale("电视机.png", 100, 80)
        
        print(f"[CustomRoomScene] 素材加载完成")
        print(f"  地板tile: {self.floor_tile_width}x{self.floor_tile_height}")
        print(f"  木门: {self.door_img.get_width()}x{self.door_img.get_height()}")
        print(f"  冰箱: {self.fridge_img.get_width()}x{self.fridge_img.get_height()}")
        print(f"  桌子: {self.table_img.get_width()}x{self.table_img.get_height()}")
        print(f"  椅子: {self.chair_img.get_width()}x{self.chair_img.get_height()}")
        print(f"  电视: {self.tv_img.get_width()}x{self.tv_img.get_height()}")
    
    def _load_image(self, filename: str) -> pygame.Surface:
        """加载图片"""
        path = os.path.join(self.custom_assets_dir, filename)
        if not os.path.exists(path):
            print(f"[Warning] 图片不存在: {path}")
            # 返回占位符
            return pygame.Surface((100, 100), pygame.SRCALPHA)
        return pygame.image.load(path).convert_alpha()
    
    def _load_and_scale(self, filename: str, target_width: int, target_height: int) -> pygame.Surface:
        """加载并缩放图片"""
        img = self._load_image(filename)
        return pygame.transform.scale(img, (target_width, target_height))
    
    def _setup_room_layout(self):
        """设置房间布局"""
        # 房间尺寸（使用地板tile的倍数）
        # 地板tile: 408x423
        # 我们创建一个合理的房间大小
        
        # 计算需要的tile数量
        self.tiles_x = 3  # 横向3块地板
        self.tiles_y = 2  # 纵向2块地板
        
        # 实际房间尺寸
        self.room_width = self.tiles_x * self.floor_tile_width
        self.room_height = self.tiles_y * self.floor_tile_height
        
        # 墙壁厚度
        self.wall_thickness = 20
        
        # 计算包含墙壁的总尺寸
        self.total_width = self.room_width + self.wall_thickness * 2
        self.total_height = self.room_height + self.wall_thickness * 2
        
        # 门的位置（底部中央）
        self.door_width = self.door_img.get_width()
        self.door_height = self.door_img.get_height()
        self.door_x = (self.total_width - self.door_width) // 2
        self.door_y = self.total_height - self.door_height // 2  # 门底部对齐底部墙
        
        print(f"[CustomRoomScene] 房间布局:")
        print(f"  地板: {self.tiles_x}x{self.tiles_y} = {self.room_width}x{self.room_height}px")
        print(f"  总尺寸: {self.total_width}x{self.total_height}px")
    
    def _place_furniture(self):
        """放置家具"""
        # 墙壁偏移
        wx = self.wall_thickness
        wy = self.wall_thickness
        
        # 房间内部坐标（扣除墙壁）
        inner_left = wx
        inner_top = wy
        inner_right = wx + self.room_width
        inner_bottom = wy + self.room_height
        
        print(f"[CustomRoomScene] 房间内部区域: ({inner_left}, {inner_top}) 到 ({inner_right}, {inner_bottom})")
        
        # 1. 门（底部中央）
        door = FurnitureItem(
            "木门",
            self.door_img,
            self.door_x,
            self.total_height - self.door_img.get_height(),  # 门底部对齐底部墙
            collidable=False  # 门可以通行
        )
        self.furniture.append(door)
        
        # 2. 冰箱（左下角）- 靠左墙，底部
        fridge_x = inner_left + 30
        fridge_y = inner_bottom - self.fridge_img.get_height() - 30
        fridge = FurnitureItem(
            "冰箱",
            self.fridge_img,
            fridge_x,
            fridge_y,
            collidable=True
        )
        self.furniture.append(fridge)
        
        # 3. 电视机（右上角）- 靠右墙，顶部
        tv_x = inner_right - self.tv_img.get_width() - 30
        tv_y = inner_top + 30
        tv = FurnitureItem(
            "电视机",
            self.tv_img,
            tv_x,
            tv_y,
            collidable=True
        )
        self.furniture.append(tv)
        
        # 4. 桌子（右下角）- 靠右墙，底部
        table_x = inner_right - self.table_img.get_width() - 60
        table_y = inner_bottom - self.table_img.get_height() - 60
        table = FurnitureItem(
            "桌子",
            self.table_img,
            table_x,
            table_y,
            collidable=True
        )
        self.furniture.append(table)
        
        # 5. 椅子（桌子旁边）- 在桌子左侧
        chair_x = table_x - self.chair_img.get_width() - 10
        chair_y = table_y + (self.table_img.get_height() - self.chair_img.get_height()) // 2
        chair = FurnitureItem(
            "椅子",
            self.chair_img,
            chair_x,
            chair_y,
            collidable=True
        )
        self.furniture.append(chair)
        
        print(f"[CustomRoomScene] 放置家具: {len(self.furniture)} 件")
        for f in self.furniture:
            print(f"  {f.name}: ({f.x}, {f.y}) {f.width}x{f.height}")
    
    def add_entity(self, entity):
        """添加实体"""
        self.entities.append(entity)
    
    def remove_entity(self, entity):
        """移除实体"""
        if entity in self.entities:
            self.entities.remove(entity)
    
    def add_npc(self, npc: NPC):
        """添加NPC"""
        self.npcs.append(npc)
        self.entities.append(npc)
    
    def update(self, dt: float):
        """更新场景"""
        for entity in self.entities:
            if hasattr(entity, 'update'):
                entity.update(dt)
    
    def render(self, surface: pygame.Surface, camera=None, offset: Tuple[int, int] = (0, 0)):
        """
        渲染场景
        
        分层渲染：
        1. 地板层
        2. 墙壁层
        3. 家具层
        4. 实体层
        """
        # 获取相机偏移
        camera_x = int(camera.x) if camera else 0
        camera_y = int(camera.y) if camera else 0
        
        # 1. 渲染地板层（横竖交叠）
        self._render_floor(surface, camera_x, camera_y)
        
        # 2. 渲染墙壁
        self._render_walls(surface, camera_x, camera_y)
        
        # 3. 渲染家具（按Y坐标排序，实现深度效果）
        sorted_furniture = sorted(self.furniture, key=lambda f: f.y)
        for item in sorted_furniture:
            item.render(surface, camera_x, camera_y)
        
        # 4. 渲染实体（按Y坐标排序）
        sorted_entities = sorted(self.entities, key=lambda e: getattr(e, 'y', 0))
        for entity in sorted_entities:
            if hasattr(entity, 'render'):
                entity.render(surface, camera)
    
    def _render_floor(self, surface: pygame.Surface, camera_x: int, camera_y: int):
        """渲染地板（横竖交叠铺满）"""
        wx = self.wall_thickness
        wy = self.wall_thickness
        
        for row in range(self.tiles_y):
            for col in range(self.tiles_x):
                # 交替使用横向和竖向tile
                if (row + col) % 2 == 0:
                    tile = self.floor_tile_h
                else:
                    tile = self.floor_tile_v
                
                x = wx + col * self.floor_tile_width - camera_x
                y = wy + row * self.floor_tile_height - camera_y
                
                surface.blit(tile, (x, y))
    
    def _render_walls(self, surface: pygame.Surface, camera_x: int, camera_y: int):
        """渲染墙壁"""
        wall_color = (101, 67, 33)  # 深棕色木墙
        
        # 左墙
        left_wall = pygame.Rect(
            -camera_x, 
            -camera_y, 
            self.wall_thickness, 
            self.total_height
        )
        pygame.draw.rect(surface, wall_color, left_wall)
        
        # 右墙
        right_wall = pygame.Rect(
            self.total_width - camera_x, 
            -camera_y, 
            self.wall_thickness, 
            self.total_height
        )
        pygame.draw.rect(surface, wall_color, right_wall)
        
        # 上墙
        top_wall = pygame.Rect(
            -camera_x, 
            -camera_y, 
            self.total_width, 
            self.wall_thickness
        )
        pygame.draw.rect(surface, wall_color, top_wall)
        
        # 下墙（中间有门，分两段）
        door_rect = pygame.Rect(
            self.door_x,
            self.total_height - self.wall_thickness,
            self.door_width,
            self.wall_thickness
        )
        
        # 下墙左段
        bottom_left = pygame.Rect(
            -camera_x, 
            self.total_height - self.wall_thickness - camera_y, 
            self.door_x, 
            self.wall_thickness
        )
        pygame.draw.rect(surface, wall_color, bottom_left)
        
        # 下墙右段
        bottom_right = pygame.Rect(
            self.door_x + self.door_width - camera_x, 
            self.total_height - self.wall_thickness - camera_y, 
            self.total_width - self.door_x - self.door_width, 
            self.wall_thickness
        )
        pygame.draw.rect(surface, wall_color, bottom_right)
    
    def get_pixel_size(self) -> Tuple[int, int]:
        """获取场景像素尺寸"""
        return (self.total_width, self.total_height)
    
    def get_grid_size(self) -> Tuple[int, int]:
        """获取场景格子尺寸（兼容接口）"""
        return (self.tiles_x, self.tiles_y)
    
    def get_spawn_position(self) -> Tuple[float, float]:
        """获取玩家出生位置（门前）"""
        return (
            float(self.door_x + self.door_width // 2),
            float(self.total_height - self.wall_thickness - 50)
        )
    
    def is_position_walkable(self, x: float, y: float) -> bool:
        """检查位置是否可通行"""
        # 检查是否在左墙或右墙内
        if x < self.wall_thickness or x > self.total_width - self.wall_thickness:
            return False
        
        # 检查是否在上墙内
        if y < self.wall_thickness:
            return False
        
        # 检查是否在下墙内（除了门的位置）
        if y > self.total_height - self.wall_thickness:
            # 检查是否在门的位置
            if not (self.door_x <= x <= self.door_x + self.door_width):
                return False
        
        # 检查是否与家具碰撞
        for item in self.furniture:
            if item.collidable:
                rect = item.get_rect()
                if rect.collidepoint(x, y):
                    return False
        
        return True
    
    def get_walkable_tiles(self) -> List[Tuple[int, int]]:
        """获取可通行格子（兼容接口）"""
        tiles = []
        for y in range(self.tiles_y):
            for x in range(self.tiles_x):
                tiles.append((x, y))
        return tiles
    
    # ===== 兼容接口（供Player使用） =====
    @property
    def tile_size(self) -> int:
        """Tile尺寸（兼容接口）"""
        return self.floor_tile_width
    
    @property
    def tilemap(self):
        """TileMap对象（兼容接口，返回self）"""
        # 返回一个简单的对象，提供width/height属性
        class SimpleTilemap:
            def __init__(self, width, height):
                self.width = width
                self.height = height
            
            def get_tile(self, x, y):
                # 返回None，因为我们使用自定义碰撞检测
                return None
        
        return SimpleTilemap(self.tiles_x, self.tiles_y)
    
    def _init_test_npcs(self):
        """初始化测试NPC"""
        # 在房间内放置几个NPC
        npc_configs = [
            (200, 300, 'green', '小绿'),
            (500, 250, 'blue', '小蓝'),
            (400, 400, 'yellow', '小黄'),
        ]
        
        for x, y, color, name in npc_configs:
            npc = NPC(x, y, color, name)
            self.add_npc(npc)
