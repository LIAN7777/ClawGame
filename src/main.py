"""
ClawGame - 休闲养成小游戏
主入口文件
"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径（支持 python -m src.main 运行方式）
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import pygame

from config import config
from game.game import Game
from utils.asset_loader import AssetLoader


def main():
    """游戏主入口"""
    # 初始化 Pygame
    pygame.init()
    
    # 尝试初始化音效系统（可选）
    try:
        pygame.mixer.init()
    except pygame.error:
        print("警告: 音频设备不可用，游戏将以静音模式运行")
    
    # 创建窗口（使用配置中的分辨率）
    screen = pygame.display.set_mode(config.screen_resolution)
    pygame.display.set_caption(config.TITLE)
    
    # 创建内部渲染表面（用于缩放渲染）
    internal_surface = pygame.Surface(config.internal_resolution)
    
    # 创建时钟
    clock = pygame.time.Clock()
    
    # 创建资源管理器
    asset_loader = AssetLoader("assets")
    
    # 创建游戏实例
    game = Game(screen, asset_loader)
    
    # 游戏主循环
    running = True
    while running:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        
        # 更新游戏状态
        game.update()
        
        # 渲染到内部表面
        game.render(internal_surface)
        
        # 缩放到窗口大小
        scaled_surface = pygame.transform.scale(
            internal_surface, 
            config.screen_resolution
        )
        screen.blit(scaled_surface, (0, 0))
        
        # 刷新显示
        pygame.display.flip()
        
        # 控制帧率
        clock.tick(config.FPS)
    
    # 清理资源
    asset_loader.clear_cache()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
