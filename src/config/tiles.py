# ClawGame Tile 配置
# 基于 Kenney 1-Bit Pack tileset

# =============================================================================
# Tileset 基本信息
# =============================================================================
TILESET_PATH = "assets/images/tiles/tileset.png"
TILE_SIZE = 16  # 原始 tile 尺寸 (像素)
TILE_SCALE = 3  # 缩放倍数 (16 * 3 = 48 最终尺寸)
TILESET_COLS = 49  # tileset 列数
TILESET_ROWS = 22  # tileset 行数

# =============================================================================
# Tile ID 映射 (基于 tilesheet 分析)
# =============================================================================
class TileID:
    """Tile ID 常量定义 (从 1 开始编号)"""
    
    # -------------------------------------------------------------------------
    # 墙壁类 (Row 0-2)
    # -------------------------------------------------------------------------
    WALL_BASIC = 1          # 基础墙壁
    WALL_STONE_1 = 2        # 石墙变体 1
    WALL_STONE_2 = 3        # 石墙变体 2
    WALL_BRICK_1 = 4        # 砖墙变体 1
    WALL_BRICK_2 = 5        # 砖墙变体 2
    WALL_WINDOW_1 = 6       # 窗户变体 1
    WALL_WINDOW_2 = 7       # 窗户变体 2
    WALL_DOOR = 8           # 门
    
    # -------------------------------------------------------------------------
    # 地板类 (Row 3-4)
    # -------------------------------------------------------------------------
    FLOOR_BASIC = 148       # 基础地板 (row 3, col 0)
    FLOOR_WOOD_H = 149      # 木地板横向
    FLOOR_WOOD_V = 150      # 木地板纵向
    FLOOR_STONE_1 = 151     # 石地板变体 1
    FLOOR_STONE_2 = 152     # 石地板变体 2
    FLOOR_TILE_1 = 153      # 瓷砖地板 1
    FLOOR_TILE_2 = 154      # 瓷砖地板 2
    FLOOR_CARPET_1 = 155    # 地毯变体 1
    FLOOR_CARPET_2 = 156    # 地毯变体 2
    FLOOR_CARPET_3 = 197    # 地毯变体 3 (row 4, col 0)
    FLOOR_CARPET_4 = 198    # 地毯变体 4
    FLOOR_CARPET_5 = 199    # 地毯变体 5
    
    # -------------------------------------------------------------------------
    # 桌子类 (Row 5-6) - 单个 tile 桌子
    # -------------------------------------------------------------------------
    TABLE_SMALL_1 = 246     # 小桌子变体 1 (row 5, col 0)
    TABLE_SMALL_2 = 247     # 小桌子变体 2
    TABLE_SMALL_3 = 248     # 小桌子变体 3
    TABLE_LARGE_1 = 249     # 大桌子变体 1
    TABLE_LARGE_2 = 250     # 大桌子变体 2
    TABLE_LARGE_3 = 251     # 大桌子变体 3
    TABLE_LARGE_4 = 252     # 大桌子变体 4
    TABLE_DESK_1 = 295      # 书桌变体 1 (row 6, col 0)
    TABLE_DESK_2 = 296      # 书桌变体 2
    TABLE_DESK_3 = 297      # 书桌变体 3
    TABLE_DESK_4 = 298      # 书桌变体 4
    
    # -------------------------------------------------------------------------
    # 椅子类 (Row 5-7)
    # -------------------------------------------------------------------------
    CHAIR_BASIC = 253       # 基础椅子
    CHAIR_FANCY_1 = 254     # 装饰椅变体 1
    CHAIR_FANCY_2 = 255     # 装饰椅变体 2
    CHAIR_FANCY_3 = 256     # 装饰椅变体 3
    CHAIR_WOODEN = 299      # 木椅 (row 6, col 4)
    CHAIR_CUSHION = 300     # 软垫椅
    CHAIR_ARM_1 = 301       # 扶手椅变体 1
    CHAIR_ARM_2 = 302       # 扶手椅变体 2
    
    # -------------------------------------------------------------------------
    # 床类 (Row 7-8)
    # -------------------------------------------------------------------------
    BED_SINGLE_1 = 344      # 单人床变体 1 (row 7, col 0)
    BED_SINGLE_2 = 345      # 单人床变体 2
    BED_SINGLE_3 = 346      # 单人床变体 3
    BED_DOUBLE_1 = 347      # 双人床变体 1
    BED_DOUBLE_2 = 348      # 双人床变体 2
    BED_DOUBLE_3 = 349      # 双人床变体 3
    BED_DOUBLE_4 = 350      # 双人床变体 4
    BED_BUNK_1 = 393        # 上下铺变体 1 (row 8, col 0)
    BED_BUNK_2 = 394        # 上下铺变体 2
    BED_BUNK_3 = 395        # 上下铺变体 3
    
    # -------------------------------------------------------------------------
    # 沙发类 (Row 8-9)
    # -------------------------------------------------------------------------
    SOFA_SMALL = 396        # 小沙发 (row 8, col 3)
    SOFA_MEDIUM = 397       # 中型沙发
    SOFA_LARGE_1 = 398      # 大沙发变体 1
    SOFA_LARGE_2 = 399      # 大沙发变体 2
    SOFA_SECTIONAL = 442    # 组合沙发 (row 9, col 0)
    SOFA_ARMCHAIR = 443     # 沙发椅
    SOFA_LOVESEAT = 444     # 双人座沙发
    SOFA_CORNER = 445       # 角落沙发
    
    # -------------------------------------------------------------------------
    # 柜子/储物类 (Row 10-11)
    # -------------------------------------------------------------------------
    SHELF_SMALL = 491       # 小书架 (row 10, col 0)
    SHELF_MEDIUM = 492      # 中型书架
    SHELF_LARGE = 493       # 大书架
    SHELF_TALL = 494        # 高书架
    CABINET_SMALL = 495     # 小柜子
    CABINET_MEDIUM = 496    # 中型柜子
    CABINET_LARGE = 497     # 大柜子
    CABINET_TALL = 538      # 高柜子 (row 11, col 0)
    DRESSER_1 = 539         # 梳妆台变体 1
    DRESSER_2 = 540         # 梳妆台变体 2
    WARDROBE_1 = 541        # 衣柜变体 1
    WARDROBE_2 = 542        # 衣柜变体 2
    
    # -------------------------------------------------------------------------
    # 厨房类 (Row 12-13)
    # -------------------------------------------------------------------------
    STOVE = 585             # 炉灶 (row 12, col 0)
    SINK_1 = 586            # 水槽变体 1
    SINK_2 = 587            # 水槽变体 2
    FRIDGE_1 = 588          # 冰箱变体 1
    FRIDGE_2 = 589          # 冰箱变体 2
    COUNTER_1 = 590         # 台面变体 1
    COUNTER_2 = 591         # 台面变体 2
    MICROWAVE = 634         # 微波炉 (row 13, col 0)
    TOASTER = 635           # 烤面包机
    BLENDER = 636           # 搅拌机
    COFFEE_MAKER = 637      # 咖啡机
    
    # -------------------------------------------------------------------------
    # 卫浴类 (Row 13-14)
    # -------------------------------------------------------------------------
    TOILET = 638            # 马桶
    BATHTUB_1 = 639         # 浴缸变体 1
    BATHTUB_2 = 640         # 浴缸变体 2
    SHOWER = 641            # 淋浴
    SINK_BATH = 683         # 浴室洗手池 (row 14, col 0)
    MIRROR = 684            # 镜子
    TOWEL_RACK = 685        # 毛巾架
    
    # -------------------------------------------------------------------------
    # 装饰类 (Row 14-18)
    # -------------------------------------------------------------------------
    PLANT_SMALL = 686       # 小盆栽
    PLANT_MEDIUM = 687      # 中型盆栽
    PLANT_LARGE = 688       # 大型盆栽
    LAMP_DESK = 689         # 台灯
    LAMP_FLOOR = 732        # 落地灯 (row 15, col 0)
    RUG_1 = 733             # 地毯装饰 1
    RUG_2 = 734             # 地毯装饰 2
    RUG_3 = 735             # 地毯装饰 3
    PICTURE_1 = 736         # 挂画 1
    PICTURE_2 = 779         # 挂画 2 (row 16, col 0)
    PICTURE_3 = 780         # 挂画 3
    CLOCK = 781             # 时钟
    TV = 782                # 电视
    BOOKS_1 = 825           # 书堆 1 (row 17, col 0)
    BOOKS_2 = 826           # 书堆 2
    VASE = 827              # 花瓶
    CANDLE = 828            # 蜡烛
    TROPHY = 829            # 奖杯
    
    # -------------------------------------------------------------------------
    # 电器类 (Row 18-21)
    # -------------------------------------------------------------------------
    COMPUTER = 872           # 电脑 (row 18, col 0)
    LAPTOP = 873             # 笔记本电脑
    PRINTER = 874            # 打印机
    TV_LARGE = 875           # 大电视
    STEREO = 918             # 音响 (row 19, col 0)
    GAME_CONSOLE = 919       # 游戏机
    FAN = 920                # 风扇
    HEATER = 921             # 加热器
    WASHER = 964             # 洗衣机 (row 20, col 0)
    DRYER = 965              # 烘干机
    VACUUM = 966             # 吸尘器
    TOOLBOX = 1008           # 工具箱 (row 21, col 0)


