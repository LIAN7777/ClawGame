"""
ClawGame - NPC 类模块
非玩家角色类，继承自 Entity
"""

from enum import Enum
from typing import TYPE_CHECKING, Optional, Tuple, Dict

import math
import os
import pygame

from game.entity.entity import Entity
from config.ui import (
    NineSliceConfig,
    DialogStyle,
    STYLE_DEFAULT,
    STYLE_GAME,
    DEFAULT_NINE_SLICE,
    DIALOG_BORDER_PATH,
    DIALOG_BORDER_GREY_PATH,
    DIALOG_BORDER_DEPTH_PATH,
    DIALOG_ARROW_PATH,
    get_full_path,
)

if TYPE_CHECKING:
    from game.camera import Camera

# 字体文件相对路径（相对于项目根目录）
_FONT_RELATIVE_PATHS = {
    # 项目本地字体（优先）
    'press_start_2p': "assets/fonts/PressStart2P-Regular.ttf",
    'noto_cjk': "assets/fonts/NotoSansCJK-Bold.ttc",
    'vonwaon_12': "assets/fonts/VonwaonBitmap-12px.ttf",
    'vonwaon_16': "assets/fonts/VonwaonBitmap-16px.ttf",
    # 系统字体（备用）
    'noto_cjk_system': "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
}

# 字体缓存
_font_cache: dict = {}


def _get_chinese_font(size: int) -> pygame.font.Font:
    """
    获取支持中文的字体
    
    优先级：
    1. VonwaonBitmap（像素位图字体，适合游戏）
    2. 项目本地字体：Noto Sans CJK（中文）
    3. 系统字体：Noto Sans CJK, 微软雅黑等
    4. 回退：默认字体
    
    Args:
        size: 字体大小
    
    Returns:
        pygame.font.Font: 字体对象
    """
    # 检查缓存
    cache_key = f"chinese_{size}"
    if cache_key in _font_cache:
        return _font_cache[cache_key]
    
    font = None
    
    # 1. 优先使用 VonwaonBitmap（像素位图字体）
    # 根据大小选择合适的版本
    if size <= 12:
        vonwaon_key = 'vonwaon_12'
    else:
        vonwaon_key = 'vonwaon_16'
    
    vonwaon_rel = _FONT_RELATIVE_PATHS.get(vonwaon_key)
    if vonwaon_rel:
        vonwaon_path = get_full_path(vonwaon_rel)
        if os.path.exists(vonwaon_path):
            try:
                font = pygame.font.Font(vonwaon_path, size)
                test_surface = font.render('你好', True, (0, 0, 0))
                w, h = test_surface.get_size()
                if w > 15 and h > 5:
                    _font_cache[cache_key] = font
                    print(f"字体加载成功: VonwaonBitmap ({vonwaon_path})")
                    return font
            except Exception as e:
                print(f"VonwaonBitmap 加载失败: {e}")
    
    # 2. 尝试 Noto Sans CJK（本地或系统）
    noto_rel = _FONT_RELATIVE_PATHS.get('noto_cjk')
    if noto_rel:
        noto_path = get_full_path(noto_rel)
        if os.path.exists(noto_path):
            try:
                font = pygame.font.Font(noto_path, size)
                test_surface = font.render('你好', True, (0, 0, 0))
                w, h = test_surface.get_size()
                if w > 15 and h > 5:
                    _font_cache[cache_key] = font
                    print(f"字体加载成功: Noto Sans CJK ({noto_path})")
                    return font
            except Exception as e:
                print(f"Noto Sans CJK 加载失败: {e}")
    
    # 2. 尝试系统字体（SysFont）
    chinese_font_names = [
        # Linux/macOS - Noto
        'Noto Sans CJK SC',
        'Noto Sans CJK',
        'noto sans cjk',
        'notosanscjk',
        # Windows - 微软雅黑
        'Microsoft YaHei',
        'microsoftyahei',
        '微软雅黑',
        # Windows - 黑体
        'SimHei',
        'simhei',
        '黑体',
        # macOS - 苹方
        'PingFang SC',
        'PingFang',
        'pingfang',
        # Linux - Droid
        'Droid Sans Fallback',
        'droid sans fallback',
    ]
    
    for font_name in chinese_font_names:
        try:
            font = pygame.font.SysFont(font_name, size)
            test_surface = font.render('你好', True, (0, 0, 0))
            w, h = test_surface.get_size()
            if w > 15 and h > 5:
                _font_cache[cache_key] = font
                print(f"字体加载成功: {font_name} (系统字体)")
                return font
        except Exception:
            continue
    
    # 3. 尝试系统 Noto Sans CJK
    noto_system = _FONT_RELATIVE_PATHS.get('noto_cjk_system')
    if noto_system and os.path.exists(noto_system):
        try:
            font = pygame.font.Font(noto_system, size)
            test_surface = font.render('你好', True, (0, 0, 0))
            w, h = test_surface.get_size()
            if w > 15 and h > 5:
                _font_cache[cache_key] = font
                print(f"字体加载成功: Noto Sans CJK (系统: {noto_system})")
                return font
        except Exception as e:
            print(f"系统 Noto Sans CJK 加载失败: {e}")
    
    # 4. 尝试其他系统字体路径
    font_paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "/System/Library/Fonts/PingFang.ttc",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = pygame.font.Font(font_path, size)
                test_surface = font.render('你好', True, (0, 0, 0))
                w, h = test_surface.get_size()
                if w > 15 and h > 5:
                    _font_cache[cache_key] = font
                    print(f"字体加载成功: {font_path}")
                    return font
            except Exception:
                continue
    
    # 4. 最后回退到默认字体
    print("警告: 未找到中文字体，文本可能显示为方块")
    font = pygame.font.Font(None, size)
    _font_cache[cache_key] = font
    return font


