"""
ClawGame - 指令解析器模块
从对话框文本中识别并解析控制 NPC 行为的指令
"""

import re
from typing import Dict, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class ParsedCommand:
    """解析后的指令数据结构"""
    type: str  # move, follow, stop
    target: str  # 目标 NPC 名称
    direction: Optional[str] = None  # 移动方向
    until: Optional[str] = None  # 条件：collision, player 等
    raw_text: str = ""  # 原始文本
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "type": self.type,
            "target": self.target,
            "direction": self.direction,
            "until": self.until,
            "raw_text": self.raw_text
        }


class CommandParser:
    """
    指令解析器
    
    支持的指令格式：
    - "小橘，向右走" → 向指定方向走一步
    - "向左走，直到撞墙" → 持续走直到碰撞
    - "右边" / "左边" → 简写，直接向该方向走
    - "跟着我" → 跟随玩家（Phase 2）
    - "停" / "停下" → 停止当前行为
    """
    
    # 方向关键词映射
    DIRECTION_KEYWORDS = {
        # 基本方向
        '左': 'left',
        '右': 'right',
        '上': 'up',
        '下': 'down',
        # 方位词
        '左方': 'left',
        '右方': 'right',
        '上方': 'up',
        '下方': 'down',
        '左边': 'left',
        '右边': 'right',
        # 东南西北
        '东': 'right',
        '西': 'left',
        '北': 'up',
        '南': 'down',
        '东边': 'right',
        '西边': 'left',
        '北边': 'up',
        '南边': 'down',
    }
    
    # 目标 NPC 名称（常见别名）
    NPC_ALIASES = {
        '小橘': '小橘',
        '橘橘': '小橘',
        '小绿': '小绿',
        '绿绿': '小绿',
        '小蓝': '小蓝',
        '蓝蓝': '小蓝',
    }
    
    # 指令触发前缀（可选）
    TRIGGER_PREFIXES = ['小橘', '小绿', '小蓝', '橘橘', '绿绿', '蓝蓝']
    
    # 条件关键词
    UNTIL_KEYWORDS = {
        '直到撞墙': 'collision',
        '直到碰到墙': 'collision',
        '直到撞到墙': 'collision',
        '直到碰到障碍': 'collision',
        '一直走': 'collision',  # 简写
        '一直': 'collision',
    }
    
    def __init__(self):
        """初始化指令解析器"""
        # 构建正则表达式
        self._build_patterns()
    
    def _build_patterns(self):
        """构建正则表达式模式"""
        # 方向词列表（用于正则）
        direction_words = list(self.DIRECTION_KEYWORDS.keys())
        direction_pattern = '|'.join(direction_words)
        
        # 条件词列表
        until_words = list(self.UNTIL_KEYWORDS.keys())
        until_pattern = '|'.join(re.escape(w) for w in until_words)
        
        # NPC 名称列表
        npc_names = list(self.NPC_ALIASES.keys())
        npc_pattern = '|'.join(npc_names)
        
        # 模式1: "小橘，向右走" 或 "小橘 向右走"
        self.pattern_move_with_target = re.compile(
            rf'^({npc_pattern})[,，\s]*向({direction_pattern})走'
        )
        
        # 模式2: "向左走，直到撞墙"
        self.pattern_move_until = re.compile(
            rf'^向({direction_pattern})走[,，\s]*({until_pattern})'
        )
        
        # 模式3: "向右走" (简单移动)
        self.pattern_move_simple = re.compile(
            rf'^向({direction_pattern})走'
        )
        
        # 模式4: "左边" / "右边" (简写)
        self.pattern_direction_only = re.compile(
            rf'^({direction_pattern})$'
        )
        
        # 模式5: "小橘，跟着我" 或 "跟着我"
        # 注意：使用 [，,]? 而不是 [,，\s]* 来确保正确匹配
        self.pattern_follow = re.compile(
            rf'^(?:{npc_pattern})?[，,]?\s*跟着我$'
        )
        
        # 模式6: "停" / "停下" / "停止"
        self.pattern_stop = re.compile(
            r'^(?:停|停下|停止)$'
        )
        
        # 模式7: "小橘，停" (带目标)
        self.pattern_stop_with_target = re.compile(
            rf'^({npc_pattern})[,，\s]*(?:停|停下|停止)$'
        )
    
    def parse(self, text: str, default_target: str = "小橘") -> Optional[ParsedCommand]:
        """
        解析文本指令
        
        Args:
            text: 输入文本
            default_target: 默认目标 NPC 名称
            
        Returns:
            ParsedCommand 对象，如果不是指令则返回 None
        """
        text = text.strip()
        if not text:
            return None
        
        # 尝试匹配各种模式
        
        # 1. 带目标的移动指令: "小橘，向右走"
        match = self.pattern_move_with_target.match(text)
        if match:
            target_alias = match.group(1)
            direction_word = match.group(2)
            return ParsedCommand(
                type='move',
                target=self.NPC_ALIASES.get(target_alias, target_alias),
                direction=self.DIRECTION_KEYWORDS.get(direction_word, direction_word),
                until=None,
                raw_text=text
            )
        
        # 2. 移动直到撞墙: "向左走，直到撞墙"
        match = self.pattern_move_until.match(text)
        if match:
            direction_word = match.group(1)
            until_word = match.group(2)
            return ParsedCommand(
                type='move',
                target=default_target,
                direction=self.DIRECTION_KEYWORDS.get(direction_word, direction_word),
                until=self.UNTIL_KEYWORDS.get(until_word, until_word),
                raw_text=text
            )
        
        # 3. 简单移动: "向右走"
        match = self.pattern_move_simple.match(text)
        if match:
            direction_word = match.group(1)
            return ParsedCommand(
                type='move',
                target=default_target,
                direction=self.DIRECTION_KEYWORDS.get(direction_word, direction_word),
                until=None,
                raw_text=text
            )
        
        # 4. 简写: "右边" / "左边"
        match = self.pattern_direction_only.match(text)
        if match:
            direction_word = match.group(1)
            return ParsedCommand(
                type='move',
                target=default_target,
                direction=self.DIRECTION_KEYWORDS.get(direction_word, direction_word),
                until=None,
                raw_text=text
            )
        
        # 5. 跟随指令: "跟着我" / "小橘，跟着我"
        match = self.pattern_follow.match(text)
        if match:
            # 尝试提取目标
            for alias in self.NPC_ALIASES.keys():
                if text.startswith(alias):
                    return ParsedCommand(
                        type='follow',
                        target=self.NPC_ALIASES[alias],
                        raw_text=text
                    )
            return ParsedCommand(
                type='follow',
                target=default_target,
                raw_text=text
            )
        
        # 6. 停止指令: "停"
        match = self.pattern_stop.match(text)
        if match:
            return ParsedCommand(
                type='stop',
                target=default_target,
                raw_text=text
            )
        
        # 7. 带目标的停止: "小橘，停"
        match = self.pattern_stop_with_target.match(text)
        if match:
            target_alias = match.group(1)
            return ParsedCommand(
                type='stop',
                target=self.NPC_ALIASES.get(target_alias, target_alias),
                raw_text=text
            )
        
        # 不是指令
        return None
    
    def is_command(self, text: str) -> bool:
        """
        快速判断文本是否是指令
        
        Args:
            text: 输入文本
            
        Returns:
            是否是指令
        """
        return self.parse(text) is not None


# 模块级别的单例
_parser_instance: Optional[CommandParser] = None


def get_command_parser() -> CommandParser:
    """获取指令解析器单例"""
    global _parser_instance
    if _parser_instance is None:
        _parser_instance = CommandParser()
    return _parser_instance


def parse_command(text: str, default_target: str = "小橘") -> Optional[ParsedCommand]:
    """
    便捷函数：解析指令
    
    Args:
        text: 输入文本
        default_target: 默认目标 NPC 名称
        
    Returns:
        ParsedCommand 对象，如果不是指令则返回 None
    """
    return get_command_parser().parse(text, default_target)


# 测试代码
if __name__ == "__main__":
    parser = CommandParser()
    
    test_cases = [
        "小橘，向右走",
        "向左走，直到撞墙",
        "右边",
        "跟着我",
        "小橘，跟着我",
        "停",
        "小绿，停",
        "向东走",
        "一直向左走",
        "你好",  # 不是指令
    ]
    
    print("=== 指令解析测试 ===\n")
    for text in test_cases:
        result = parser.parse(text)
        if result:
            print(f"✓ '{text}' → {result.to_dict()}")
        else:
            print(f"✗ '{text}' → 不是指令")
