"""
ClawGame - 指令解析器单元测试
"""

import pytest
from ai.command_parser import CommandParser, parse_command, ParsedCommand


class TestCommandParser:
    """指令解析器测试"""
    
    @pytest.fixture
    def parser(self):
        """创建解析器实例"""
        return CommandParser()
    
    def test_parser_init(self, parser):
        """测试解析器初始化"""
        assert parser is not None
        assert hasattr(parser, 'parse')
        assert hasattr(parser, 'is_command')
    
    def test_move_with_target(self, parser):
        """测试带目标的移动指令: '小橘，向右走'"""
        result = parser.parse("小橘，向右走")
        assert result is not None
        assert result.type == 'move'
        assert result.target == '小橘'
        assert result.direction == 'right'
        assert result.until is None
    
    def test_move_with_different_targets(self, parser):
        """测试不同目标的移动指令"""
        # 小绿
        result = parser.parse("小绿，向左走")
        assert result.target == '小绿'
        assert result.direction == 'left'
        
        # 小蓝
        result = parser.parse("小蓝，向上走")
        assert result.target == '小蓝'
        assert result.direction == 'up'
    
    def test_move_until_collision(self, parser):
        """测试持续移动直到撞墙: '向左走，直到撞墙'"""
        result = parser.parse("向左走，直到撞墙")
        assert result is not None
        assert result.type == 'move'
        assert result.direction == 'left'
        assert result.until == 'collision'
    
    def test_move_simple(self, parser):
        """测试简单移动: '向右走'"""
        result = parser.parse("向右走")
        assert result is not None
        assert result.type == 'move'
        assert result.direction == 'right'
        assert result.until is None
    
    def test_direction_shorthand(self, parser):
        """测试方向简写: '右边', '左边'"""
        result = parser.parse("右边")
        assert result is not None
        assert result.type == 'move'
        assert result.direction == 'right'
        
        result = parser.parse("左边")
        assert result.direction == 'left'
    
    def test_cardinal_directions(self, parser):
        """测试东南西北方向"""
        result = parser.parse("向东走")
        assert result.direction == 'right'
        
        result = parser.parse("向西走")
        assert result.direction == 'left'
        
        result = parser.parse("向北走")
        assert result.direction == 'up'
        
        result = parser.parse("向南走")
        assert result.direction == 'down'
    
    def test_stop_command(self, parser):
        """测试停止指令"""
        result = parser.parse("停")
        assert result is not None
        assert result.type == 'stop'
        
        result = parser.parse("停下")
        assert result.type == 'stop'
        
        result = parser.parse("停止")
        assert result.type == 'stop'
    
    def test_stop_with_target(self, parser):
        """测试带目标的停止指令"""
        result = parser.parse("小橘，停")
        assert result is not None
        assert result.type == 'stop'
        assert result.target == '小橘'
    
    def test_follow_command(self, parser):
        """测试跟随指令（Phase 2）"""
        result = parser.parse("跟着我")
        assert result is not None
        assert result.type == 'follow'
        
        result = parser.parse("小橘，跟着我")
        assert result.type == 'follow'
        assert result.target == '小橘'
    
    def test_not_a_command(self, parser):
        """测试非指令文本"""
        result = parser.parse("你好")
        assert result is None
        
        result = parser.parse("今天天气怎么样")
        assert result is None
        
        result = parser.parse("小橘，你叫什么名字")
        assert result is None
    
    def test_is_command_method(self, parser):
        """测试 is_command 方法"""
        assert parser.is_command("向右走") is True
        assert parser.is_command("小橘，向左走") is True
        assert parser.is_command("停") is True
        assert parser.is_command("你好") is False
    
    def test_default_target(self, parser):
        """测试默认目标"""
        result = parser.parse("向右走")
        assert result.target == "小橘"  # 默认目标
        
        result = parser.parse("向左走", default_target="小绿")
        assert result.target == "小绿"
    
    def test_to_dict(self, parser):
        """测试 to_dict 方法"""
        result = parser.parse("向右走")
        d = result.to_dict()
        assert isinstance(d, dict)
        assert d['type'] == 'move'
        assert d['direction'] == 'right'
        assert 'raw_text' in d


class TestParseCommandFunction:
    """便捷函数测试"""
    
    def test_parse_command_function(self):
        """测试 parse_command 便捷函数"""
        result = parse_command("向右走")
        assert result is not None
        assert result.type == 'move'
        assert result.direction == 'right'
    
    def test_parse_command_with_default_target(self):
        """测试带默认目标的便捷函数"""
        result = parse_command("向左走", default_target="小蓝")
        assert result.target == "小蓝"


class TestParsedCommand:
    """ParsedCommand 数据类测试"""
    
    def test_parsed_command_creation(self):
        """测试创建 ParsedCommand"""
        cmd = ParsedCommand(
            type='move',
            target='小橘',
            direction='right',
            until='collision',
            raw_text='向右走，直到撞墙'
        )
        assert cmd.type == 'move'
        assert cmd.target == '小橘'
        assert cmd.direction == 'right'
        assert cmd.until == 'collision'
        assert cmd.raw_text == '向右走，直到撞墙'
    
    def test_parsed_command_to_dict(self):
        """测试 to_dict 方法"""
        cmd = ParsedCommand(
            type='stop',
            target='小橘',
            raw_text='停'
        )
        d = cmd.to_dict()
        assert d == {
            'type': 'stop',
            'target': '小橘',
            'direction': None,
            'until': None,
            'raw_text': '停'
        }