def _get_english_font(size: int) -> pygame.font.Font:
    """
    获取英文字体（Press Start 2P）
    
    用于英文/数字显示，像素风格。
    
    Args:
        size: 字体大小
    
    Returns:
        pygame.font.Font: 字体对象
    """
    cache_key = f"english_{size}"
    if cache_key in _font_cache:
        return _font_cache[cache_key]
    
    font = None
    
    # 优先使用 Press Start 2P
    press_rel = _FONT_RELATIVE_PATHS.get('press_start_2p')
    if press_rel:
        press_path = get_full_path(press_rel)
        if os.path.exists(press_path):
            try:
                font = pygame.font.Font(press_path, size)
                test_surface = font.render('Hello', True, (0, 0, 0))
                w, h = test_surface.get_size()
                if w > 10 and h > 5:
                    _font_cache[cache_key] = font
                    print(f"英文字体加载成功: Press Start 2P ({press_path})")
                    return font
            except Exception as e:
                print(f"Press Start 2P 加载失败: {e}")
    
    # 回退到默认字体
    font = pygame.font.Font(None, size)
    _font_cache[cache_key] = font
    return font


class NPCState(Enum):
    """NPC 状态枚举"""
    IDLE = 0      # 闲置
    WALKING = 1   # 走动中
    TALKING = 2   # 对话中


# ============================================================
# 9-Slice 渲染器（模块级别缓存）
# ============================================================

