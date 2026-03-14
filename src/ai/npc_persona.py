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

【意图理解原则】
**宽松理解用户意图！** 只要有任何指令意图，就执行行为：

✅ **举例应该执行的情况**（有指令意图）：
- "向右走"
- "小橘，一起向上走"
- "球球你了小橘，一直往右滚行吗"
- "能往左边挪一下吗"
- "我们要去右边哦"
- "一起往下走吧"
- "走走走，往那边" → 如果"那边"有指向性，按指向执行；否则询问
- "别站着不动呀，动起来" → 可以随机选方向移动

❌ **举例不应该执行的情况**（完全无指令意图）：
- "你好"
- "今天天气真好"
- "你真可爱"
- "你在干嘛呢"

【意图提取技巧】
1. 寻找方向词：左/右边、上/下、东/西/南/北
2. 寻找动作词：走/移动/滚/跑/动/挪
3. 寻找持续性：一直/持续/不停
4. 忽略修饰语：球球你了/拜托/能不能/我们要/一起
5. 组合理解：即使指令不完整，只要有方向或动作意图，就执行"""
    
    @classmethod
    def parse_response(cls, llm_response: str) -> Dict:
        """
        解析 LLM 响应，提取行为和回复
        
        LLM 统一返回 JSON 格式：
        {
          "response": "对话回复（不能为空）",
          "actions": [{"type": "move", "direction": "right", "until": null}]
        }
        
        - 有指令意图 → actions 包含完整行为信息
        - 无指令意图 → actions 为空数组 []
        
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
示例返回 JSON 格式：
```json
{
  "response": "你的对话回复",
  "actions": [{"type": "move", "direction": "right", "until": null}]
}
```
direction可以为right、left、up、down
until为null或collision

【输出示例】
```json
{
  "response": "喵~ 小橘这就跟你向上走~",
  "actions": [{"type": "move", "direction": "up", "until": null}]
}
```

【判断标准】
- 不论是否有指令意图，都返回JSON，response都不能为空
- 有指令意图 → actions中包含完整的信息
- 完全无指令意图 → actions放空
"""
        
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
