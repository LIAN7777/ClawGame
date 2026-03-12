"""
配置模块测试
"""

import pytest
from config import GameConfig


class TestGameConfig:
    """GameConfig 配置类测试"""
    
    def test_default_config_values(self):
        """测试默认配置值是否正确"""
        config = GameConfig()
        
        # 显示配置
        assert config.SCREEN_WIDTH == 800
        assert config.SCREEN_HEIGHT == 600
        assert config.SCALE_FACTOR == 2
        
        # 渲染配置
        assert config.FPS == 60
        
        # 游戏配置
        assert config.TILE_SIZE == 32
        assert config.TITLE == "ClawGame"
    
    def test_custom_config_values(self):
        """测试自定义配置值"""
        config = GameConfig(
            SCREEN_WIDTH=1024,
            SCREEN_HEIGHT=768,
            SCALE_FACTOR=4
        )
        
        assert config.SCREEN_WIDTH == 1024
        assert config.SCREEN_HEIGHT == 768
        assert config.SCALE_FACTOR == 4
    
    def test_internal_width_property(self):
        """测试内部渲染宽度计算"""
        config = GameConfig(
            SCREEN_WIDTH=800,
            SCALE_FACTOR=2
        )
        assert config.internal_width == 400
        
        # 不同缩放因子
        config.SCALE_FACTOR = 4
        assert config.internal_width == 200
    
    def test_internal_height_property(self):
        """测试内部渲染高度计算"""
        config = GameConfig(
            SCREEN_HEIGHT=600,
            SCALE_FACTOR=2
        )
        assert config.internal_height == 300
        
        # 不同缩放因子
        config.SCALE_FACTOR = 3
        assert config.internal_height == 200
    
    def test_internal_resolution_property(self):
        """测试内部渲染分辨率"""
        config = GameConfig(
            SCREEN_WIDTH=800,
            SCREEN_HEIGHT=600,
            SCALE_FACTOR=2
        )
        
        resolution = config.internal_resolution
        assert resolution == (400, 300)
        assert isinstance(resolution, tuple)
        assert len(resolution) == 2
    
    def test_screen_resolution_property(self):
        """测试窗口分辨率"""
        config = GameConfig(
            SCREEN_WIDTH=800,
            SCREEN_HEIGHT=600
        )
        
        resolution = config.screen_resolution
        assert resolution == (800, 600)
        assert isinstance(resolution, tuple)
        assert len(resolution) == 2
    
    def test_scaled_tile_size_property(self):
        """测试缩放后的 Tile 尺寸"""
        config = GameConfig(
            TILE_SIZE=32,
            SCALE_FACTOR=2
        )
        assert config.scaled_tile_size == 16
        
        # 不同缩放因子
        config.SCALE_FACTOR = 4
        assert config.scaled_tile_size == 8
    
    def test_global_config_instance(self):
        """测试全局配置实例"""
        from config import config as global_config
        
        assert isinstance(global_config, GameConfig)
        # 验证默认值
        assert global_config.SCREEN_WIDTH == 800
        assert global_config.SCREEN_HEIGHT == 600
    
    def test_config_immutability_on_instantiation(self):
        """测试配置实例化后的可修改性"""
        config = GameConfig()
        
        # 配置值应该可以被修改（因为使用的是 dataclass）
        config.SCREEN_WIDTH = 1024
        assert config.SCREEN_WIDTH == 1024
    
    def test_different_scale_factors(self):
        """测试不同缩放因子的计算"""
        test_cases = [
            (800, 600, 1, (800, 600)),   # 无缩放
            (800, 600, 2, (400, 300)),   # 2倍缩放
            (800, 600, 4, (200, 150)),   # 4倍缩放
            (1024, 768, 2, (512, 384)),  # 不同分辨率
        ]
        
        for width, height, scale, expected in test_cases:
            config = GameConfig(
                SCREEN_WIDTH=width,
                SCREEN_HEIGHT=height,
                SCALE_FACTOR=scale
            )
            assert config.internal_resolution == expected
