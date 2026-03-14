"""
测试 NPC 行为解析和 LLM 响应处理
"""

import pytest
from ai.npc_persona import NPCPersona, NPCAction


class TestNPCAction:
    """测试 NPCAction 类"""
    
    def test_parse_json_response_with_action(self):
        """测试解析包含行为的 JSON 响应"""
        llm_response = '''
        {
            "response": "好的，我向右走~",
            "actions": [{"type": "move", "direction": "right", "until": null}]
        }
        '''
        
        result = NPCAction.parse_response(llm_response)
        
        assert result["response"] == "好的，我向右走~"
        assert len(result["actions"]) == 1
        assert result["actions"][0]["type"] == "move"
        assert result["actions"][0]["direction"] == "right"
    
    def test_parse_json_response_with_until_collision(self):
        """测试解析包含持续移动行为的响应"""
        llm_response = '''
        {
            "response": "好的，我一直向左走喵~",
            "actions": [{"type": "move", "direction": "left", "until": "collision"}]
        }
        '''
        
        result = NPCAction.parse_response(llm_response)
        
        assert result["response"] == "好的，我一直向左走喵~"
        assert result["actions"][0]["until"] == "collision"
    
    def test_parse_json_response_stop_action(self):
        """测试解析停止行为"""
        llm_response = '''
        {
            "response": "好的，我停下来~",
            "actions": [{"type": "stop"}]
        }
        '''
        
        result = NPCAction.parse_response(llm_response)
        
        assert result["response"] == "好的，我停下来~"
        assert result["actions"][0]["type"] == "stop"
    
    def test_parse_json_response_multiple_actions(self):
        """测试解析多个行为"""
        llm_response = '''
        {
            "response": "好的~",
            "actions": [
                {"type": "stop"},
                {"type": "move", "direction": "up"}
            ]
        }
        '''
        
        result = NPCAction.parse_response(llm_response)
        
        assert len(result["actions"]) == 2
    
    def test_parse_plain_text_response(self):
        """测试解析纯文本响应（无行为）"""
        llm_response = "喵~ 你好呀~"
        
        result = NPCAction.parse_response(llm_response)
        
        assert result["response"] == "喵~ 你好呀~"
        assert result["actions"] == []
    
    def test_parse_markdown_json_block(self):
        """测试解析 markdown 代码块中的 JSON"""
        llm_response = '''
        ```json
        {
            "response": "好的喵~",
            "actions": [{"type": "move", "direction": "down"}]
        }
        ```
        '''
        
        result = NPCAction.parse_response(llm_response)
        
        assert result["response"] == "好的喵~"
        assert result["actions"][0]["direction"] == "down"
    
    def test_parse_invalid_json_returns_text(self):
        """测试无效 JSON 返回纯文本"""
        llm_response = "这不是 JSON，就是普通对话喵~"
        
        result = NPCAction.parse_response(llm_response)
        
        assert result["response"] == "这不是 JSON，就是普通对话喵~"
        assert result["actions"] == []
    
    def test_parse_partial_json(self):
        """测试部分 JSON（缺少 actions 字段）"""
        llm_response = '{"response": "只是对话~"}'
        
        result = NPCAction.parse_response(llm_response)
        
        assert result["response"] == "只是对话~"
        assert result["actions"] == []


class TestNPCPersona:
    """测试 NPCPersona 类"""
    
    def test_get_system_prompt_with_actions(self):
        """测试获取包含行为能力说明的系统提示词"""
        prompt = NPCPersona.get_system_prompt("小橘", with_actions=True)
        
        assert "小橘" in prompt
        assert "行为能力" in prompt
        assert "move" in prompt
        assert "stop" in prompt
        assert "输出格式" in prompt
    
    def test_get_system_prompt_without_actions(self):
        """测试获取不包含行为能力说明的系统提示词"""
        prompt = NPCPersona.get_system_prompt("小橘", with_actions=False)
        
        assert "小橘" in prompt
        # 不应该包含行为能力说明
        assert "行为能力" not in prompt or len(prompt) < 500
    
    def test_get_system_prompt_default_with_actions(self):
        """测试默认获取包含行为能力说明的系统提示词"""
        prompt = NPCPersona.get_system_prompt("小橘")
        
        assert "行为能力" in prompt
    
    def test_get_available_actions_description(self):
        """测试获取行为描述"""
        desc = NPCAction.get_available_actions_description()
        
        assert "移动" in desc
        assert "停止" in desc
        assert "left" in desc
        assert "right" in desc
    
    def test_get_npc_info(self):
        """测试获取 NPC 信息"""
        info = NPCPersona.get_npc_info("小橘")
        
        assert info["name"] == "小橘"
        assert info["species"] == "橘猫"
    
    def test_get_fallback_response(self):
        """测试获取回退回复"""
        response = NPCPersona.get_fallback_response("小橘")
        
        assert "喵" in response


class TestNPCActionDirections:
    """测试行为方向"""
    
    def test_valid_directions(self):
        """测试有效方向"""
        assert "left" in NPCAction.DIRECTIONS
        assert "right" in NPCAction.DIRECTIONS
        assert "up" in NPCAction.DIRECTIONS
        assert "down" in NPCAction.DIRECTIONS
    
    def test_action_types(self):
        """测试行为类型常量"""
        assert NPCAction.MOVE == "move"
        assert NPCAction.STOP == "stop"
        assert NPCAction.FOLLOW == "follow"


class TestIntegration:
    """集成测试"""
    
    def test_full_flow_simple_dialog(self):
        """测试完整流程：普通对话"""
        # 模拟 LLM 返回纯文本
        llm_response = "喵~ 今天天气真好~"
        
        result = NPCAction.parse_response(llm_response)
        
        assert result["response"] == "喵~ 今天天气真好~"
        assert result["actions"] == []
    
    def test_full_flow_move_command(self):
        """测试完整流程：移动指令"""
        # 模拟 LLM 返回 JSON
        llm_response = '''
        {
            "response": "好的，向右走喵~",
            "actions": [{"type": "move", "direction": "right"}]
        }
        '''
        
        result = NPCAction.parse_response(llm_response)
        
        assert result["response"] == "好的，向右走喵~"
        assert len(result["actions"]) == 1
        assert result["actions"][0]["type"] == "move"
        assert result["actions"][0]["direction"] == "right"
    
    def test_full_flow_continuous_move(self):
        """测试完整流程：持续移动"""
        llm_response = '''
        {
            "response": "好的，一直往左走直到撞墙喵~",
            "actions": [{"type": "move", "direction": "left", "until": "collision"}]
        }
        '''
        
        result = NPCAction.parse_response(llm_response)
        
        assert result["actions"][0]["until"] == "collision"
