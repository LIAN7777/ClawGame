"""
ClawGame 测试配置
"""

import pytest
import pygame
import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """初始化 pygame（整个测试会话只执行一次）"""
    pygame.init()
    yield
    pygame.quit()
