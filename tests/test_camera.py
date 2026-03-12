"""
相机模块测试
"""

import pytest
import pygame
from game.camera import Camera


class TestCamera:
    """Camera 类测试"""
    
    def test_camera_init(self):
        """测试相机初始化"""
        camera = Camera(width=400, height=300)
        
        assert camera.width == 400
        assert camera.height == 300
        assert camera.x == 0
        assert camera.y == 0
        assert camera.world_width is None
        assert camera.world_height is None
    
    def test_camera_init_with_world_bounds(self):
        """测试带世界边界的相机初始化"""
        camera = Camera(
            width=400, 
            height=300,
            world_width=1600,
            world_height=1200
        )
        
        assert camera.world_width == 1600
        assert camera.world_height == 1200
    
    def test_camera_rect_property(self):
        """测试相机矩形区域"""
        camera = Camera(width=400, height=300)
        camera.x = 100
        camera.y = 200
        
        rect = camera.rect
        assert rect.x == 100
        assert rect.y == 200
        assert rect.width == 400
        assert rect.height == 300
    
    def test_camera_center_property(self):
        """测试相机中心点"""
        camera = Camera(width=400, height=300)
        camera.x = 100
        camera.y = 200
        
        center = camera.center
        assert center == (300.0, 350.0)  # (100 + 400/2, 200 + 300/2)
    
    def test_follow_direct(self):
        """测试直接跟随"""
        camera = Camera(width=400, height=300)
        target = pygame.Rect(500, 400, 32, 32)
        
        camera.follow(target, smooth=False)
        assert camera._target is not None
        assert camera.smooth is False
        
        camera.update()
        
        # 相机应该以目标为中心
        expected_x = 500 + 16 - 200  # target.centerx - width/2
        expected_y = 400 + 16 - 150  # target.centery - height/2
        
        assert abs(camera.x - expected_x) < 0.01
        assert abs(camera.y - expected_y) < 0.01
    
    def test_follow_smooth(self):
        """测试平滑跟随"""
        camera = Camera(width=400, height=300)
        target = pygame.Rect(500, 400, 32, 32)
        
        camera.follow(target, smooth=True)
        assert camera.smooth is True
        assert camera.smooth_speed == 0.1
        
        # 初始位置
        camera.x = 0
        camera.y = 0
        
        # 第一次更新，应该向目标移动但不到达
        camera.update()
        assert camera.x > 0  # 向目标移动
        assert camera.y > 0
        
        # 不是直接到达
        expected_x = 500 + 16 - 200
        assert camera.x < expected_x  # 平滑插值，未完全到达
    
    def test_unfollow(self):
        """测试取消跟随"""
        camera = Camera(width=400, height=300)
        target = pygame.Rect(500, 400, 32, 32)
        
        camera.follow(target)
        assert camera._target is not None
        
        camera.unfollow()
        assert camera._target is None
    
    def test_boundary_left_top(self):
        """测试左上边界限制"""
        camera = Camera(
            width=400, 
            height=300,
            world_width=1600,
            world_height=1200
        )
        
        # 尝试移动到负坐标
        camera.set_position(-100, -100)
        
        # 应该被限制到 0
        assert camera.x == 0
        assert camera.y == 0
    
    def test_boundary_right_bottom(self):
        """测试右下边界限制"""
        camera = Camera(
            width=400, 
            height=300,
            world_width=1600,
            world_height=1200
        )
        
        # 尝试移动超出世界边界
        camera.set_position(1500, 1200)
        
        # 应该被限制
        assert camera.x == 1200  # world_width - camera_width = 1600 - 400
        assert camera.y == 900   # world_height - camera_height = 1200 - 300
    
    def test_boundary_no_world_size(self):
        """测试无世界边界时的行为"""
        camera = Camera(width=400, height=300)
        
        # 无世界边界时，左上边界仍然生效
        camera.set_position(-100, -100)
        assert camera.x == 0
        assert camera.y == 0
        
        # 右下边界不生效
        camera.set_position(10000, 10000)
        assert camera.x == 10000
        assert camera.y == 10000
    
    def test_apply_entity(self):
        """测试坐标转换 - 实体"""
        camera = Camera(width=400, height=300)
        camera.x = 100
        camera.y = 200
        
        entity_rect = pygame.Rect(300, 400, 32, 32)
        screen_rect = camera.apply(entity_rect)
        
        assert screen_rect.x == 200  # 300 - 100
        assert screen_rect.y == 200  # 400 - 200
        assert screen_rect.width == 32
        assert screen_rect.height == 32
    
    def test_apply_point(self):
        """测试坐标转换 - 点"""
        camera = Camera(width=400, height=300)
        camera.x = 100
        camera.y = 200
        
        # 世界坐标转屏幕坐标
        screen_point = camera.apply_point((300, 400))
        assert screen_point == (200.0, 200.0)
    
    def test_screen_to_world(self):
        """测试屏幕坐标转世界坐标"""
        camera = Camera(width=400, height=300)
        camera.x = 100
        camera.y = 200
        
        # 屏幕坐标转世界坐标
        world_point = camera.screen_to_world((200, 200))
        assert world_point == (300.0, 400.0)
    
    def test_coordinate_conversion_roundtrip(self):
        """测试坐标转换往返"""
        camera = Camera(width=400, height=300)
        camera.x = 100
        camera.y = 200
        
        # 世界 -> 屏幕 -> 世界
        world_point = (500, 600)
        screen_point = camera.apply_point(world_point)
        back_to_world = camera.screen_to_world(screen_point)
        
        assert back_to_world == world_point
    
    def test_is_visible(self):
        """测试实体可见性检测"""
        camera = Camera(width=400, height=300)
        camera.x = 100
        camera.y = 200
        
        # 可见实体（在视口内）
        visible_rect = pygame.Rect(150, 250, 32, 32)
        assert camera.is_visible(visible_rect) is True
        
        # 不可见实体（在视口外）
        invisible_rect = pygame.Rect(1000, 1000, 32, 32)
        assert camera.is_visible(invisible_rect) is False
        
        # 部分可见实体（边缘相交）
        edge_rect = pygame.Rect(450, 350, 32, 32)  # 刚好在视口右边
        # 这个矩形刚好在相机右边，相机 rect 是 (100, 200, 400, 300)
        # 右边界是 500，edge_rect 左边是 450，应该可见
        assert camera.is_visible(edge_rect) is True
    
    def test_move(self):
        """测试手动移动相机"""
        camera = Camera(width=400, height=300)
        
        camera.move(50, 100)
        assert camera.x == 50
        assert camera.y == 100
        
        camera.move(-30, -40)
        assert camera.x == 20
        assert camera.y == 60
    
    def test_move_with_bounds(self):
        """测试带边界限制的移动"""
        camera = Camera(
            width=400, 
            height=300,
            world_width=800,
            world_height=600
        )
        
        # 向右移动超出边界
        camera.move(500, 0)
        assert camera.x == 400  # 被限制到 800 - 400 = 400
        
        # 向左移动超出边界
        camera.set_position(100, 0)
        camera.move(-200, 0)
        assert camera.x == 0  # 被限制到 0
    
    def test_set_position(self):
        """测试设置相机位置"""
        camera = Camera(width=400, height=300)
        
        camera.set_position(123, 456)
        assert camera.x == 123
        assert camera.y == 456
    
    def test_set_center(self):
        """测试设置相机中心位置"""
        camera = Camera(width=400, height=300)
        
        camera.set_center(400, 300)
        
        # 相机中心应该是 (400, 300)
        assert camera.x == 200  # 400 - 400/2
        assert camera.y == 150  # 300 - 300/2
        
        # 验证 center 属性
        assert camera.center == (400.0, 300.0)
    
    def test_update_without_target(self):
        """测试无目标时的更新"""
        camera = Camera(width=400, height=300)
        camera.x = 100
        camera.y = 200
        
        # 无目标，位置不变
        camera.update()
        assert camera.x == 100
        assert camera.y == 200