class NineSliceRenderer:
    """
    9-Slice 边框渲染器
    
    支持从单张边框图片切分出 9 个区域，并拉伸渲染到任意尺寸的矩形。
    """
    
    # 缓存已加载的边框图片
    _border_cache: Dict[str, pygame.Surface] = {}
    _arrow_cache: Dict[str, pygame.Surface] = {}
    
    @classmethod
    def load_border(cls, path: str) -> pygame.Surface:
        """
        加载边框图片（带缓存）
        
        Args:
            path: 图片路径
            
        Returns:
            pygame.Surface: 边框图片
        """
        full_path = get_full_path(path)
        
        if full_path not in cls._border_cache:
            if os.path.exists(full_path):
                cls._border_cache[full_path] = pygame.image.load(full_path).convert_alpha()
            else:
                print(f"警告: 边框图片不存在: {full_path}")
                # 创建一个默认的边框表面
                default_surface = pygame.Surface((384, 128), pygame.SRCALPHA)
                pygame.draw.rect(default_surface, (255, 255, 255, 240), (0, 0, 384, 128), border_radius=16)
                pygame.draw.rect(default_surface, (100, 100, 100, 255), (0, 0, 384, 128), width=2, border_radius=16)
                cls._border_cache[full_path] = default_surface
        
        return cls._border_cache[full_path]
    
    @classmethod
    def load_arrow(cls, path: str) -> pygame.Surface:
        """
        加载箭头图片（带缓存）
        
        Args:
            path: 图片路径
            
        Returns:
            pygame.Surface: 箭头图片
        """
        full_path = get_full_path(path)
        
        if full_path not in cls._arrow_cache:
            if os.path.exists(full_path):
                cls._arrow_cache[full_path] = pygame.image.load(full_path).convert_alpha()
            else:
                # 创建默认箭头
                default_arrow = pygame.Surface((24, 16), pygame.SRCALPHA)
                pygame.draw.polygon(
                    default_arrow,
                    (255, 255, 255, 240),
                    [(12, 0), (24, 16), (0, 16)]
                )
                cls._arrow_cache[full_path] = default_arrow
        
        return cls._arrow_cache[full_path]
    
    @classmethod
    def draw_9slice(
        cls,
        surface: pygame.Surface,
        border_img: pygame.Surface,
        rect: pygame.Rect,
        config: NineSliceConfig = None
    ) -> None:
        """
        绘制 9-slice 边框
        
        将边框图片切分为 9 个区域，拉伸渲染到目标矩形。
        
        布局:
        ┌────┬────────┬────┐
        │ TL │   T    │ TR │
        ├────┼────────┼────┤
        │ L  │   C    │ R  │
        ├────┼────────┼────┤
        │ BL │   B    │ BR │
        └────┴────────┴────┘
        
        Args:
            surface: 目标渲染表面
            border_img: 边框源图片
            rect: 目标矩形区域
            config: 9-slice 配置
        """
        if config is None:
            config = DEFAULT_NINE_SLICE
        
        # 获取源图片尺寸
        src_w, src_h = border_img.get_size()
        
        # 边框尺寸
        bl = config.border_left
        br = config.border_right
        bt = config.border_top
        bb = config.border_bottom
        
        # 确保边框尺寸不超过图片尺寸
        if bl + br > rect.width or bt + bb > rect.height:
            # 目标太小，直接缩放整个图片
            scaled = pygame.transform.scale(border_img, (rect.width, rect.height))
            surface.blit(scaled, rect.topleft)
            return
        
        # 目标区域尺寸
        dst_w, dst_h = rect.width, rect.height
        
        # 中心区域尺寸（可拉伸部分）
        center_w = dst_w - bl - br
        center_h = dst_h - bt - bb
        
        # 源图片中心区域尺寸
        src_center_w = src_w - bl - br
        src_center_h = src_h - bt - bb
        
        # 目标位置
        dx, dy = rect.x, rect.y
        
        # === 1. 绘制四个角（不拉伸）===
        # 左上角
        corner_tl = border_img.subsurface(pygame.Rect(0, 0, bl, bt))
        surface.blit(corner_tl, (dx, dy))
        
        # 右上角
        corner_tr = border_img.subsurface(pygame.Rect(src_w - br, 0, br, bt))
        surface.blit(corner_tr, (dx + dst_w - br, dy))
        
        # 左下角
        corner_bl = border_img.subsurface(pygame.Rect(0, src_h - bb, bl, bb))
        surface.blit(corner_bl, (dx, dy + dst_h - bb))
        
        # 右下角
        corner_br = border_img.subsurface(pygame.Rect(src_w - br, src_h - bb, br, bb))
        surface.blit(corner_br, (dx + dst_w - br, dy + dst_h - bb))
        
        # === 2. 绘制四条边（单向拉伸）===
        # 上边（水平拉伸）
        if center_w > 0 and src_center_w > 0:
            edge_t = border_img.subsurface(pygame.Rect(bl, 0, src_center_w, bt))
            edge_t_scaled = pygame.transform.scale(edge_t, (center_w, bt))
            surface.blit(edge_t_scaled, (dx + bl, dy))
        
        # 下边（水平拉伸）
        if center_w > 0 and src_center_w > 0:
            edge_b = border_img.subsurface(pygame.Rect(bl, src_h - bb, src_center_w, bb))
            edge_b_scaled = pygame.transform.scale(edge_b, (center_w, bb))
            surface.blit(edge_b_scaled, (dx + bl, dy + dst_h - bb))
        
        # 左边（垂直拉伸）
        if center_h > 0 and src_center_h > 0:
            edge_l = border_img.subsurface(pygame.Rect(0, bt, bl, src_center_h))
            edge_l_scaled = pygame.transform.scale(edge_l, (bl, center_h))
            surface.blit(edge_l_scaled, (dx, dy + bt))
        
        # 右边（垂直拉伸）
        if center_h > 0 and src_center_h > 0:
            edge_r = border_img.subsurface(pygame.Rect(src_w - br, bt, br, src_center_h))
            edge_r_scaled = pygame.transform.scale(edge_r, (br, center_h))
            surface.blit(edge_r_scaled, (dx + dst_w - br, dy + bt))
        
        # === 3. 绘制中心区域（双向拉伸）===
        if center_w > 0 and center_h > 0 and src_center_w > 0 and src_center_h > 0:
            center = border_img.subsurface(pygame.Rect(bl, bt, src_center_w, src_center_h))
            center_scaled = pygame.transform.scale(center, (center_w, center_h))
            surface.blit(center_scaled, (dx + bl, dy + bt))


