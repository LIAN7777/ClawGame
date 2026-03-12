"""
ClawGame 测试配置
"""

import os
import pytest
import pygame
import sys
from pathlib import Path

# 设置虚拟显示驱动（headless 环境）
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """初始化 pygame（整个测试会话只执行一次）"""
    pygame.init()
    yield
    pygame.quit()
