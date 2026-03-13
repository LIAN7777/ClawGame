# ClawGame Tile 配置
# 基于 Kenney Tiny Town Pack tileset

# =============================================================================
# Tileset 基本信息 (Tiny Town)
# =============================================================================
TILESET_PATH = "assets/images/tiles/tiny-town-tilesheet.png"
TILE_SIZE = 16  # 原始 tile 尺寸 (像素)
TILE_SCALE = 3  # 缩放倍数 (16 * 3 = 48 最终尺寸)
TILESET_COLS = 12  # tileset 列数
TILESET_ROWS = 11  # tileset 行数

# =============================================================================
# Tile ID 映射 (基于 Tiny Town tilesheet 分析)
# Tilesheet: 12 列 x 11 行 = 132 tiles
# ID 从 1 开始编号
# =============================================================================
class TileID:
    """Tiny Town Tile ID 常量定义 (从 1 开始编号)"""
    
    # -------------------------------------------------------------------------
    # 空白/背景
    # -------------------------------------------------------------------------
    EMPTY = 1               # 空白黑色背景 (row 0, col 0)
    
    # -------------------------------------------------------------------------
    # 墙壁类 (Row 0)
    # -------------------------------------------------------------------------
    WALL_DARK = 2           # 深色墙壁 (row 0, col 1)
    WALL_STONE_1 = 3        # 石墙变体 1 (row 0, col 2)
    WALL_STONE_2 = 4        # 石墙变体 2 (row 0, col 3)
    WALL_WOOD_1 = 5         # 木墙 (row 0, col 4) - 温馨木屋风格
    WALL_WOOD_2 = 6         # 木墙带装饰 (row 0, col 5)
    WALL_WINDOW = 7         # 窗户 (row 0, col 6)
    WALL_WOOD_3 = 8         # 木墙变体 (row 0, col 7)
    WALL_DOOR = 9           # 门 (row 0, col 8)
    WALL_WOOD_4 = 10        # 木墙 (row 0, col 9)
    WALL_CORNER_1 = 11      # 墙角 1 (row 0, col 10)
    WALL_CORNER_2 = 12      # 墙角 2 (row 0, col 11)
    
    # -------------------------------------------------------------------------
    # 地板类 (Row 1)
    # -------------------------------------------------------------------------
    FLOOR_WOOD_1 = 13       # 木地板浅棕 (row 1, col 0) - 主要地板
    FLOOR_WOOD_2 = 14       # 木地板变体 (row 1, col 1)
    FLOOR_WOOD_DARK = 15    # 木地板深色 (row 1, col 2)
    FLOOR_STONE_1 = 16      # 石地板 1 (row 1, col 3)
    FLOOR_STONE_2 = 17      # 石地板 2 (row 1, col 4)
    FLOOR_TILE_1 = 18       # 瓷砖地板 1 (row 1, col 5)
    FLOOR_TILE_2 = 19       # 瓷砖地板 2 (row 1, col 6)
    FLOOR_CARPET_RED = 20   # 红色地毯 (row 1, col 7) - 温馨装饰
    FLOOR_CARPET_BLUE = 21  # 蓝色地毯 (row 1, col 8)
    FLOOR_CARPET_CORNER = 22    # 地毯边角 (row 1, col 9)
    FLOOR_EDGE_1 = 23       # 地板边角 1 (row 1, col 10)
    FLOOR_EDGE_2 = 24       # 地板边角 2 (row 1, col 11)
    
    # -------------------------------------------------------------------------
    # 家具类 (Row 2)
    # -------------------------------------------------------------------------
    FURNITURE_CRATE = 25    # 木箱/柜子 (row 2, col 0)
    FURNITURE_BARREL = 26   # 木桶 (row 2, col 1)
    TABLE_WOOD = 27         # 木桌 (row 2, col 2) - 主要桌子
    CHAIR_SIDE = 28         # 椅子侧面 (row 2, col 3)
    CHAIR_FRONT = 29        # 椅子正面 (row 2, col 4)
    BED_RED = 30            # 红色床单 (row 2, col 5) - 主要床
    BED_VARIANT = 31        # 床变体 (row 2, col 6)
    BOOKSHELF = 32          # 书架 (row 2, col 7)
    BOOKSHELF_ALT = 33      # 书架变体 (row 2, col 8)
    TORCH_1 = 34            # 火把/火焰 1 (row 2, col 9)
    TORCH_2 = 35            # 火把/火焰 2 (row 2, col 10)
    STUMP = 36              # 木桩 (row 2, col 11)
    
    # -------------------------------------------------------------------------
    # 装饰类 (Row 3)
    # -------------------------------------------------------------------------
    DECOR_VASE_1 = 37       # 花瓶/罐子 1 (row 3, col 0)
    DECOR_ITEM_1 = 38       # 装饰品 1 (row 3, col 1)
    PLANT = 39              # 植物 (row 3, col 2) - 盆栽
    DECOR_VASE_2 = 40       # 花瓶 2 (row 3, col 3)
    WALL_DECOR = 41         # 墙上装饰 (row 3, col 4)
    KEY = 42                # 钥匙 (row 3, col 5)
    GEM_1 = 43              # 宝石 1 (row 3, col 6)
    GEM_2 = 44              # 宝石 2 (row 3, col 7)
    # tile 45-48 为地牢风格装饰，不适合木屋室内
    
    # -------------------------------------------------------------------------
    # 箱子/储物类 (Row 4)
    # -------------------------------------------------------------------------
    CHEST_CLOSED = 49       # 箱子关闭 (row 4, col 0)
    CHEST_OPEN = 50         # 箱子打开 (row 4, col 1)
    DOOR_FRAME = 51         # 门框 (row 4, col 2)
    DOOR_WOOD = 52          # 木门 (row 4, col 3)
    STAIRS_1 = 53           # 台阶 1 (row 4, col 4)
    STAIRS_2 = 54           # 台阶 2 (row 4, col 5)
    # tile 55-60 为武器道具类


