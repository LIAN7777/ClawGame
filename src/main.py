"""
ClawGame - 休闲养成小游戏
主入口文件
"""

import pygame
import sys
from game.game import Game


def main():
    """游戏主入口"""
    pygame.init()
    
    # 游戏配置
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    
    # 创建窗口
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ClawGame - 休闲养成")
    
    # 创建时钟
    clock = pygame.time.Clock()
    
    # 创建游戏实例
    game = Game(screen)
    
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
        
        # 渲染
        game.render()
        
        # 刷新显示
        pygame.display.flip()
        
        # 控制帧率
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
