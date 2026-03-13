"""
ClawGame - UI 配置模块

对话框 UI 组件配置，支持 9-slice 缩放和中文显示。
"""

from dataclasses import dataclass
from typing import Tuple, Optional
import os

# ============================================================
# 路径配置
# ============================================================

UI_ASSETS_PATH = os.path.join("assets", "images", "ui")

# 对话框资源路径
DIALOG_BORDER_PATH = os.path.join(UI_ASSETS_PATH, "dialog_border.png")
DIALOG_BORDER_GREY_PATH = os.path.join(UI_ASSETS_PATH, "dialog_border_grey.png")
DIALOG_BORDER_DEPTH_PATH = os.path.join(UI_ASSETS_PATH, "dialog_border_depth.png")
DIALOG_BORDER_DEPTH_GREY_PATH = os.path.join(UI_ASSETS_PATH, "dialog_border_depth_grey.png")
DIALOG_ARROW_PATH = os.path.join(UI_ASSETS_PATH, "dialog_arrow.png")
DIALOG_ARROW_SMALL_PATH = os.path.join(UI_ASSETS_PATH, "dialog_arrow_small.png")


# ============================================================
# 9-Slice 边框配置
# ============================================================

@dataclass
class NineSliceConfig:
    """9-slice 边框配置"""
    # 边框图片尺寸
    image_width: int = 384
    image_height: int = 128
    
    # 9-slice 切分区域（从边缘到切分线的距离）
    # 左边框宽度
    border_left: int = 32
    # 右边框宽度
    border_right: int = 32
    # 上边框高度
    border_top: int = 32
    # 下边框高度
    border_bottom: int = 32


# 默认 9-slice 配置
DEFAULT_NINE_SLICE = NineSliceConfig()


# ============================================================
# 对话框样式配置
# ============================================================

@dataclass
class DialogStyle:
    """对话框样式配置"""
    # 背景颜色 (R, G, B, A)
    background_color: Tuple[int, int, int, int] = (255, 255, 255, 240)
    
    # 边框颜色 (R, G, B, A) - 用于 fallback 绘制
    border_color: Tuple[int, int, int, int] = (100, 100, 100, 255)
    
    # 边框宽度（像素）
    border_width: int = 2
    
    # 圆角半径（像素）
    border_radius: int = 8
    
    # 内边距（像素）
    padding_x: int = 12
    padding_y: int = 8
    
    # 文字颜色
    text_color: Tuple[int, int, int] = (40, 40, 40)
    
    # 文字阴影颜色（可选，None 表示无阴影）
    text_shadow_color: Optional[Tuple[int, int, int, int]] = (255, 255, 255, 128)
    
    # 文字阴影偏移
    text_shadow_offset: Tuple[int, int] = (1, 1)
    
    # 最小宽度
    min_width: int = 60
    
    # 最小高度
    min_height: int = 32
    
    # 最大宽度（相对于屏幕宽度的比例）
    max_width_ratio: float = 0.8
    
    # 箭头尺寸
    arrow_width: int = 12
    arrow_height: int = 8
    
    # 箭头与气泡的间距
    arrow_offset: int = 2


# ============================================================
# 预定义样式
# ============================================================

# 默认样式 - 白底灰边
STYLE_DEFAULT = DialogStyle(
    background_color=(255, 255, 255, 240),
    border_color=(100, 100, 100, 255),
    text_color=(40, 40, 40),
)

# 游戏风格 - 半透明深色
STYLE_GAME = DialogStyle(
    background_color=(30, 30, 50, 220),
    border_color=(80, 80, 120, 255),
    text_color=(255, 255, 255),
    text_shadow_color=(0, 0, 0, 128),
)

# 卡通风格 - 亮色系
STYLE_CARTOON = DialogStyle(
    background_color=(255, 250, 240, 250),
    border_color=(200, 150, 100, 255),
    text_color=(60, 40, 20),
    border_radius=12,
)

# 暗色主题
STYLE_DARK = DialogStyle(
    background_color=(40, 40, 50, 230),
    border_color=(80, 80, 100, 255),
    text_color=(220, 220, 220),
)


# ============================================================
# 字体配置
# ============================================================

@dataclass
class FontConfig:
    """字体配置"""
    # 默认字号
    default_size: int = 16
    
    # 标题字号
    title_size: int = 20
    
    # 小字号
    small_size: int = 12
    
    # 行间距（倍数）
    line_spacing: float = 1.2
    
    # 字符间距
    char_spacing: int = 0


FONT_CONFIG = FontConfig()


# ============================================================
# 动画配置
# ============================================================

