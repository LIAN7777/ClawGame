"""
ClawGame - 游戏配置模块
定义游戏的核心配置参数
"""

from dataclasses import dataclass


@dataclass
class GameConfig:
    """
    游戏配置类
    
    使用数据类封装所有游戏配置参数，便于管理和修改。
    支持缩放渲染：内部渲染较小分辨率，然后放大显示。
    """
    
    # === 显示配置 ===
    # 窗口分辨率（实际显示大小）
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    
    # 缩放倍数（内部渲染分辨率 = 窗口分辨率 / 缩放倍数）
    SCALE_FACTOR: int = 2
    
    # === 渲染配置 ===
    # 帧率
    FPS: int = 60
    
    # === 游戏配置 ===
    # Tile 尺寸（像素）
    TILE_SIZE: int = 32
    
    # 游戏标题
    TITLE: str = "ClawGame"
    
    @property
    def internal_width(self) -> int:
        """内部渲染宽度"""
        return self.SCREEN_WIDTH // self.SCALE_FACTOR
    
    @property
    def internal_height(self) -> int:
        """内部渲染高度"""
        return self.SCREEN_HEIGHT // self.SCALE_FACTOR
    
    @property
    def internal_resolution(self) -> tuple[int, int]:
        """内部渲染分辨率 (宽, 高)"""
        return (self.internal_width, self.internal_height)
    
    @property
    def screen_resolution(self) -> tuple[int, int]:
        """窗口分辨率 (宽, 高)"""
        return (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
    
    @property
    def scaled_tile_size(self) -> int:
        """缩放后的 Tile 尺寸（用于内部渲染）"""
        return self.TILE_SIZE // self.SCALE_FACTOR


# 全局配置实例
config = GameConfig()
