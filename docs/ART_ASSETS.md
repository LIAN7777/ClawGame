# ClawGame 美术资源方案

## 已下载资源

### 1. 1-Bit Pack (Kenney.nl)
- **来源:** https://www.kenney.nl/assets/1-bit-pack
- **许可证:** CC0 (完全免费商用)
- **Tile 尺寸:** 16x16 像素
- **总数量:** 1078 个 tiles
- **版本:** colored-transparent.png (彩色透明背景)

**适配方案:**
- ClawGame 使用 48x48 像素 tile
- 需要将 16x16 放大 3 倍到 48x48
- 或使用 pygame.transform.scale 实时缩放

### 2. UI Pack (Kenney.nl)
- **来源:** https://www.kenney.nl/assets/ui-pack
- **许可证:** CC0 (完全免费商用)
- **元素数量:** 870+ PNG 文件
- **包含:** 按钮、箭头、面板等
- **字体:** Kenney Future (像素风格英文字体)

### 3. Game Icons (Kenney.nl)
- **来源:** https://www.kenney.nl/assets/game-icons
- **许可证:** CC0 (完全免费商用)
- **图标数量:** 105 个

## 资源使用方案

### 场景 Tile 分类 (待确认)
需要查看 tileset 确认具体 tile 位置：
- 地板 tiles
- 墙壁 tiles
- 家具 tiles (桌子、椅子、床)
- 装饰 tiles (植物、挂画)
- 门窗 tiles

### UI 元素使用
- **按钮:** button_rectangle_* 系列
- **对话框:** 需要组合多个元素或自定义绘制
- **字体:** Kenney Future (仅支持英文，中文需用系统字体)

### 颜色风格
- colored 版本有预设颜色
- 可以通过 pygame 进行颜色调整
- 建议调整为温馨暖色调

## 待办事项
1. 分析 tileset 确认各 tile 位置
2. 编写 tile 映射配置文件
3. 修改游戏代码加载外部 tileset
4. 实现对话框 UI 组件
5. 处理中文字体

## 文件位置
```
assets/
├── downloaded/        # 原始下载资源
│   ├── 1-bit-pack/
│   ├── ui-pack/
│   └── game-icons/
├── images/
│   ├── tiles/
│   │   └── tileset.png
│   └── ui/
└── fonts/
    └── KenneyFuture.ttf
```