@dataclass
class DialogAnimation:
    """对话框动画配置"""
    # 是否启用动画
    enabled: bool = True
    
    # 显示动画时长（秒）
    show_duration: float = 0.2
    
    # 隐藏动画时长（秒）
    hide_duration: float = 0.15
    
    # 打字机效果速度（字符/秒）
    typewriter_speed: float = 30.0
    
    # 弹跳效果幅度（像素）
    bounce_amplitude: float = 4.0
    
    # 弹跳效果弹簧常数
    bounce_spring: float = 15.0


ANIMATION_CONFIG = DialogAnimation()


# ============================================================
# 位置配置
# ============================================================

@dataclass
class DialogPosition:
    """对话框位置配置"""
    # 与 NPC 的垂直间距（像素）
    npc_offset_y: int = 24
    
    # 与屏幕顶部的最小间距
    screen_margin_top: int = 10
    
    # 与屏幕两侧的间距
    screen_margin_sides: int = 10
    
    # 默认对齐方式: 'center', 'left', 'right'
    alignment: str = 'center'


POSITION_CONFIG = DialogPosition()


# ============================================================
# 工具函数
# ============================================================

def get_dialog_border_rects(nine_slice: NineSliceConfig = None) -> dict:
    """
    获取 9-slice 边框的各个区域矩形
    
    Args:
        nine_slice: 9-slice 配置，默认使用 DEFAULT_NINE_SLICE
    
    Returns:
        包含 9 个区域的字典: {
            'top_left': (x, y, w, h),
            'top': (x, y, w, h),
            'top_right': (x, y, w, h),
            'left': (x, y, w, h),
            'center': (x, y, w, h),
            'right': (x, y, w, h),
            'bottom_left': (x, y, w, h),
            'bottom': (x, y, w, h),
            'bottom_right': (x, y, w, h),
        }
    """
    if nine_slice is None:
        nine_slice = DEFAULT_NINE_SLICE
    
    w = nine_slice.image_width
    h = nine_slice.image_height
    bl = nine_slice.border_left
    br = nine_slice.border_right
    bt = nine_slice.border_top
    bb = nine_slice.border_bottom
    
    # 中心区域尺寸
    cw = w - bl - br
    ch = h - bt - bb
    
    return {
        # 上排
        'top_left': (0, 0, bl, bt),
        'top': (bl, 0, cw, bt),
        'top_right': (w - br, 0, br, bt),
        # 中排
        'left': (0, bt, bl, ch),
        'center': (bl, bt, cw, ch),
        'right': (w - br, bt, br, ch),
        # 下排
        'bottom_left': (0, h - bb, bl, bb),
        'bottom': (bl, h - bb, cw, bb),
        'bottom_right': (w - br, h - bb, br, bb),
    }


def calculate_bubble_size(
    text_width: int,
    text_height: int,
    style: DialogStyle = None
) -> Tuple[int, int]:
    """
    计算气泡尺寸
    
    Args:
        text_width: 文本宽度
        text_height: 文本高度
        style: 对话框样式
    
    Returns:
        (气泡宽度, 气泡高度)
    """
    if style is None:
        style = STYLE_DEFAULT
    
    width = max(style.min_width, text_width + style.padding_x * 2)
    height = max(style.min_height, text_height + style.padding_y * 2)
    
    return width, height


def get_full_path(relative_path: str) -> str:
    """
    获取资源的完整路径
    
    Args:
        relative_path: 相对于项目根目录的路径
    
    Returns:
        完整路径
    """
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)
    )))
    return os.path.join(project_root, relative_path)


# ============================================================
# 导出
# ============================================================

__all__ = [
    # 路径
    'UI_ASSETS_PATH',
    'DIALOG_BORDER_PATH',
    'DIALOG_BORDER_GREY_PATH',
    'DIALOG_BORDER_DEPTH_PATH',
    'DIALOG_BORDER_DEPTH_GREY_PATH',
    'DIALOG_ARROW_PATH',
    'DIALOG_ARROW_SMALL_PATH',
    # 配置类
    'NineSliceConfig',
    'DialogStyle',
    'FontConfig',
    'DialogAnimation',
    'DialogPosition',
    # 实例
    'DEFAULT_NINE_SLICE',
    'STYLE_DEFAULT',
    'STYLE_GAME',
    'STYLE_CARTOON',
    'STYLE_DARK',
    'FONT_CONFIG',
    'ANIMATION_CONFIG',
    'POSITION_CONFIG',
    # 函数
    'get_dialog_border_rects',
    'calculate_bubble_size',
    'get_full_path',
]