# =============================================================================
# Tile 分组
# =============================================================================
TILE_GROUPS = {
    "walls": [
        TileID.WALL_BASIC, TileID.WALL_STONE_1, TileID.WALL_STONE_2,
        TileID.WALL_BRICK_1, TileID.WALL_BRICK_2, TileID.WALL_WINDOW_1,
        TileID.WALL_WINDOW_2, TileID.WALL_DOOR
    ],
    "floors": [
        TileID.FLOOR_BASIC, TileID.FLOOR_WOOD_H, TileID.FLOOR_WOOD_V,
        TileID.FLOOR_STONE_1, TileID.FLOOR_STONE_2, TileID.FLOOR_TILE_1,
        TileID.FLOOR_TILE_2, TileID.FLOOR_CARPET_1, TileID.FLOOR_CARPET_2,
        TileID.FLOOR_CARPET_3, TileID.FLOOR_CARPET_4, TileID.FLOOR_CARPET_5
    ],
    "tables": [
        TileID.TABLE_SMALL_1, TileID.TABLE_SMALL_2, TileID.TABLE_SMALL_3,
        TileID.TABLE_LARGE_1, TileID.TABLE_LARGE_2, TileID.TABLE_LARGE_3,
        TileID.TABLE_LARGE_4, TileID.TABLE_DESK_1, TileID.TABLE_DESK_2,
        TileID.TABLE_DESK_3, TileID.TABLE_DESK_4
    ],
    "chairs": [
        TileID.CHAIR_BASIC, TileID.CHAIR_FANCY_1, TileID.CHAIR_FANCY_2,
        TileID.CHAIR_FANCY_3, TileID.CHAIR_WOODEN, TileID.CHAIR_CUSHION,
        TileID.CHAIR_ARM_1, TileID.CHAIR_ARM_2
    ],
    "beds": [
        TileID.BED_SINGLE_1, TileID.BED_SINGLE_2, TileID.BED_SINGLE_3,
        TileID.BED_DOUBLE_1, TileID.BED_DOUBLE_2, TileID.BED_DOUBLE_3,
        TileID.BED_DOUBLE_4, TileID.BED_BUNK_1, TileID.BED_BUNK_2,
        TileID.BED_BUNK_3
    ],
    "sofas": [
        TileID.SOFA_SMALL, TileID.SOFA_MEDIUM, TileID.SOFA_LARGE_1,
        TileID.SOFA_LARGE_2, TileID.SOFA_SECTIONAL, TileID.SOFA_ARMCHAIR,
        TileID.SOFA_LOVESEAT, TileID.SOFA_CORNER
    ],
    "cabinets": [
        TileID.SHELF_SMALL, TileID.SHELF_MEDIUM, TileID.SHELF_LARGE,
        TileID.SHELF_TALL, TileID.CABINET_SMALL, TileID.CABINET_MEDIUM,
        TileID.CABINET_LARGE, TileID.CABINET_TALL, TileID.DRESSER_1,
        TileID.DRESSER_2, TileID.WARDROBE_1, TileID.WARDROBE_2
    ],
    "kitchen": [
        TileID.STOVE, TileID.SINK_1, TileID.SINK_2, TileID.FRIDGE_1,
        TileID.FRIDGE_2, TileID.COUNTER_1, TileID.COUNTER_2,
        TileID.MICROWAVE, TileID.TOASTER, TileID.BLENDER, TileID.COFFEE_MAKER
    ],
    "bathroom": [
        TileID.TOILET, TileID.BATHTUB_1, TileID.BATHTUB_2, TileID.SHOWER,
        TileID.SINK_BATH, TileID.MIRROR, TileID.TOWEL_RACK
    ],
    "decorations": [
        TileID.PLANT_SMALL, TileID.PLANT_MEDIUM, TileID.PLANT_LARGE,
        TileID.LAMP_DESK, TileID.LAMP_FLOOR, TileID.RUG_1, TileID.RUG_2,
        TileID.RUG_3, TileID.PICTURE_1, TileID.PICTURE_2, TileID.PICTURE_3,
        TileID.CLOCK, TileID.TV, TileID.BOOKS_1, TileID.BOOKS_2,
        TileID.VASE, TileID.CANDLE, TileID.TROPHY
    ],
    "electronics": [
        TileID.COMPUTER, TileID.LAPTOP, TileID.PRINTER, TileID.TV_LARGE,
        TileID.STEREO, TileID.GAME_CONSOLE, TileID.FAN, TileID.HEATER,
        TileID.WASHER, TileID.DRYER, TileID.VACUUM, TileID.TOOLBOX
    ]
}


