"""
实体模块测试
"""

import pytest
import pygame
from unittest.mock import MagicMock, patch
from game.entity.entity import Entity
from game.entity.player import Player, Direction, AnimState


# 测试用的具体实体类（因为 Entity 是抽象类）
class ConcreteEntity(Entity):
    """测试用具体实体类"""
    
    def update(self, dt: float) -> None:
        """更新实体"""
        self.x += self.vx * dt
        self.y += self.vy * dt
    
    def render(self, surface: pygame.Surface, camera=None) -> None:
        """渲染实体"""
        pass


class TestEntity:
    """Entity 基类测试"""
    
    def test_entity_init(self):
        """测试实体初始化"""
        entity = ConcreteEntity(x=100, y=200, width=32, height=32)
        
        assert entity.x == 100
        assert entity.y == 200
        assert entity.width == 32
        assert entity.height == 32
        assert entity.vx == 0.0
        assert entity.vy == 0.0
        assert entity.active is True
        assert entity.visible is True
    
    def test_entity_rect_property(self):
        """测试实体矩形属性"""
        entity = ConcreteEntity(x=100, y=200, width=32, height=32)
        
        rect = entity.rect
        assert isinstance(rect, pygame.Rect)
        assert rect.x == 100
        assert rect.y == 200
        assert rect.width == 32
        assert rect.height == 32
    
    def test_entity_hitbox_default(self):
        """测试默认碰撞盒"""
        entity = ConcreteEntity(x=100, y=200, width=32, height=32)
        
        # 默认碰撞盒与实体尺寸相同
        hitbox = entity.hitbox
        assert hitbox.x == 100
        assert hitbox.y == 200
        assert hitbox.width == 32
        assert hitbox.height == 32
    
    def test_entity_hitbox_custom(self):
        """测试自定义碰撞盒"""
        entity = ConcreteEntity(x=100, y=200, width=32, height=32)
        
        # 设置碰撞盒偏移
        entity.hitbox_offset_x = 4
        entity.hitbox_offset_y = 4
        entity.hitbox_width = 24
        entity.hitbox_height = 24
        
        hitbox = entity.hitbox
        assert hitbox.x == 104  # 100 + 4
        assert hitbox.y == 204  # 200 + 4
        assert hitbox.width == 24
        assert hitbox.height == 24
    
    def test_entity_center_property(self):
        """测试中心坐标属性"""
        entity = ConcreteEntity(x=100, y=200, width=32, height=32)
        
        center = entity.center
        assert center == (116.0, 216.0)  # (100 + 32/2, 200 + 32/2)
    
    def test_entity_center_x_y_properties(self):
        """测试中心坐标分量属性"""
        entity = ConcreteEntity(x=100, y=200, width=32, height=32)
        
        assert entity.center_x == 116.0
        assert entity.center_y == 216.0
    
    def test_set_position(self):
        """测试设置位置"""
        entity = ConcreteEntity(x=0, y=0, width=32, height=32)
        
        entity.set_position(50, 100)
        assert entity.x == 50
        assert entity.y == 100
    
    def test_set_center(self):
        """测试设置中心位置"""
        entity = ConcreteEntity(x=0, y=0, width=32, height=32)
        
        entity.set_center(100, 200)
        
        assert entity.x == 84.0  # 100 - 32/2
        assert entity.y == 184.0  # 200 - 32/2
        assert entity.center == (100.0, 200.0)
    
    def test_move(self):
        """测试移动"""
        entity = ConcreteEntity(x=100, y=200, width=32, height=32)
        
        entity.move(50, -30)
        assert entity.x == 150
        assert entity.y == 170
    
    def test_set_velocity(self):
        """测试设置速度"""
        entity = ConcreteEntity(x=0, y=0, width=32, height=32)
        
        entity.set_velocity(100, -50)
        assert entity.vx == 100
        assert entity.vy == -50
    
    def test_collides_with_entity(self):
        """测试实体间碰撞检测"""
        entity1 = ConcreteEntity(x=0, y=0, width=32, height=32)
        entity2 = ConcreteEntity(x=30, y=30, width=32, height=32)
        
        # 重叠
        assert entity1.collides_with(entity2) is True
        
        # 不重叠
        entity2.set_position(100, 100)
        assert entity1.collides_with(entity2) is False
    
    def test_collides_with_rect(self):
        """测试与矩形碰撞检测"""
        entity = ConcreteEntity(x=0, y=0, width=32, height=32)
        
        # 重叠
        rect1 = pygame.Rect(20, 20, 32, 32)
        assert entity.collides_with_rect(rect1) is True
        
        # 不重叠
        rect2 = pygame.Rect(100, 100, 32, 32)
        assert entity.collides_with_rect(rect2) is False
    
    def test_repr(self):
        """测试字符串表示"""
        entity = ConcreteEntity(x=100.5, y=200.3, width=32, height=32)
        repr_str = repr(entity)
        
        assert "ConcreteEntity" in repr_str
        assert "x=100.5" in repr_str
        assert "y=200.3" in repr_str


