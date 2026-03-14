#!/usr/bin/env python3
"""
自动裁剪图片透明边缘工具

使用方法：
    python crop_transparent.py <输入目录> <输出目录>
    
示例：
    python crop_transparent.py assets/images/custom assets/images/cropped
"""

import os
import sys
from PIL import Image


def crop_transparent_edges(image_path: str, output_path: str, padding: int = 2) -> tuple:
    """
    裁剪图片的透明边缘
    
    Args:
        image_path: 输入图片路径
        output_path: 输出图片路径
        padding: 保留的边距（像素）
    
    Returns:
        (原尺寸, 裁剪后尺寸, 裁剪掉的像素)
    """
    img = Image.open(image_path)
    
    # 确保有 alpha 通道
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    original_size = img.size
    
    # 获取非透明区域的边界框
    bbox = img.getbbox()
    
    if bbox is None:
        # 图片完全透明
        print(f"  ⚠️ 图片完全透明，跳过: {image_path}")
        return (original_size, original_size, (0, 0, 0, 0))
    
    # 添加边距
    left = max(0, bbox[0] - padding)
    top = max(0, bbox[1] - padding)
    right = min(img.width, bbox[2] + padding)
    bottom = min(img.height, bbox[3] + padding)
    
    # 裁剪
    cropped = img.crop((left, top, right, bottom))
    
    # 保存
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cropped.save(output_path)
    
    cropped_size = cropped.size
    trimmed = (left, top, img.width - right, img.height - bottom)
    
    return (original_size, cropped_size, trimmed)


def process_directory(input_dir: str, output_dir: str, padding: int = 2):
    """
    批量处理目录下的所有图片
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        padding: 保留的边距
    """
    supported_formats = ('.png', '.gif', '.webp')
    
    # 遍历所有文件
    files_processed = 0
    
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename.lower().endswith(supported_formats):
                input_path = os.path.join(root, filename)
                
                # 保持相对路径结构
                rel_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, rel_path)
                
                print(f"处理: {rel_path}")
                
                try:
                    original, cropped, trimmed = crop_transparent_edges(
                        input_path, output_path, padding
                    )
                    
                    if trimmed != (0, 0, 0, 0):
                        print(f"  原尺寸: {original[0]}x{original[1]}")
                        print(f"  新尺寸: {cropped[0]}x{cropped[1]}")
                        print(f"  裁剪: 左{trimmed[0]} 上{trimmed[1]} 右{trimmed[2]} 下{trimmed[3]}")
                    else:
                        print(f"  尺寸不变: {original[0]}x{original[1]}")
                    
                    files_processed += 1
                    
                except Exception as e:
                    print(f"  ❌ 错误: {e}")
    
    print(f"\n✅ 完成！处理了 {files_processed} 个文件")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    padding = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print(f"边距: {padding}px")
    print("-" * 40)
    
    process_directory(input_dir, output_dir, padding)
