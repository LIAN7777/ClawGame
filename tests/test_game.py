"""
游戏核心模块测试
"""

import pytest
import pygame
from game.game import Game


class TestGame:
    """Game 类测试"""
    
    def test_game_init(self):
        """测试游戏初始化"""
        screen = pygame.display.set_mode((800, 600))
        game = Game(screen)
        
        assert game.width == 800
        assert game.height == 600
        assert game.running is True
        assert game.paused is False
    
    def test_game_colors(self):
        """测试颜色定义"""
        screen = pygame.display.set_mode((800, 600))
        game = Game(screen)
        
        assert "background" in game.colors
        assert "white" in game.colors
        assert "black" in game.colors
    
    def test_pause_toggle(self):
        """测试暂停切换"""
        screen = pygame.display.set_mode((800, 600))
        game = Game(screen)
        
        # 模拟按下 ESC 键
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
        game.handle_event(event)
        
        assert game.paused is True
        
        # 再次按下 ESC
        game.handle_event(event)
        assert game.paused is False
    
    def test_quit_key(self):
        """测试退出键"""
        screen = pygame.display.set_mode((800, 600))
        game = Game(screen)
        
        # 模拟按下 Q 键
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q)
        game.handle_event(event)
        
        assert game.running is False
