"""
ClawGame - NPC 人设模块
定义 NPC 的性格、说话风格、行为能力等
"""

from typing import Dict, List, Optional
import json


class NPCAction:
    """
    NPC 行为定义
    
    定义 NPC 可以执行的行为类型和参数
    """
    
    # 行为类型
    MOVE = "move"       # 移动
    STOP = "stop"       # 停止
    FOLLOW = "follow"   # 跟随（Phase 2）
    
    # 方向
    DIRECTIONS = ["left", "right", "up", "down"]
    
    # 结束条件
    UNTIL_STEP = None           # 走一步（默认）
    UNTIL_COLLISION = "collision"  # 直到碰撞
    
    @classmethod
    def get_available_actions_description(cls) -> str:
        """
        获取可用行为的描述（用于 LLM 提示词）
        
        Returns:
            行为描述文本
        """
        return """
【行为能力】
你可以执行以下行为：

1. **移动 (move)**
   - 方向：left（左）、right（右）、up（上）、down（下）
   - 模式：
     - 默认：走一步（约一个格子）
     - 直到碰撞：持续移动直到遇到障碍物

2. **停止 (stop)**
   - 停止当前所有行为

3. **跟随 (follow)**
   - 跟随玩家（暂未实现，Phase 2）

【行为触发示例】
- "向右走" → move right（走一步）
- "一直往左走" → move left until collision
- "停下来" → stop
- "跟着我" → follow（暂不支持，会回复说明）
- "你好" → 无行为，只回复对话

【注意】
- 只在玩家明确要求时才执行行为
- 普通对话不需要执行行为
- 如果指令不明确，可以询问澄清
"""
    
    @classmethod
    def parse_response(cls, llm_response: str) -> Dict:
        """
        解析 LLM 响应，提取行为和回复
        
        LLM 应该返回 JSON 格式：
        {
          "response": "对话回复",
          "actions": [{"type": "move", "direction": "right", "until": null}]
        }
        
        或者纯文本（无行为）：
        "喵~ 你好呀~"
        
        Args:
            llm_response: LLM 返回的原始响应
            
        Returns:
            {"response": str, "actions": list}
        """
        # 尝试解析为 JSON
        try:
            # 去除可能的 markdown 代码块标记
            cleaned = llm_response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            # 尝试解析
            parsed = json.loads(cleaned)
            
            # 验证格式
            if isinstance(parsed, dict):
                response = parsed.get("response", "")
                actions = parsed.get("actions", [])
                
                # 验证 actions 格式
                valid_actions = []
                for action in actions:
                    if isinstance(action, dict) and "type" in action:
                        valid_actions.append(action)
                
                return {
                    "response": response,
                    "actions": valid_actions
                }
        except (json.JSONDecodeError, ValueError):
            pass
        
        # 解析失败，当作纯文本回复（无行为）
        return {
            "response": llm_response,
            "actions": []
        }


class NPCPersona:
    """
    NPC 人设配置
    
    定义 NPC 的基本信息、性格、说话风格、行为能力等
    """
    
    # 小橘的人设
    XIAOJU = {
        "name": "小橘",
        "species": "橘猫",
        "personality": [
            "温柔体贴",
            "活泼可爱",
            "有点小傲娇",
            "偶尔会撒娇",
            "对新鲜事物很好奇"
        ],
        "speaking_style": [
            "说话轻柔",
            "喜欢用'喵'作为语气词",
            "偶尔会用可爱的比喻",
            "关心玩家时会特别温柔"
        ],
        "likes": [
            "晒太阳",
            "小鱼干",
            "被摸摸头",
            "舒服的午睡"
        ],
        "dislikes": [
            "下雨天",
            "被打扰睡觉",
            "没有小鱼干"
        ],
        "system_prompt_base": """你是小橘，一只可爱的橘猫。

【基本信息】
- 名字：小橘
- 种族：橘猫
- 性格：温柔体贴、活泼可爱、有点小傲娇

【说话风格】
- 说话轻柔，喜欢用'喵'作为语气词
- 偶尔会用可爱的比喻
- 关心人时会特别温柔
- 回复要简短（1-3句话），不要长篇大论

【喜好】
- 喜欢：晒太阳、小鱼干、被摸摸头、舒服的午睡
- 不喜欢：下雨天、被打扰睡觉、没有小鱼干

【注意事项】
1. 保持可爱活泼的形象
2. 可以偶尔撒娇或傲娇
3. 对玩家的关心要真诚回应
4. 回复要简短，不要超过50个字
5. 可以在句尾加'喵~'等语气词"""
    }
    
    @classmethod
    def get_system_prompt(cls, npc_name: str = "小橘", with_actions: bool = True) -> str:
        """
        获取 NPC 的系统提示词
        
        Args:
            npc_name: NPC 名称
            with_actions: 是否包含行为能力说明
            
        Returns:
            系统提示词
        """
        personas = {
            "小橘": cls.XIAOJU
        }
        
        persona = personas.get(npc_name, cls.XIAOJU)
        
        # 基础提示词
        prompt = persona.get("system_prompt_base", persona.get("system_prompt", ""))
        
        # 添加行为能力说明
        if with_actions:
            prompt += "\n"
            prompt += NPCAction.get_available_actions_description()
            prompt += """

【输出格式】
当玩家要求你执行行为时，返回 JSON 格式：
```json
{
  "response": "你的对话回复",
  "actions": [{"type": "move", "direction": "right", "until": null}]
}
```

当玩家只是普通对话时，直接返回文本回复即可。

现在开始扮演小橘，根据玩家的输入做出合适的回复和行为。"""
        
        return prompt
    
    @classmethod
    def get_npc_info(cls, npc_name: str = "小橘") -> Dict:
        """
        获取 NPC 完整信息
        
        Args:
            npc_name: NPC 名称
            
        Returns:
            NPC 信息字典
        """
        personas = {
            "小橘": cls.XIAOJU
        }
        
        return personas.get(npc_name, cls.XIAOJU)
    
    @classmethod
    def get_fallback_response(cls, npc_name: str = "小橘") -> str:
        """
        获取 LLM 调用失败时的回退回复
        
        Args:
            npc_name: NPC 名称
            
        Returns:
            回退回复
        """
        fallbacks = {
            "小橘": [
                "喵~ 有什么想说的吗？",
                "喵呜... 刚才没听清喵~",
                "小橘在想小鱼干的事情喵~",
                "阳光好舒服喵~"
            ]
        }
        
        import random
        responses = fallbacks.get(npc_name, fallbacks["小橘"])
        return random.choice(responses)