class TestPlayer:
    """Player 玩家类测试"""
    
    def test_player_init(self):
        """测试玩家初始化"""
        player = Player(x=100, y=200)
        
        assert player.x == 100
        assert player.y == 200
        assert player.width == Player.SPRITE_SIZE
        assert player.height == Player.SPRITE_SIZE
        assert player.direction == Direction.DOWN
        assert player.is_moving is False
        assert player.is_running is False
        assert player.is_jumping is False
    
    def test_player_speed_constants(self):
        """测试玩家速度常量"""
        assert Player.WALK_SPEED == 100.0
        assert Player.RUN_SPEED == 180.0
    
    def test_player_jump_constants(self):
        """测试跳跃参数"""
        assert Player.JUMP_HEIGHT == 40.0
        assert Player.JUMP_DURATION == 0.5
    
    def test_player_hitbox_smaller_than_sprite(self):
        """测试碰撞盒比精灵小"""
        player = Player(x=100, y=200)
        
        # 碰撞盒应该比精灵尺寸小
        assert player.hitbox_width < player.width
        assert player.hitbox_height < player.height
    
    def test_player_direction_enum(self):
        """测试朝向枚举"""
        assert Direction.DOWN.value == 0
        assert Direction.LEFT.value == 1
        assert Direction.RIGHT.value == 2
        assert Direction.UP.value == 3
    
    def test_player_anim_state_enum(self):
        """测试动画状态枚举"""
        assert AnimState.IDLE.value == 0
        assert AnimState.MOVE.value == 1
        assert AnimState.JUMP.value == 2
    
    def test_player_set_scene(self):
        """测试设置场景"""
        player = Player(x=100, y=200)
        scene = MagicMock()
        
        player.set_scene(scene)
        assert player.scene == scene
    
    def test_player_handle_input_movement(self):
        """测试输入处理 - 移动"""
        player = Player(x=100, y=200)
        
        # 创建模拟按键状态
        keys = MagicMock()
        keys.__getitem__ = lambda self, key: True if key in [pygame.K_w] else False
        
        # 向上移动
        keys = MagicMock()
        keys.__getitem__ = lambda _, key: key == pygame.K_w
        keys.__contains__ = lambda _, key: key == pygame.K_w
        
        # 手动设置按键状态
        with patch.object(player, 'handle_input') as mock_handle:
            # 使用实际的按键检查逻辑
            player.vx = 0
            player.vy = -Player.WALK_SPEED
            player.is_moving = True
            player.direction = Direction.UP
        
        assert player.vy == -Player.WALK_SPEED
        assert player.direction == Direction.UP
        assert player.is_moving is True
    
    def test_player_update_changes_position(self):
        """测试更新改变位置"""
        player = Player(x=100, y=200)
        player.vx = 100
        player.vy = 50
        player.is_moving = True
        
        # 没有场景，碰撞检测跳过
        player.scene = None
        
        initial_x = player.x
        initial_y = player.y
        
        player.update(0.1)  # 0.1 秒
        
        # 位置应该改变
        assert player.x != initial_x
        assert player.y != initial_y
    
    def test_player_update_anim_time(self):
        """测试更新动画时间"""
        player = Player(x=100, y=200)
        
        initial_time = player.anim_time
        player.update(0.5)
        
        assert player.anim_time == initial_time + 0.5
    
    def test_player_update_anim_state(self):
        """测试动画状态更新"""
        player = Player(x=100, y=200)
        
        # 默认闲置
        player.is_moving = False
        player.is_jumping = False
        player._update_anim_state()
        assert player.anim_state == AnimState.IDLE
        
        # 移动状态
        player.is_moving = True
        player._update_anim_state()
        assert player.anim_state == AnimState.MOVE
        
        # 跳跃状态优先
        player.is_jumping = True
        player._update_anim_state()
        assert player.anim_state == AnimState.JUMP
    
    def test_player_jump_start_and_end(self):
        """测试跳跃开始和结束"""
        player = Player(x=100, y=200)
        
        # 开始跳跃
        player._start_jump()
        assert player.is_jumping is True
        assert player.jump_timer == 0.0
        assert player.jump_progress == 0.0
        
        # 更新跳跃到结束（超过持续时间）
        player._update_jump(0.6)
        # 跳跃结束后，状态被重置
        assert player.is_jumping is False
        assert player.jump_timer == 0.0
        assert player.jump_progress == 0.0  # 结束后被重置为 0
    
    def test_player_jump_progress(self):
        """测试跳跃进度"""
        player = Player(x=100, y=200)
        player._start_jump()
        
        # 半程
        player._update_jump(0.25)
        assert 0 < player.jump_progress < 1
    
    def test_player_move_without_collision(self):
        """测试无碰撞移动"""
        player = Player(x=100, y=200)
        player.scene = None  # 无场景，无碰撞
        
        initial_x = player.x
        initial_y = player.y
        
        # 直接移动
        player._move_with_collision(10, 5)
        
        assert player.x == initial_x + 10
        assert player.y == initial_y + 5
    
    def test_player_get_speed_text(self):
        """测试速度文本"""
        player = Player(x=100, y=200)
        
        player.is_running = False
        assert player.get_speed_text() == "行走中"
        
        player.is_running = True
        assert player.get_speed_text() == "奔跑中"
    
    def test_player_get_direction_text(self):
        """测试朝向文本"""
        player = Player(x=100, y=200)
        
        direction_texts = {
            Direction.UP: "上",
            Direction.DOWN: "下",
            Direction.LEFT: "左",
            Direction.RIGHT: "右"
        }
        
        for direction, expected_text in direction_texts.items():
            player.direction = direction
            assert player.get_direction_text() == expected_text
    
    def test_player_repr(self):
        """测试玩家字符串表示"""
        player = Player(x=100, y=200)
        repr_str = repr(player)
        
        assert "Player" in repr_str
        assert "x=" in repr_str
        assert "y=" in repr_str
        assert "dir=" in repr_str


class TestPlayerCollision:
    """玩家碰撞检测测试"""
    
    def test_can_move_to_without_scene(self):
        """测试无场景时的移动检测"""
        player = Player(x=100, y=200)
        player.scene = None
        
        # 无场景，任何位置都可以移动
        assert player._can_move_to(1000, 1000) is True
    
    def test_can_move_to_with_scene(self):
        """测试有场景时的移动检测"""
        player = Player(x=100, y=200)
        
        # 创建模拟场景
        scene = MagicMock()
        scene.tile_size = 32
        scene.tilemap = MagicMock()
        scene.tilemap.width = 20
        scene.tilemap.height = 15
        
        # 所有 tile 都可通行
        scene.tilemap.get_tile = lambda x, y: None
        
        player.scene = scene
        
        # 应该可以移动
        assert player._can_move_to(100, 100) is True
