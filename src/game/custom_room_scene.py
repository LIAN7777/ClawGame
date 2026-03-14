"""
ClawGame - 自定义室内场景模块
使用用户提供的素材渲染房间
"""

import os
import random
from typing import Dict, List, Optional, Tuple

import pygame

from game.tilemap import TileMap
from game.entity.npc import NPC
from config.tiles import get_scaled_size


class FurnitureItem:
    """家具物品（支持像素级碰撞检测）"""
    def __init__(self, name: str, image: pygame.Surface, x: int, y: int, collidable: bool = True):
        self.name = name
        self.image = image
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.collidable = collidable
        
        # 碰撞矩形（用于粗略检测）
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # 像素级碰撞遮罩（基于 alpha 通道）
        self.mask = None
        if collidable:
            try:
                self.mask = pygame.mask.from_surface(image)
            except Exception as e:
                print(f"[FurnitureItem] 创建 mask 失败: {e}")
    
    def get_rect(self) -> pygame.Rect:
        """获取碰撞矩形"""
        return self.rect.copy()
    
    def collides_with_point(self, world_x: int, world_y: int) -> bool:
        """
        检测世界坐标点是否与家具碰撞
        
        Args:
            world_x: 世界 X 坐标
            world_y: 世界 Y 坐标
            
        Returns:
            是否碰撞
        """
        if not self.collidable:
            return False
        
        # 转换为相对于家具图片的局部坐标
        local_x = world_x - self.x
        local_y = world_y - self.y
        
        # 检查是否在图片范围内
        if local_x < 0 or local_x >= self.width or local_y < 0 or local_y >= self.height:
            return False
        
        # 如果没有 mask，使用矩形碰撞
        if self.mask is None:
            return True
        
        # 使用 mask 检测像素级碰撞
        try:
            # mask.get_at() 返回该点的值，0 表示透明，非0 表示不透明
            return self.mask.get_at((local_x, local_y)) != 0
        except IndexError:
            return False
    
    def collides_with_rect(self, rect: pygame.Rect, check_corners: bool = True) -> bool:
        """
        检测矩形是否与家具碰撞
        
        Args:
            rect: 世界坐标矩形
            check_corners: 是否只检测角点（更快但不够精确）
            
        Returns:
            是否碰撞
        """
        if not self.collidable:
            return False
        
        # 先用矩形做粗略检测
        if not self.rect.colliderect(rect):
            return False
        
        # 如果没有 mask，使用矩形碰撞
        if self.mask is None:
            return True
        
        # 检测点列表
        if check_corners:
            # 只检测矩形的角点和中心点（更快）
            points = [
                rect.topleft,
                rect.topright,
                rect.bottomleft,
                rect.bottomright,
                rect.center,
                (rect.left, rect.centery),
                (rect.right, rect.centery),
                (rect.centerx, rect.top),
                (rect.centerx, rect.bottom),
            ]
        else:
            # 检测更多点（更精确但更慢）
            points = []
            step = 4  # 每 4 像素检测一次
            for px in range(rect.left, rect.right, step):
                for py in range(rect.top, rect.bottom, step):
                    points.append((px, py))
        
        # 检测每个点
        for px, py in points:
            if self.collides_with_point(px, py):
                return True
        
        return False
    
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
        # 地板tile目标尺寸：缩小到32px让地板更密集
        self.target_tile_size = 32
        
        # 加载地板tiles并缩放
        raw_tile_h = self._load_image("木地板tile_横.png")
        raw_tile_v = self._load_image("木地板tile_竖.png")
        
        self.floor_tile_h = pygame.transform.scale(raw_tile_h, (self.target_tile_size, self.target_tile_size))
        self.floor_tile_v = pygame.transform.scale(raw_tile_v, (self.target_tile_size, self.target_tile_size))
        
        # 地板tile尺寸
        self.floor_tile_width = self.target_tile_size
        self.floor_tile_height = self.target_tile_size
        
        # 加载家具（重新设计的尺寸）
        # 门：缩放到约 60x90
        self.door_img = self._load_and_scale("木门.png", 60, 90)
        # 冰箱：缩放到约 80x130（稍大一点）
        self.fridge_img = self._load_and_scale("冰箱.png", 80, 130)
        # 椅子：缩放到约 60x66
        self.chair_img = self._load_and_scale("椅子.png", 60, 66)
        # 桌子（中心桌）：做大一点，约 140x95
        self.table_img = self._load_and_scale("桌子.png", 140, 95)
        # 电视机：缩放到约 120x95
        self.tv_img = self._load_and_scale("电视机.png", 120, 95)
        
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
        # 扩大房间以容纳更多家具
        self.tiles_x = 20  # 横向20块地板 (20 * 32 = 640)
        self.tiles_y = 15  # 纵向15块地板 (15 * 32 = 480)
        
        # 实际房间尺寸
        self.room_width = self.tiles_x * self.floor_tile_width
        self.room_height = self.tiles_y * self.floor_tile_height
        
        # 墙壁厚度
        self.wall_thickness = 20
        
        # 计算包含墙壁的总尺寸
        self.total_width = self.room_width + self.wall_thickness * 2
        self.total_height = self.room_height + self.wall_thickness * 2
        
        # 门的位置（底部中央，门底部在房间底部）
        self.door_width = self.door_img.get_width()
        self.door_height = self.door_img.get_height()
        self.door_x = (self.total_width - self.door_width) // 2
        # 门放置在房间内部底部，底部对齐下墙壁顶部
        self.door_y = self.total_height - self.wall_thickness - self.door_height
        
        print(f"[CustomRoomScene] 房间布局:")
        print(f"  地板: {self.tiles_x}x{self.tiles_y} = {self.room_width}x{self.room_height}px")
        print(f"  总尺寸: {self.total_width}x{self.total_height}px")
    
    def _place_furniture(self):
        """放置家具（随机位置，增加重复家具）"""
        # 墙壁偏移
        wx = self.wall_thickness
        wy = self.wall_thickness
        
        # 房间内部坐标（扣除墙壁）
        inner_left = wx
        inner_top = wy
        inner_right = wx + self.room_width
        inner_bottom = wy + self.room_height
        
        # 门的禁区（底部中央区域，家具不能放这里，确保出生点安全）
        # 禁区只需要覆盖门和门前小区域
        door_clear_zone = pygame.Rect(
            self.door_x - 40,  # 左侧扩展40px
            self.door_y - 80,  # 门前扩展80px（覆盖出生点）
            self.door_img.get_width() + 80,  # 右侧扩展40px
            self.door_img.get_height() + 100  # 底部扩展
        )
        
        print(f"[CustomRoomScene] 房间内部区域: ({inner_left}, {inner_top}) 到 ({inner_right}, {inner_bottom})")
        print(f"[CustomRoomScene] 门口禁区: {door_clear_zone}")
        
        # 已放置的家具位置列表（用于碰撞检测）
        placed_rects: List[pygame.Rect] = []
        
        def can_place(rect: pygame.Rect) -> bool:
            """检查是否可以放置（不与其他家具或门冲突）"""
            # 检查是否与门冲突
            if rect.colliderect(door_clear_zone):
                return False
            # 检查是否与其他家具冲突
            for existing in placed_rects:
                # 增加间距（家具之间保留30px通行空间）
                expanded = existing.inflate(30, 30)
                if rect.colliderect(expanded):
                    return False
            return True
        
        def find_random_position(width: int, height: int, max_attempts: int = 50) -> Optional[Tuple[int, int]]:
            """找到随机可用位置"""
            for _ in range(max_attempts):
                # 在房间内部随机位置
                x = random.randint(inner_left + 20, inner_right - width - 20)
                y = random.randint(inner_top + 20, inner_bottom - height - 20)
                rect = pygame.Rect(x, y, width, height)
                if can_place(rect):
                    return (x, y)
            return None
        
        # 1. 门（底部中央，固定位置）
        door = FurnitureItem(
            "木门",
            self.door_img,
            self.door_x,
            self.door_y,
            collidable=False
        )
        self.furniture.append(door)
        placed_rects.append(door.get_rect())
        
        # ===== 新的家具布置逻辑 =====
        # 房间中心区域
        room_center_x = (inner_left + inner_right) // 2
        room_center_y = (inner_top + inner_bottom) // 2
        
        # 2. 中心桌子（1张大桌子，放在房间中心偏左）
        table_w = self.table_img.get_width()
        table_h = self.table_img.get_height()
        center_table_x = room_center_x - table_w // 2 - 50  # 偏左一点
        center_table_y = room_center_y - table_h // 2
        
        center_table = FurnitureItem("中心桌", self.table_img, center_table_x, center_table_y, collidable=True)
        self.furniture.append(center_table)
        placed_rects.append(center_table.get_rect())
        
        # 3. 桌子周围的椅子（2-3把，围绕桌子）
        chair_w = self.chair_img.get_width()
        chair_h = self.chair_img.get_height()
        chair_spacing = 70  # 椅子间距
        
        # 椅子位置：桌子下方和两侧
        chair_positions = [
            (center_table_x + table_w // 2 - chair_w // 2, center_table_y + table_h + 10),  # 下方
            (center_table_x - chair_w - 10, center_table_y + table_h // 2 - chair_h // 2),  # 左侧
            (center_table_x + table_w + 10, center_table_y + table_h // 2 - chair_h // 2),  # 右侧
        ]
        
        for i, (cx, cy) in enumerate(chair_positions[:3]):
            chair = FurnitureItem(f"椅子{i+1}", self.chair_img, cx, cy, collidable=True)
            self.furniture.append(chair)
            placed_rects.append(chair.get_rect())
        
        # 4. 冰箱（左上角靠墙）
        fridge_w = self.fridge_img.get_width()
        fridge_h = self.fridge_img.get_height()
        fridge_x = inner_left + 20
        fridge_y = inner_top + 30
        
        fridge = FurnitureItem("冰箱", self.fridge_img, fridge_x, fridge_y, collidable=True)
        self.furniture.append(fridge)
        placed_rects.append(fridge.get_rect())
        
        # 5. 电视机（右上角靠墙）
        tv_w = self.tv_img.get_width()
        tv_h = self.tv_img.get_height()
        tv_x = inner_right - tv_w - 30
        tv_y = inner_top + 30
        
        tv = FurnitureItem("电视机", self.tv_img, tv_x, tv_y, collidable=True)
        self.furniture.append(tv)
        placed_rects.append(tv.get_rect())
        
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
        npc.set_scene(self)  # 设置场景引用，用于碰撞检测
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
        """获取玩家出生位置（门内安全区域）"""
        # 出生点在门的正前方，确保在门禁区内
        spawn_x = float(self.door_x + self.door_width // 2)
        spawn_y = float(self.door_y - 50)  # 在门前50像素处
        return (spawn_x, spawn_y)
    
    def is_position_walkable(self, x: float, y: float) -> bool:
        """检查位置是否可通行（支持像素级碰撞检测）"""
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
        
        # 检查是否与家具碰撞（使用像素级检测）
        for item in self.furniture:
            if item.collides_with_point(int(x), int(y)):
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
        # 第一个是 LLM NPC（小橘）
        xiaoju = NPC(300, 300, 'yellow', '小橘', use_llm=True, persona_name='小橘')
        self.add_npc(xiaoju)
        
        # 其他是传统 NPC
        npc_configs = [
            (200, 200, 'green', '小绿'),
            (500, 300, 'blue', '小蓝'),
        ]
        
        for x, y, color, name in npc_configs:
            npc = NPC(x, y, color, name)
            self.add_npc(npc)
