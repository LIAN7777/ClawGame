"""
ClawGame 测试配置
"""

import pytest
import pygame


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """初始化 pygame（整个测试会话只执行一次）"""
    pygame.init()
    yield
    pygame.quit()