# =============================================================================
# Tile 分组 (Tiny Town)
# =============================================================================
TILE_GROUPS = {
    "walls": [
        TileID.WALL_DARK, TileID.WALL_STONE_1, TileID.WALL_STONE_2,
        TileID.WALL_WOOD_1, TileID.WALL_WOOD_2, TileID.WALL_WINDOW,
        TileID.WALL_WOOD_3, TileID.WALL_DOOR, TileID.WALL_WOOD_4,
        TileID.WALL_CORNER_1, TileID.WALL_CORNER_2
    ],
    "floors": [
        TileID.FLOOR_WOOD_1, TileID.FLOOR_WOOD_2, TileID.FLOOR_WOOD_DARK,
        TileID.FLOOR_STONE_1, TileID.FLOOR_STONE_2, TileID.FLOOR_TILE_1,
        TileID.FLOOR_TILE_2, TileID.FLOOR_CARPET_RED, TileID.FLOOR_CARPET_BLUE,
        TileID.FLOOR_CARPET_CORNER, TileID.FLOOR_EDGE_1, TileID.FLOOR_EDGE_2
    ],
    "furniture": [
        TileID.FURNITURE_CRATE, TileID.FURNITURE_BARREL,
        TileID.TABLE_WOOD, TileID.CHAIR_SIDE, TileID.CHAIR_FRONT,
        TileID.BED_RED, TileID.BED_VARIANT, TileID.BOOKSHELF, TileID.BOOKSHELF_ALT
    ],
    "decorations": [
        TileID.DECOR_VASE_1, TileID.DECOR_ITEM_1, TileID.PLANT,
        TileID.DECOR_VASE_2, TileID.WALL_DECOR,
        TileID.TORCH_1, TileID.TORCH_2, TileID.STUMP,
        TileID.CHEST_CLOSED, TileID.CHEST_OPEN
    ],
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
    print("ClawGame Tile 配置 (Tiny Town)")
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
        ("木墙", TileID.WALL_WOOD_1),
        ("木地板", TileID.FLOOR_WOOD_1),
        ("木桌", TileID.TABLE_WOOD),
        ("红床", TileID.BED_RED),
        ("书架", TileID.BOOKSHELF),
    ]
    for name, tile_id in sample_tiles:
        rect = get_tile_rect(tile_id)
        grid = get_tile_grid_pos(tile_id)
        print(f"  {name} (ID={tile_id}): 格子={grid}, 像素={rect}")
