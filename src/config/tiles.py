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
# Tile ID 映射
# =============================================================================
class TileID:
    """Tile ID 常量定义 (从 1 开始编号)"""
    
    # -------------------------------------------------------------------------
    # 墙壁类
    # -------------------------------------------------------------------------
    WALL_BASIC = 1          # 基础墙壁
    WALL_DECOR_1 = 2        # 墙壁装饰变体 1
    WALL_DECOR_2 = 4        # 墙壁装饰变体 2
    
    # -------------------------------------------------------------------------
    # 地板类
    # -------------------------------------------------------------------------
    FLOOR_BASIC = 41        # 基础地板 (底部边界)
    FLOOR_WOOD_1 = 417      # 木地板变体 1
    FLOOR_WOOD_2 = 419      # 木地板变体 2
    
    # -------------------------------------------------------------------------
    # 桌子组合 (从左到右排列)
    # -------------------------------------------------------------------------
    TABLE_TOP_LEFT = 257    # 桌子左上角
    TABLE_TOP_MID_1 = 258   # 桌子上部中间 1
    TABLE_TOP_MID_2 = 260   # 桌子上部中间 2
    TABLE_TOP_RIGHT = 261   # 桌子右上角
    TABLE_LEG = 262         # 桌子腿/侧边
    
    # -------------------------------------------------------------------------
    # 椅子类
    # -------------------------------------------------------------------------
    CHAIR_1 = 228           # 椅子变体 1
    CHAIR_2 = 229           # 椅子变体 2
    CHAIR_3 = 265           # 椅子变体 3
    CHAIR_4 = 269           # 椅子变体 4
    
    # -------------------------------------------------------------------------
    # 桌椅组合
    # -------------------------------------------------------------------------
    TABLE_CHAIR_1 = 273     # 桌椅组合 1
    TABLE_CHAIR_2 = 292     # 桌椅组合 2
    TABLE_CHAIR_3 = 305     # 桌椅组合 3
    TABLE_CHAIR_4 = 337     # 桌椅组合 4
    
    # -------------------------------------------------------------------------
    # 装饰类
    # -------------------------------------------------------------------------
    DECOR_1 = 5             # 装饰物 1
    DECOR_2 = 35            # 装饰物 2
    DECOR_3 = 59            # 装饰物 3
    DECOR_4 = 63            # 装饰物 4
    DECOR_5 = 89            # 装饰物 5
    DECOR_6 = 154           # 装饰物 6
    DECOR_7 = 218           # 装饰物 7
    DECOR_8 = 236           # 装饰物 8
    DECOR_9 = 237           # 装饰物 9
    DECOR_10 = 485          # 装饰物 10
    DECOR_11 = 486          # 装饰物 11


# =============================================================================
# Tile 分组
# =============================================================================
TILE_GROUPS = {
    "walls": [TileID.WALL_BASIC, TileID.WALL_DECOR_1, TileID.WALL_DECOR_2],
    "floors": [TileID.FLOOR_BASIC, TileID.FLOOR_WOOD_1, TileID.FLOOR_WOOD_2],
    "tables": [
        TileID.TABLE_TOP_LEFT, TileID.TABLE_TOP_MID_1, 
        TileID.TABLE_TOP_MID_2, TileID.TABLE_TOP_RIGHT, TileID.TABLE_LEG
    ],
    "chairs": [
        TileID.CHAIR_1, TileID.CHAIR_2, 
        TileID.CHAIR_3, TileID.CHAIR_4
    ],
    "furniture": [
        TileID.TABLE_CHAIR_1, TileID.TABLE_CHAIR_2,
        TileID.TABLE_CHAIR_3, TileID.TABLE_CHAIR_4
    ],
    "decorations": [
        TileID.DECOR_1, TileID.DECOR_2, TileID.DECOR_3,
        TileID.DECOR_4, TileID.DECOR_5, TileID.DECOR_6,
        TileID.DECOR_7, TileID.DECOR_8, TileID.DECOR_9,
        TileID.DECOR_10, TileID.DECOR_11
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
        group_name: 分组名称 ("walls", "floors", "tables", "chairs", "furniture", "decorations")
    
    Returns:
        list: Tile ID 列表，如果分组不存在则返回空列表
    """
    return TILE_GROUPS.get(group_name, [])


# =============================================================================
# 调试与测试
# =============================================================================
if __name__ == "__main__":
    # 测试常用的 tile
    test_tiles = [
        ("墙壁", TileID.WALL_BASIC),
        ("木地板 1", TileID.FLOOR_WOOD_1),
        ("桌子左上", TileID.TABLE_TOP_LEFT),
        ("椅子 1", TileID.CHAIR_1),
    ]
    
    print("ClawGame Tile 配置测试")
    print("=" * 50)
    print(f"Tileset: {TILESET_PATH}")
    print(f"原始尺寸: {TILE_SIZE}x{TILE_SIZE}")
    print(f"缩放倍数: {TILE_SCALE}x")
    print(f"最终尺寸: {get_scaled_size()}x{get_scaled_size()}")
    print("=" * 50)
    
    for name, tile_id in test_tiles:
        rect = get_tile_rect(tile_id)
        grid = get_tile_grid_pos(tile_id)
        print(f"{name} (ID={tile_id}):")
        print(f"  格子坐标: {grid}")
        print(f"  像素坐标: {rect}")
    
    print("\nTile 分组统计:")
    for group_name, tiles in TILE_GROUPS.items():
        print(f"  {group_name}: {len(tiles)} tiles")
