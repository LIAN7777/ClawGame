"""
测试自定义房间场景渲染
生成截图验证效果
"""

import os
import sys

# 添加 src 目录到路径
src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src")
sys.path.insert(0, src_path)

import pygame

# 初始化
pygame.init()

# 创建虚拟显示模式（用于图片加载）
pygame.display.set_mode((1, 1))

# 创建测试表面
width, height = 800, 600
surface = pygame.Surface((width, height))

# 导入场景
from game.custom_room_scene import CustomRoomScene

# 创建场景
print("创建自定义房间场景...")
scene = CustomRoomScene()

# 创建简单的相机
class SimpleCamera:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

# 渲染场景
print("\n渲染场景...")
camera = SimpleCamera(200, 200)  # 从房间中央开始
scene.render(surface, camera)

# 保存截图
output_path = os.path.join(os.path.dirname(__file__), "test_room_screenshot.png")
pygame.image.save(surface, output_path)
print(f"\n截图已保存: {output_path}")

# 测试碰撞检测
print("\n测试碰撞检测:")
test_positions = [
    (632, 800),  # 门前（应该可通行）
    (10, 400),   # 左墙内（不可通行）
    (1250, 400), # 右墙内（不可通行）
    (400, 10),   # 上墙内（不可通行）
    (632, 880),  # 下墙内，不在门的位置（不可通行）
    (632, 860),  # 门的位置（可通行）
    (100, 750),  # 冰箱位置（不可通行）
    (400, 400),  # 房间中央（可通行）
]

for x, y in test_positions:
    walkable = scene.is_position_walkable(float(x), float(y))
    print(f"  ({x}, {y}): {'可通行' if walkable else '不可通行'}")

# 测试玩家出生位置
spawn_x, spawn_y = scene.get_spawn_position()
print(f"\n玩家出生位置: ({spawn_x:.0f}, {spawn_y:.0f})")

print("\n测试完成！")
