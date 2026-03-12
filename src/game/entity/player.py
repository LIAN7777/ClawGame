"""
ClawGame - Player 玩家类模块
主角精灵类，包含形象绘制、移动控制和碰撞检测
"""

from enum import Enum
from typing import TYPE_CHECKING, Optional, Tuple

import math
import pygame

from game.entity.entity import Entity

if TYPE_CHECKING:
    from game.camera import Camera
    from game.scene import Scene


class Direction(Enum):
    """朝向枚举"""
    DOWN = 0   # 向下（默认）
    LEFT = 1   # 向左
    RIGHT = 2  # 向右
    UP = 3     # 向上


class AnimState(Enum):
    """动画状态枚举"""
    IDLE = 0    # 闲置
    MOVE = 1    # 移动
    JUMP = 2    # 跳跃


class Player(Entity):
    """
    玩家类
    
    卡通人形小动物角色（Hello Kitty 风格）。
    支持四向移动、奔跑加速和碰撞检测。
    """
    
    # 移动参数
    WALK_SPEED: float = 100.0    # 普通速度：100 像素/秒
    RUN_SPEED: float = 180.0     # 奔跑速度：180 像素/秒
    
    # 跳跃参数
    JUMP_HEIGHT: float = 40.0    # 跳跃高度：40 像素
    JUMP_DURATION: float = 0.5   # 跳跃持续时间：0.5 秒
    
    # 动画参数
    IDLE_FLOAT_AMPLITUDE: float = 2.0  # 闲置浮动幅度
    IDLE_FLOAT_SPEED: float = 4.0      # 闲置浮动速度（周期/秒）
    MOVE_TILT_ANGLE: float = 8.0       # 移动倾斜角度
    JUMP_SQUASH: float = 0.7           # 起跳压扁比例
    JUMP_STRETCH: float = 1.2          # 空中拉伸比例
    
    # 精灵尺寸
    SPRITE_SIZE: int = 24        # 24x24 像素（小于 tile 便于移动）
    
    # 颜色配置（Hello Kitty 风格）
    BODY_COLOR = (255, 182, 193)       # 粉色身体
    EAR_COLOR = (255, 150, 170)        # 深粉色耳朵
    EYE_COLOR = (40, 40, 40)           # 深灰色眼睛
    EYE_HIGHLIGHT = (255, 255, 255)    # 眼睛高光
    CHEEK_COLOR = (255, 130, 150)      # 腮红
    SHADOW_COLOR = (50, 50, 50, 80)    # 影子颜色（半透明深灰）
    
    def __init__(self, x: float, y: float):
        """
        初始化玩家
        
        Args:
            x: 世界 X 坐标（像素）
            y: 世界 Y 坐标（像素）
        """
        # 调用父类初始化
        super().__init__(x, y, self.SPRITE_SIZE, self.SPRITE_SIZE)
        
        # 朝向（默认向下）
        self.direction: Direction = Direction.DOWN
        
        # 移动状态
        self.is_moving: bool = False
        self.is_running: bool = False
        
        # 跳跃状态
        self.is_jumping: bool = False
        self.jump_timer: float = 0.0     # 跳跃计时器
        self.jump_progress: float = 0.0  # 跳跃进度 (0.0 ~ 1.0)
        
        # 动画状态
        self.anim_state: AnimState = AnimState.IDLE
        self.anim_time: float = 0.0      # 动画时间
        
        # 当前速度（像素/秒）
        self.current_speed: float = self.WALK_SPEED
        
        # 当前场景引用（用于碰撞检测）
        self.scene: Optional['Scene'] = None
        
        # 调整碰撞盒（比精灵稍小，更宽松的碰撞）
        self.hitbox_offset_x = 4
        self.hitbox_offset_y = 6
        self.hitbox_width = self.SPRITE_SIZE - 8
        self.hitbox_height = self.SPRITE_SIZE - 10
    
    def set_scene(self, scene: 'Scene') -> None:
        """
        设置当前场景
        
        Args:
            scene: 场景对象
        """
        self.scene = scene
    
    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """
        处理输入
        
        Args:
            keys: pygame 键盘状态
        """
        # 重置速度
        self.vx = 0.0
        self.vy = 0.0
        self.is_moving = False
        
        # 检查是否奔跑（按住 Shift）
        self.is_running = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        self.current_speed = self.RUN_SPEED if self.is_running else self.WALK_SPEED
        
        # 四向移动（WASD 或方向键）
        # 上下移动
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vy = -self.current_speed
            self.direction = Direction.UP
            self.is_moving = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.vy = self.current_speed
            self.direction = Direction.DOWN
            self.is_moving = True
        
        # 左右移动
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -self.current_speed
            self.direction = Direction.LEFT
            self.is_moving = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = self.current_speed
            self.direction = Direction.RIGHT
            self.is_moving = True
        
        # 跳跃（空格键，仅在未跳跃时可以跳）
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self._start_jump()
    
    def update(self, dt: float) -> None:
        """
        更新玩家状态
        
        Args:
            dt: 时间增量（秒）
        """
        if not self.active:
            return
        
        # 更新动画时间
        self.anim_time += dt
        
        # 更新跳跃状态
        if self.is_jumping:
            self._update_jump(dt)
        
        # 更新动画状态
        self._update_anim_state()
        
        # 计算移动量
        dx = self.vx * dt
        dy = self.vy * dt
        
        # 如果有移动，进行碰撞检测
        if dx != 0 or dy != 0:
            self._move_with_collision(dx, dy)
    
    def _start_jump(self) -> None:
        """开始跳跃"""
        self.is_jumping = True
        self.jump_timer = 0.0
        self.jump_progress = 0.0
    
    def _update_jump(self, dt: float) -> None:
        """
        更新跳跃状态
        
        Args:
            dt: 时间增量（秒）
        """
        self.jump_timer += dt
        self.jump_progress = min(1.0, self.jump_timer / self.JUMP_DURATION)
        
        # 跳跃结束
        if self.jump_progress >= 1.0:
            self.is_jumping = False
            self.jump_timer = 0.0
            self.jump_progress = 0.0
    
    def _update_anim_state(self) -> None:
        """更新动画状态"""
        if self.is_jumping:
            self.anim_state = AnimState.JUMP
        elif self.is_moving:
            self.anim_state = AnimState.MOVE
        else:
            self.anim_state = AnimState.IDLE
    
    def _move_with_collision(self, dx: float, dy: float) -> None:
        """
        带碰撞检测的移动
        
        Args:
            dx: X 方向移动量
            dy: Y 方向移动量
        """
        # 分别检测 X 和 Y 方向的碰撞
        # 先尝试 X 方向移动
        if dx != 0:
            new_x = self.x + dx
            if self._can_move_to(new_x, self.y):
                self.x = new_x
            else:
                # X 方向碰到障碍，尝试滑动（贴墙）
                pass
        
        # 再尝试 Y 方向移动
        if dy != 0:
            new_y = self.y + dy
            if self._can_move_to(self.x, new_y):
                self.y = new_y
            else:
                # Y 方向碰到障碍，尝试滑动（贴墙）
                pass
    
    def _can_move_to(self, new_x: float, new_y: float) -> bool:
        """
        检测是否可以移动到指定位置
        
        Args:
            new_x: 新的 X 坐标
            new_y: 新的 Y 坐标
            
        Returns:
            是否可以移动
        """
        if self.scene is None:
            return True
        
        # 创建新的碰撞盒
        new_hitbox = pygame.Rect(
            int(new_x + self.hitbox_offset_x),
            int(new_y + self.hitbox_offset_y),
            self.hitbox_width,
            self.hitbox_height
        )
        
        # 获取碰撞盒覆盖的所有 tile
        tile_size = self.scene.tile_size
        start_x = max(0, new_hitbox.left // tile_size)
        start_y = max(0, new_hitbox.top // tile_size)
        end_x = min(self.scene.tilemap.width, (new_hitbox.right // tile_size) + 1)
        end_y = min(self.scene.tilemap.height, (new_hitbox.bottom // tile_size) + 1)
        
        # 检查每个 tile
        for grid_y in range(start_y, end_y):
            for grid_x in range(start_x, end_x):
                tile = self.scene.tilemap.get_tile(grid_x, grid_y)
                if tile is None:
                    continue
                
                # 墙壁和家具不可通行
                if tile.tile_type in (11, 14, 16):  # WALL, TABLE, BED
                    # 获取 tile 的矩形区域
                    tile_rect = pygame.Rect(
                        grid_x * tile_size,
                        grid_y * tile_size,
                        tile_size,
                        tile_size
                    )
                    
                    # 检测碰撞
                    if new_hitbox.colliderect(tile_rect):
                        return False
        
        return True
    
    def render(
        self, 
        surface: pygame.Surface, 
        camera: Optional['Camera'] = None
    ) -> None:
        """
        渲染玩家精灵
        
        绘制卡通人形小动物形象，包含影子和动画效果。
        
        Args:
            surface: 目标渲染表面
            camera: 相机对象
        """
        if not self.visible:
            return
        
        # 获取屏幕坐标
        screen_x, screen_y = self._get_screen_position(camera)
        
        # 计算跳跃时的 Y 偏移（抛物线）
        jump_offset_y = 0.0
        if self.is_jumping:
            # 使用抛物线计算高度：h = 4 * p * (1 - p)
            p = self.jump_progress
            jump_offset_y = self.JUMP_HEIGHT * 4 * p * (1 - p)
        
        # 绘制影子（在玩家脚下）
        self._draw_shadow(surface, screen_x, screen_y, jump_offset_y)
        
        # 绘制玩家精灵（带动画效果）
        self._draw_sprite(surface, screen_x, screen_y - int(jump_offset_y))
    
    def _draw_sprite(
        self, 
        surface: pygame.Surface, 
        x: int, 
        y: int
    ) -> None:
        """
        绘制玩家精灵
        
        绘制卡通人形小动物（椭圆身体 + 小耳朵 + 眼睛）。
        根据动画状态应用变换效果。
        
        Args:
            surface: 目标渲染表面
            x: 屏幕 X 坐标
            y: 屏幕 Y 坐标
        """
        # 计算动画偏移和缩放
        offset_y = 0.0
        scale_x = 1.0
        scale_y = 1.0
        tilt_angle = 0.0
        
        if self.anim_state == AnimState.IDLE:
            # 闲置：轻微上下浮动（呼吸效果）
            offset_y = math.sin(self.anim_time * self.IDLE_FLOAT_SPEED * 2 * math.pi) * self.IDLE_FLOAT_AMPLITUDE
        
        elif self.anim_state == AnimState.MOVE:
            # 移动：轻微倾斜
            if self.direction == Direction.LEFT:
                tilt_angle = -self.MOVE_TILT_ANGLE
            elif self.direction == Direction.RIGHT:
                tilt_angle = self.MOVE_TILT_ANGLE
            elif self.direction == Direction.UP:
                scale_y = 1.05  # 向上移动时略微拉伸
            else:
                scale_y = 0.95  # 向下移动时略微压扁
        
        elif self.anim_state == AnimState.JUMP:
            # 跳跃：压扁和拉伸效果
            p = self.jump_progress
            if p < 0.15:
                # 起跳准备阶段：压扁
                squash_factor = p / 0.15
                scale_y = 1.0 - (1.0 - self.JUMP_SQUASH) * squash_factor
                scale_x = 1.0 + (1.0 - self.JUMP_SQUASH) * squash_factor * 0.5
            elif p < 0.85:
                # 空中阶段：拉伸
                stretch_factor = min(1.0, (p - 0.15) / 0.35)
                scale_y = self.JUMP_SQUASH + (self.JUMP_STRETCH - self.JUMP_SQUASH) * stretch_factor
                scale_x = 1.0 - (scale_y - 1.0) * 0.3
            else:
                # 落地阶段：恢复正常
                recover_factor = (p - 0.85) / 0.15
                scale_y = self.JUMP_STRETCH - (self.JUMP_STRETCH - 1.0) * recover_factor
                scale_x = 1.0 + (scale_y - 1.0) * 0.3
        
        # 应用 Y 偏移
        y = int(y + offset_y)
        
        # 中心点
        center_x = x + self.SPRITE_SIZE // 2
        center_y = y + self.SPRITE_SIZE // 2
        
        # === 绘制身体（椭圆）===
        body_width = int(20 * scale_x)
        body_height = int(18 * scale_y)
        body_rect = pygame.Rect(
            center_x - body_width // 2,
            center_y - body_height // 2,
            body_width,
            body_height
        )
        pygame.draw.ellipse(surface, self.BODY_COLOR, body_rect)
        
        # === 绘制耳朵（根据朝向调整）===
        ear_width = int(5 * scale_x)
        ear_height = int(6 * scale_y)
        
        if self.direction == Direction.UP:
            # 向上时显示背面，耳朵在下方
            ear_y = center_y + body_height // 4
            pygame.draw.ellipse(
                surface, 
                self.EAR_COLOR,
                pygame.Rect(center_x - body_width // 3, ear_y, ear_width, ear_height)
            )
            pygame.draw.ellipse(
                surface, 
                self.EAR_COLOR,
                pygame.Rect(center_x + body_width // 6, ear_y, ear_width, ear_height)
            )
        else:
            # 其他方向，耳朵在上方
            ear_y = center_y - body_height // 2 - ear_height // 2
            # 左耳
            pygame.draw.ellipse(
                surface, 
                self.EAR_COLOR,
                pygame.Rect(center_x - body_width // 3, ear_y, ear_width, ear_height)
            )
            # 右耳
            pygame.draw.ellipse(
                surface, 
                self.EAR_COLOR,
                pygame.Rect(center_x + body_width // 6, ear_y, ear_width, ear_height)
            )
        
        # === 绘制眼睛（根据朝向调整）===
        eye_y = center_y - 2
        eye_spacing = int(6 * scale_x)
        
        if self.direction == Direction.LEFT:
            # 向左看
            self._draw_eye(surface, center_x - eye_spacing, eye_y, look_left=True)
            self._draw_eye(surface, center_x, eye_y, look_left=True)
        elif self.direction == Direction.RIGHT:
            # 向右看
            self._draw_eye(surface, center_x, eye_y, look_left=False)
            self._draw_eye(surface, center_x + eye_spacing, eye_y, look_left=False)
        elif self.direction == Direction.UP:
            # 向上看，眼睛位置上移
            self._draw_eye(surface, center_x - eye_spacing // 2, eye_y - 3)
            self._draw_eye(surface, center_x + eye_spacing // 2, eye_y - 3)
        else:
            # 向下（默认）
            self._draw_eye(surface, center_x - 3, eye_y)
            self._draw_eye(surface, center_x + 3, eye_y)
        
        # === 绘制腮红 ===
        cheek_y = center_y + 4
        pygame.draw.circle(
            surface, 
            self.CHEEK_COLOR,
            (center_x - body_width // 3, cheek_y),
            2
        )
        pygame.draw.circle(
            surface, 
            self.CHEEK_COLOR,
            (center_x + body_width // 3, cheek_y),
            2
        )
    
    def _draw_shadow(
        self, 
        surface: pygame.Surface, 
        x: int, 
        y: int,
        jump_height: float
    ) -> None:
        """
        绘制玩家影子
        
        跳跃时影子缩小，模拟高度感。
        
        Args:
            surface: 目标渲染表面
            x: 屏幕 X 坐标
            y: 屏幕 Y 坐标（玩家脚部位置）
            jump_height: 当前跳跃高度
        """
        # 影子大小根据跳跃高度缩放
        base_size = self.SPRITE_SIZE - 4
        if jump_height > 0:
            # 跳跃时影子缩小
            scale = 1.0 - (jump_height / self.JUMP_HEIGHT) * 0.5
            shadow_width = int(base_size * scale)
            shadow_height = int(6 * scale)
        else:
            shadow_width = base_size
            shadow_height = 6
        
        # 影子透明度（跳跃时更淡）
        alpha = int(80 - jump_height * 1.5)
        alpha = max(20, min(80, alpha))
        
        # 创建影子表面
        shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
        shadow_color = (50, 50, 50, alpha)
        pygame.draw.ellipse(shadow_surface, shadow_color, (0, 0, shadow_width, shadow_height))
        
        # 绘制影子（在脚部位置）
        shadow_x = x + (self.SPRITE_SIZE - shadow_width) // 2
        shadow_y = y + self.SPRITE_SIZE - 4
        surface.blit(shadow_surface, (shadow_x, shadow_y))
    
    def _draw_eye(
        self, 
        surface: pygame.Surface, 
        x: int, 
        y: int,
        look_left: Optional[bool] = None
    ) -> None:
        """
        绘制单只眼睛
        
        Args:
            surface: 目标渲染表面
            x: 眼睛 X 坐标
            y: 眼睛 Y 坐标
            look_left: 是否向左看，None 表示中间
        """
        # 眼白
        pygame.draw.circle(surface, self.EYE_HIGHLIGHT, (x, y), 2)
        
        # 眼珠
        pupil_offset_x = -1 if look_left else (1 if look_left is False else 0)
        pygame.draw.circle(
            surface, 
            self.EYE_COLOR,
            (x + pupil_offset_x, y),
            1
        )
    
    def get_speed_text(self) -> str:
        """
        获取当前速度描述
        
        Returns:
            速度描述文本
        """
        return "奔跑中" if self.is_running else "行走中"
    
    def get_direction_text(self) -> str:
        """
        获取当前朝向描述
        
        Returns:
            朝向描述文本
        """
        direction_names = {
            Direction.UP: "上",
            Direction.DOWN: "下",
            Direction.LEFT: "左",
            Direction.RIGHT: "右"
        }
        return direction_names.get(self.direction, "未知")
    
    def __repr__(self) -> str:
        """字符串表示"""
        return (
            f"Player(x={self.x:.1f}, y={self.y:.1f}, "
            f"dir={self.direction.name}, speed={self.current_speed:.0f})"
        )