# =============================================================================
# 辅助函数
# =============================================================================
def get_tile_rect(tile_id: int) -> tuple:
    """
    根据 tile ID 获取在 tileset 中的像素坐标
    
    Args:
        tile_id: Tile ID (从 1 开始)
    
    Returns:
        tuple: (x, y, width, height) 像素坐标
    """
    index = tile_id - 1
    col = index % TILESET_COLS
    row = index // TILESET_COLS
    return (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)


def get_tile_grid_pos(tile_id: int) -> tuple:
    """
    根据 tile ID 获取在 tileset 中的格子坐标
    
    Args:
        tile_id: Tile ID (从 1 开始)
    
    Returns:
        tuple: (col, row) 格子坐标
    """
    index = tile_id - 1
    col = index % TILESET_COLS
    row = index // TILESET_COLS
    return (col, row)


def get_tile_id(col: int, row: int) -> int:
    """
    根据格子坐标获取 tile ID
    
    Args:
        col: 列号 (从 0 开始)
        row: 行号 (从 0 开始)
    
    Returns:
        int: Tile ID
    """
    return row * TILESET_COLS + col + 1


def get_scaled_size() -> int:
    """
    获取缩放后的 tile 尺寸
    
    Returns:
        int: 缩放后的尺寸 (像素)
    """
    return TILE_SIZE * TILE_SCALE


