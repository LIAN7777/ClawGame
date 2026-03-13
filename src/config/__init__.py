"""
ClawGame 配置模块
"""

from .game_config import GameConfig, config
from .tiles import (
    TileID,
    TILESET_PATH,
    TILE_SIZE,
    TILE_SCALE,
    TILESET_COLS,
    TILESET_ROWS,
    TILE_GROUPS,
    get_tile_rect,
    get_tile_grid_pos,
    get_tile_id,
    get_scaled_size,
    is_valid_tile_id,
    get_tiles_by_group,
)
from .ui import (
    # 路径
    UI_ASSETS_PATH,
    DIALOG_BORDER_PATH,
    DIALOG_BORDER_GREY_PATH,
    DIALOG_BORDER_DEPTH_PATH,
    DIALOG_BORDER_DEPTH_GREY_PATH,
    DIALOG_ARROW_PATH,
    DIALOG_ARROW_SMALL_PATH,
    # 配置类
    NineSliceConfig,
    DialogStyle,
    FontConfig,
    DialogAnimation,
    DialogPosition,
    # 实例
    DEFAULT_NINE_SLICE,
    STYLE_DEFAULT,
    STYLE_GAME,
    STYLE_CARTOON,
    STYLE_DARK,
    FONT_CONFIG,
    ANIMATION_CONFIG,
    POSITION_CONFIG,
    # 函数
    get_dialog_border_rects,
    calculate_bubble_size,
    get_full_path,
)

__all__ = [
    # 游戏配置
    'GameConfig',
    'config',
    # Tile 配置
    'TileID',
    'TILESET_PATH',
    'TILE_SIZE',
    'TILE_SCALE',
    'TILESET_COLS',
    'TILESET_ROWS',
    'TILE_GROUPS',
    'get_tile_rect',
    'get_tile_grid_pos',
    'get_tile_id',
    'get_scaled_size',
    'is_valid_tile_id',
    'get_tiles_by_group',
    # UI 配置
    'UI_ASSETS_PATH',
    'DIALOG_BORDER_PATH',
    'DIALOG_BORDER_GREY_PATH',
    'DIALOG_BORDER_DEPTH_PATH',
    'DIALOG_BORDER_DEPTH_GREY_PATH',
    'DIALOG_ARROW_PATH',
    'DIALOG_ARROW_SMALL_PATH',
    'NineSliceConfig',
    'DialogStyle',
    'FontConfig',
    'DialogAnimation',
    'DialogPosition',
    'DEFAULT_NINE_SLICE',
    'STYLE_DEFAULT',
    'STYLE_GAME',
    'STYLE_CARTOON',
    'STYLE_DARK',
    'FONT_CONFIG',
    'ANIMATION_CONFIG',
    'POSITION_CONFIG',
    'get_dialog_border_rects',
    'calculate_bubble_size',
    'get_full_path',
]