class NPC(Entity):
    """
    NPC 类

    卡通小动物角色（与玩家风格一致，不同颜色）。
    支持闲置呼吸动画和交互反馈。
    """

    # 动画参数
    IDLE_FLOAT_AMPLITUDE: float = 1.5   # 闲置浮动幅度（比玩家小）
    IDLE_FLOAT_SPEED: float = 3.0       # 闲置浮动速度

    # 精灵尺寸
    SPRITE_SIZE: int = 32  # 与玩家相同

    # NPC 颜色配置（不同颜色方案）
    COLOR_SCHEMES = {
        'pink': {
            'body': (255, 182, 193),        # 粉色身体（与玩家相同）
            'ear': (255, 150, 170),         # 深粉色耳朵
            'eye': (40, 40, 40),            # 深灰色眼睛
            'eye_highlight': (255, 255, 255),
            'cheek': (255, 130, 150),       # 腮红
        },
        'green': {
            'body': (144, 238, 144),        # 浅绿色身体
            'ear': (60, 179, 113),          # 中绿色耳朵
            'eye': (40, 40, 40),
            'eye_highlight': (255, 255, 255),
            'cheek': (152, 251, 152),       # 浅绿腮红
        },
        'blue': {
            'body': (173, 216, 230),        # 浅蓝色身体
            'ear': (70, 130, 180),          # 钢蓝色耳朵
            'eye': (40, 40, 40),
            'eye_highlight': (255, 255, 255),
            'cheek': (135, 206, 250),       # 浅蓝腮红
        },
        'yellow': {
            'body': (255, 255, 224),        # 浅黄色身体
            'ear': (240, 230, 140),         # 卡其色耳朵
            'eye': (40, 40, 40),
            'eye_highlight': (255, 255, 255),
            'cheek': (255, 228, 181),       # 木瓜鞭腮红
        },
    }

    # 对话内容
    DIALOGS = {
        'default': ["你好~", "Hi!", "有什么事吗？", "欢迎！"],
        'green': ["你好呀~", "今天天气真好！", "需要帮忙吗？"],
        'blue': ["嘿~", "有什么新鲜事吗？", "一起来玩吧！"],
        'yellow': ["你好你好~", "见到你真开心！", "有什么想聊的吗？"],
    }

    # 自言自语内容（NPC自己说话）
    MUMURS = {
        'default': ["嗯...", "有点无聊...", "今天天气不错~", "想去哪走走呢...", "呼~"],
        'green': ["草地上好舒服~", "有没有好吃的呢...", "有点困了...", "嗯嗯~"],
        'blue': ["想看海...", "天空好蓝~", "有点冷...", "嘿嘿~"],
        'yellow': ["阳光真好~", "想睡觉...", "有点饿了...", "啦啦啦~"],
    }

    # 对话气泡配置
    BUBBLE_DURATION: float = 3.0  # 气泡显示时长（秒）
    MUMUR_DURATION: float = 2.0   # 自言自语气泡时长（秒）
    MUMUR_CHANCE: float = 0.02    # 每帧自言自语概率（约每秒0.12次，即每8秒左右一次）

    def __init__(
        self,
        x: float,
        y: float,
        color_scheme: str = 'pink',
        name: str = "NPC"
    ):
        """
        初始化 NPC

        Args:
            x: 世界 X 坐标（像素）
            y: 世界 Y 坐标（像素）
            color_scheme: 颜色方案名称
            name: NPC 名称
        """
        # 调用父类初始化
        super().__init__(x, y, self.SPRITE_SIZE, self.SPRITE_SIZE)

        # NPC 基本信息
        self.name = name
        self.color_scheme = color_scheme

        # 获取颜色配置
        colors = self.COLOR_SCHEMES.get(color_scheme, self.COLOR_SCHEMES['pink'])
        self.body_color = colors['body']
        self.ear_color = colors['ear']
        self.eye_color = colors['eye']
        self.eye_highlight = colors['eye_highlight']
        self.cheek_color = colors['cheek']

        # 状态
        self.state = NPCState.IDLE

        # 动画时间
        self.anim_time: float = 0.0

        # 对话气泡
        self.show_bubble: bool = False
        self.bubble_text: str = ""
        self.bubble_timer: float = 0.0

        # 圆形碰撞模型（比精灵稍小，更顺滑）
        self.collision_radius: float = (self.SPRITE_SIZE - 6) / 2  # 半径，比精灵小一点

        # 调整碰撞盒（比精灵稍小）
        self.hitbox_offset_x = 4
        self.hitbox_offset_y = 6
        self.hitbox_width = self.SPRITE_SIZE - 8
        self.hitbox_height = self.SPRITE_SIZE - 10

        # ===== 随机走动系统 =====
        # 移动速度（像素/秒）
        self.walk_speed: float = 30.0
        # 当前移动方向 (dx, dy)，归一化向量
        self.walk_direction: Tuple[float, float] = (0.0, 0.0)
        # 走动计时器
        self.walk_timer: float = 0.0
        # 当前状态持续时间
        self.state_timer: float = 0.0
        # 走动持续时间范围（秒）
        self.walk_duration_range: Tuple[float, float] = (1.0, 3.0)
        # 停留持续时间范围（秒）
        self.idle_duration_range: Tuple[float, float] = (1.5, 4.0)
        # 场景引用（用于碰撞检测）
        self.scene = None
        # 初始状态：随机决定是走动还是停留
        self._start_random_state()

    def set_scene(self, scene) -> None:
        """
        设置场景引用
        
        Args:
            scene: 场景对象（需要有 is_position_walkable 方法）
        """
        self.scene = scene

    def _start_random_state(self) -> None:
        """随机决定初始状态并开始"""
        import random
        if random.random() < 0.5:
            # 开始走动
            self._start_walking()
        else:
            # 开始停留
            self._start_idle()

    def _start_walking(self) -> None:
        """开始随机走动"""
        import random
        
        self.state = NPCState.WALKING
        # 随机方向
        angle = random.uniform(0, 2 * math.pi)
        self.walk_direction = (math.cos(angle), math.sin(angle))
        # 随机走动时长
        self.state_timer = random.uniform(*self.walk_duration_range)
        self.walk_timer = 0.0

    def _start_idle(self) -> None:
        """开始停留"""
        import random
        
        self.state = NPCState.IDLE
        self.walk_direction = (0.0, 0.0)
        # 随机停留时长
        self.state_timer = random.uniform(*self.idle_duration_range)

    def _try_change_direction(self) -> None:
        """尝试改变方向（遇到障碍物时调用）"""
        import random
        
        # 随机选择一个新的方向（避开当前方向的反方向附近）
        angle = random.uniform(0, 2 * math.pi)
        self.walk_direction = (math.cos(angle), math.sin(angle))

    def show_dialog(self, text: str = "你好！") -> None:
        """
        显示对话气泡

        Args:
            text: 对话文本
        """
        self.show_bubble = True
        self.bubble_text = text
        self.bubble_timer = self.BUBBLE_DURATION
        self.state = NPCState.TALKING

    def hide_dialog(self) -> None:
        """隐藏对话气泡"""
        self.show_bubble = False
        self.bubble_text = ""
        self.bubble_timer = 0.0
        # 对话结束后，开始停留状态
        self._start_idle()

    def interact(self) -> str:
        """
        被交互时调用

        Returns:
            对话文本
        """
        import random

        # 如果正在自言自语，立即切换为互动对话
        # 如果已经在互动对话中，不重复触发
        if self.show_bubble and self.state == NPCState.TALKING:
            return self.bubble_text

        # 根据颜色方案选择对话内容
        dialogs = self.DIALOGS.get(self.color_scheme, self.DIALOGS['default'])
        text = random.choice(dialogs)

        self.show_dialog(text)
        return text

    def update(self, dt: float) -> None:
        """
        更新 NPC 状态

        Args:
            dt: 时间增量（秒）
        """
        if not self.active:
            return

        # 更新动画时间
        self.anim_time += dt

        # 更新气泡计时器
        if self.show_bubble:
            self.bubble_timer -= dt
            if self.bubble_timer <= 0:
                # 区分对话和自言自语
                if self.state == NPCState.TALKING:
                    # 对话结束，恢复
                    self.hide_dialog()
                else:
                    # 自言自语结束，只清除气泡
                    self.show_bubble = False
                    self.bubble_text = ""
            
            # 对话时不走动
            if self.state == NPCState.TALKING:
                return

        # ===== 随机走动系统 =====
        self.state_timer -= dt
        
        if self.state == NPCState.WALKING:
            # 走动状态
            self._update_walking(dt)
        elif self.state == NPCState.IDLE:
            # 停留状态
            self._update_idle(dt)

    def _update_walking(self, dt: float) -> None:
        """
        更新走动状态
        
        Args:
            dt: 时间增量（秒）
        """
        import random
        
        # 检查是否该停下来
        if self.state_timer <= 0:
            self._start_idle()
            return
        
        # 计算移动量
        dx = self.walk_direction[0] * self.walk_speed * dt
        dy = self.walk_direction[1] * self.walk_speed * dt
        
        # 尝试移动
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 检查碰撞
        can_move_x = self._check_walkable(new_x, self.y)
        can_move_y = self._check_walkable(self.x, new_y)
        
        if can_move_x and can_move_y:
            # 两个方向都可以移动
            self.x = new_x
            self.y = new_y
        elif can_move_x:
            # 只能 X 方向移动（Y 方向有障碍）
            self.x = new_x
            # 改变 Y 方向
            self.walk_direction = (self.walk_direction[0], -self.walk_direction[1])
        elif can_move_y:
            # 只能 Y 方向移动（X 方向有障碍）
            self.y = new_y
            # 改变 X 方向
            self.walk_direction = (-self.walk_direction[0], self.walk_direction[1])
        else:
            # 两个方向都有障碍，改变方向
            self._try_change_direction()
        
        # 走动计时器
        self.walk_timer += dt

    def _update_idle(self, dt: float) -> None:
        """
        更新停留状态
        
        Args:
            dt: 时间增量（秒）
        """
        import random
        
        # 检查是否该开始走动
        if self.state_timer <= 0:
            self._start_walking()
            return
        
        # 随机自言自语（不在对话中时）
        if not self.show_bubble and random.random() < self.MUMUR_CHANCE:
            self._do_mumur()

    def _do_mumur(self) -> None:
        """执行自言自语"""
        import random
        
        # 获取对应颜色的自言自语内容
        mumurs = self.MUMURS.get(self.color_scheme, self.MUMURS['default'])
        text = random.choice(mumurs)
        
        # 显示自言自语气泡
        self.show_bubble = True
        self.bubble_text = text
        self.bubble_timer = self.MUMUR_DURATION
        # 自言自语时不改变状态，保持 IDLE

    def _check_walkable(self, x: float, y: float) -> bool:
        """
        检查指定位置是否可行走
        
        Args:
            x: X 坐标
            y: Y 坐标
            
        Returns:
            是否可行走
        """
        if self.scene is None:
            # 没有场景引用，默认可以移动
            return True
        
        # 计算圆心位置
        center_x = x + self.SPRITE_SIZE / 2
        center_y = y + self.SPRITE_SIZE / 2
        
        # 检查场景中的可行走区域
        if hasattr(self.scene, 'is_position_walkable'):
            # 使用圆形碰撞检测（检测圆周上的点）
            # 圆周上均匀分布 8 个检测点 + 圆心
            import math
            points_to_check = [(center_x, center_y)]  # 圆心
            
            for angle in range(0, 360, 45):  # 每 45 度一个点
                rad = math.radians(angle)
                px = center_x + self.collision_radius * math.cos(rad)
                py = center_y + self.collision_radius * math.sin(rad)
                points_to_check.append((px, py))
            
            for px, py in points_to_check:
                if not self.scene.is_position_walkable(px, py):
                    return False
            
            return True
        
        # 如果场景没有碰撞检测方法，默认可以移动
        return True

    def render(
        self,
        surface: pygame.Surface,
        camera: Optional['Camera'] = None
    ) -> None:
        """
        渲染 NPC 精灵

        Args:
            surface: 目标渲染表面
            camera: 相机对象
        """
        if not self.visible:
            return

        # 获取屏幕坐标
        screen_x, screen_y = self._get_screen_position(camera)

        # 绘制影子
        self._draw_shadow(surface, screen_x, screen_y)

        # 计算闲置浮动偏移
        offset_y = math.sin(self.anim_time * self.IDLE_FLOAT_SPEED * 2 * math.pi) * self.IDLE_FLOAT_AMPLITUDE

        # 绘制 NPC 精灵
        self._draw_sprite(surface, screen_x, int(screen_y + offset_y))

        # 绘制对话气泡
        if self.show_bubble:
            self._draw_bubble(surface, screen_x, int(screen_y + offset_y), camera)

    def _draw_sprite(
        self,
        surface: pygame.Surface,
        x: int,
        y: int
    ) -> None:
        """
        绘制 NPC 精灵

        与玩家风格一致的卡通小动物形象。

        Args:
            surface: 目标渲染表面
            x: 屏幕 X 坐标
            y: 屏幕 Y 坐标
        """
        center_x = x + self.SPRITE_SIZE // 2
        center_y = y + self.SPRITE_SIZE // 2

        # === 绘制身体（椭圆）===
        body_width = 20
        body_height = 18
        body_rect = pygame.Rect(
            center_x - body_width // 2,
            center_y - body_height // 2,
            body_width,
            body_height
        )
        pygame.draw.ellipse(surface, self.body_color, body_rect)

        # === 绘制耳朵 ===
        ear_width = 5
        ear_height = 6
        ear_y = center_y - body_height // 2 - ear_height // 2

        # 左耳
        pygame.draw.ellipse(
            surface,
            self.ear_color,
            pygame.Rect(center_x - body_width // 3, ear_y, ear_width, ear_height)
        )
        # 右耳
        pygame.draw.ellipse(
            surface,
            self.ear_color,
            pygame.Rect(center_x + body_width // 6, ear_y, ear_width, ear_height)
        )

        # === 绘制眼睛（看向玩家，默认向下）===
        eye_y = center_y - 2
        eye_spacing = 6

        self._draw_eye(surface, center_x - 3, eye_y)
        self._draw_eye(surface, center_x + 3, eye_y)

        # === 绘制腮红 ===
        cheek_y = center_y + 4
        pygame.draw.circle(
            surface,
            self.cheek_color,
            (center_x - body_width // 3, cheek_y),
            2
        )
        pygame.draw.circle(
            surface,
            self.cheek_color,
            (center_x + body_width // 3, cheek_y),
            2
        )

    def _draw_shadow(
        self,
        surface: pygame.Surface,
        x: int,
        y: int
    ) -> None:
        """
        绘制 NPC 影子

        Args:
            surface: 目标渲染表面
            x: 屏幕 X 坐标
            y: 屏幕 Y 坐标
        """
        shadow_width = self.SPRITE_SIZE - 4
        shadow_height = 6

        # 创建影子表面
        shadow_surface = pygame.Surface((shadow_width, shadow_height), pygame.SRCALPHA)
        shadow_color = (50, 50, 50, 80)
        pygame.draw.ellipse(shadow_surface, shadow_color, (0, 0, shadow_width, shadow_height))

        # 绘制影子
        shadow_x = x + (self.SPRITE_SIZE - shadow_width) // 2
        shadow_y = y + self.SPRITE_SIZE - 4
        surface.blit(shadow_surface, (shadow_x, shadow_y))

    def _draw_eye(
        self,
        surface: pygame.Surface,
        x: int,
        y: int
    ) -> None:
        """
        绘制单只眼睛

        Args:
            surface: 目标渲染表面
            x: 眼睛 X 坐标
            y: 眼睛 Y 坐标
        """
        # 眼白
        pygame.draw.circle(surface, self.eye_highlight, (x, y), 2)

        # 眼珠（居中）
        pygame.draw.circle(surface, self.eye_color, (x, y), 1)

    def _calculate_text_lines(
        self,
        text: str,
        font: pygame.font.Font,
        max_width: int
    ) -> Tuple[int, int, list]:
        """
        计算文本所需尺寸，支持自动换行
        
        Args:
            text: 要显示的文本
            font: 字体对象
            max_width: 最大宽度限制
        
        Returns:
            (最大行宽度, 总高度, 行列表)
        """
        lines = []
        current_line = ""
        
        for char in text:
            test_line = current_line + char
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = char
        
        if current_line:
            lines.append(current_line)
        
        if not lines:
            return 0, 0, []
        
        line_height = font.get_linesize()
        total_height = len(lines) * line_height
        max_line_width = max(font.size(line)[0] for line in lines)
        
        return max_line_width, total_height, lines

    def _draw_bubble(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        camera: Optional['Camera'] = None
    ) -> None:
        """
        绘制对话气泡（使用 9-slice 边框）

        Args:
            surface: 目标渲染表面
            x: NPC 屏幕 X 坐标
            y: NPC 屏幕 Y 坐标
            camera: 相机对象
        """
        # 获取样式配置
        style = STYLE_DEFAULT
        
        # 使用支持中文的字体 - 14px 粗体
        font = _get_chinese_font(14)
        
        # 文本最大宽度限制（屏幕宽度的 60%）
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        max_text_width = int(screen_width * 0.6)
        
        # 检查 NPC 是否在屏幕范围内（留出一定边距）
        margin = 100  # 边距
        if x < -margin or x > screen_width + margin or y < -margin or y > screen_height + margin:
            # NPC 在屏幕外，不显示气泡
            return
        
        # 计算文本换行
        text_width, text_height, lines = self._calculate_text_lines(
            self.bubble_text, font, max_text_width
        )
        
        if not lines:
            return
        
        # 气泡内边距
        padding_x = 10
        padding_y = 6
        
        # 计算气泡尺寸（根据文本实际尺寸动态调整）
        bubble_width = text_width + padding_x * 2
        bubble_height = text_height + padding_y * 2
        
        # 确保最小尺寸
        min_width = 40
        min_height = 24
        bubble_width = max(bubble_width, min_width)
        bubble_height = max(bubble_height, min_height)
        
        # 使用缩小的 9-slice 边框配置（边框宽度 6px，更细）
        small_nine_slice = NineSliceConfig(
            border_left=6,
            border_right=6,
            border_top=6,
            border_bottom=6
        )
        
        # 确保最小尺寸能容纳 9-slice 边框
        min_size = small_nine_slice.border_left + small_nine_slice.border_right
        bubble_width = max(bubble_width, min_size)
        bubble_height = max(bubble_height, min_size)
        
        # 三角形尺寸（缩小到合理比例：宽度 10-12 像素）
        triangle_width = 10
        triangle_height = 6
        triangle_offset = 2  # 与气泡的间距
        
        # 气泡位置（NPC 头顶，居中对齐）
        bubble_x = x + self.SPRITE_SIZE // 2 - bubble_width // 2
        bubble_y = y - bubble_height - triangle_height - triangle_offset - 8
        
        # 不再强制将气泡限制在屏幕内，让气泡自然跟随NPC位置
        
        # 创建气泡矩形
        bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
        
        # === 加载并绘制 9-slice 边框 ===
        try:
            border_img = NineSliceRenderer.load_border(DIALOG_BORDER_PATH)
            NineSliceRenderer.draw_9slice(
                surface,
                border_img,
                bubble_rect,
                small_nine_slice  # 使用缩小的边框配置
            )
        except Exception as e:
            # 回退到简单矩形
            print(f"警告: 无法加载边框图片，使用简单矩形: {e}")
            pygame.draw.rect(
                surface,
                style.background_color,
                bubble_rect,
                border_radius=style.border_radius
            )
            pygame.draw.rect(
                surface,
                style.border_color,
                bubble_rect,
                width=style.border_width,
                border_radius=style.border_radius
            )
        
        # === 绘制三角形（指向 NPC）===
        # 三角形位置：气泡底部中央下方
        triangle_points = [
            (bubble_rect.centerx - triangle_width // 2, bubble_rect.bottom + triangle_offset),
            (bubble_rect.centerx + triangle_width // 2, bubble_rect.bottom + triangle_offset),
            (bubble_rect.centerx, bubble_rect.bottom + triangle_offset + triangle_height)
        ]
        pygame.draw.polygon(surface, style.background_color, triangle_points)
        
        # === 绘制文本（支持多行）===
        line_height = font.get_linesize()
        start_y = bubble_rect.centery - (len(lines) * line_height) // 2
        
        for i, line in enumerate(lines):
            line_surface = font.render(line, True, style.text_color)
            line_rect = line_surface.get_rect()
            line_pos = (
                bubble_rect.centerx - line_rect.width // 2,
                start_y + i * line_height
            )
            surface.blit(line_surface, line_pos)

    def __repr__(self) -> str:
        """字符串表示"""
        return f"NPC(name={self.name}, x={self.x:.1f}, y={self.y:.1f}, color={self.color_scheme})"
