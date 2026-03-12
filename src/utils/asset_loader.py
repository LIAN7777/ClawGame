"""
ClawGame - 资源管理器模块
负责加载、缓存和管理游戏资源（图片、音效等）
"""

import os
from typing import Optional

import pygame


class AssetLoader:
    """
    资源管理器类
    
    负责加载游戏资源（图片、音效），并提供缓存机制避免重复加载。
    支持指定资源根目录，所有路径相对于该目录。
    
    使用示例:
        loader = AssetLoader("assets")
        player_img = loader.load_image("sprites/player.png")
        jump_sound = loader.load_sound("audio/jump.wav")
    """
    
    def __init__(self, root_dir: str = "assets"):
        """
        初始化资源管理器
        
        Args:
            root_dir: 资源根目录路径，默认为 "assets"
        """
        self._root_dir = root_dir
        self._image_cache: dict[str, pygame.Surface] = {}
        self._sound_cache: dict[str, pygame.mixer.Sound] = {}
    
    def _get_full_path(self, relative_path: str) -> str:
        """
        获取资源的完整路径
        
        Args:
            relative_path: 相对于资源根目录的路径
            
        Returns:
            完整的文件系统路径
        """
        return os.path.join(self._root_dir, relative_path)
    
    def load_image(
        self, 
        path: str, 
        use_alpha: bool = True,
        scale: Optional[tuple[int, int]] = None
    ) -> pygame.Surface:
        """
        加载图片资源
        
        优先从缓存读取，缓存未命中时从文件加载。
        
        Args:
            path: 相对于资源根目录的图片路径
            use_alpha: 是否使用 Alpha 通道（支持透明），默认 True
            scale: 可选的缩放尺寸 (宽, 高)，默认不缩放
            
        Returns:
            加载的 pygame.Surface 对象
            
        Raises:
            FileNotFoundError: 图片文件不存在
            pygame.error: 图片加载失败
        """
        # 生成缓存键（包含缩放参数）
        cache_key = f"{path}:{scale}" if scale else path
        
        # 检查缓存
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]
        
        # 加载图片
        full_path = self._get_full_path(path)
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"图片文件不存在: {full_path}")
        
        if use_alpha:
            image = pygame.image.load(full_path).convert_alpha()
        else:
            image = pygame.image.load(full_path).convert()
        
        # 应用缩放
        if scale:
            image = pygame.transform.scale(image, scale)
        
        # 存入缓存
        self._image_cache[cache_key] = image
        
        return image
    
    def load_sound(self, path: str) -> pygame.mixer.Sound:
        """
        加载音效资源
        
        优先从缓存读取，缓存未命中时从文件加载。
        
        Args:
            path: 相对于资源根目录的音效路径
            
        Returns:
            加载的 pygame.mixer.Sound 对象
            
        Raises:
            FileNotFoundError: 音效文件不存在
            pygame.error: 音效加载失败
        """
        # 检查缓存
        if path in self._sound_cache:
            return self._sound_cache[path]
        
        # 加载音效
        full_path = self._get_full_path(path)
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"音效文件不存在: {full_path}")
        
        sound = pygame.mixer.Sound(full_path)
        
        # 存入缓存
        self._sound_cache[path] = sound
        
        return sound
    
    def clear_cache(self) -> None:
        """清空所有缓存"""
        self._image_cache.clear()
        self._sound_cache.clear()
    
    def clear_image_cache(self) -> None:
        """清空图片缓存"""
        self._image_cache.clear()
    
    def clear_sound_cache(self) -> None:
        """清空音效缓存"""
        self._sound_cache.clear()
    
    def get_cache_stats(self) -> dict[str, int]:
        """
        获取缓存统计信息
        
        Returns:
            包含缓存数量的字典
        """
        return {
            "images": len(self._image_cache),
            "sounds": len(self._sound_cache),
            "total": len(self._image_cache) + len(self._sound_cache)
        }
    
    @property
    def root_dir(self) -> str:
        """资源根目录"""
        return self._root_dir