def is_valid_tile_id(tile_id: int) -> bool:
    """
    检查 tile ID 是否有效
    
    Args:
        tile_id: Tile ID
    
    Returns:
        bool: 是否有效
    """
    return 1 <= tile_id <= TILESET_COLS * TILESET_ROWS


def get_tiles_by_group(group_name: str) -> list:
    """
    根据分组名获取 tile ID 列表
    
    Args:
        group_name: 分组名称
    
    Returns:
        list: Tile ID 列表，如果分组不存在则返回空列表
    """
    return TILE_GROUPS.get(group_name, [])


# =============================================================================
# 调试与测试
# =============================================================================
if __name__ == "__main__":
    print("ClawGame Tile 配置")
    print("=" * 60)
    print(f"Tileset: {TILESET_PATH}")
    print(f"原始尺寸: {TILE_SIZE}x{TILE_SIZE}")
    print(f"缩放倍数: {TILE_SCALE}x")
    print(f"最终尺寸: {get_scaled_size()}x{get_scaled_size()}")
    print("=" * 60)
    
    print("\nTile 分组统计:")
    for group_name, tiles in TILE_GROUPS.items():
        print(f"  {group_name}: {len(tiles)} tiles")
    
    print("\n示例 Tile 信息:")
    sample_tiles = [
        ("基础墙壁", TileID.WALL_BASIC),
        ("基础地板", TileID.FLOOR_BASIC),
        ("小桌子", TileID.TABLE_SMALL_1),
        ("单人床", TileID.BED_SINGLE_1),
        ("小沙发", TileID.SOFA_SMALL),
    ]
    for name, tile_id in sample_tiles:
        rect = get_tile_rect(tile_id)
        grid = get_tile_grid_pos(tile_id)
        print(f"  {name} (ID={tile_id}): 格子={grid}, 像素={rect}")
