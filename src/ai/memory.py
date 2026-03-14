"""
ClawGame - NPC 记忆管理模块
管理对话历史，实现记忆截断算法
"""

import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ConversationTurn:
    """一轮对话"""
    role: str  # "user" 或 "assistant"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConversationTurn':
        return cls(
            role=data["role"],
            content=data["content"],
            timestamp=data.get("timestamp", datetime.now().isoformat())
        )
    
    def to_message(self) -> Dict[str, str]:
        """转换为 LLM API 格式的消息"""
        return {"role": self.role, "content": self.content}


class ConversationMemory:
    """
    对话记忆管理
    
    特点：
    1. 保存到 JSON 文件
    2. 支持记忆截断（按 token 上限）
    3. 支持最近 N 轮对话
    """
    
    def __init__(
        self, 
        memory_file: str,
        max_tokens: int = 2000,  # 上下文上限
        min_turns: int = 3       # 最少保留轮数
    ):
        """
        初始化记忆管理
        
        Args:
            memory_file: 记忆文件路径
            max_tokens: 最大 token 数（粗略估算：1 token ≈ 1.5 中文字符）
            min_turns: 最少保留的对话轮数
        """
        self.memory_file = memory_file
        self.max_tokens = max_tokens
        self.min_turns = min_turns
        self.conversations: List[ConversationTurn] = []
        
        # 加载已有记忆
        self._load()
    
    def _load(self) -> None:
        """从文件加载记忆"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversations = [
                        ConversationTurn.from_dict(t) for t in data.get("conversations", [])
                    ]
            except Exception as e:
                print(f"[Memory] 加载记忆失败: {e}")
                self.conversations = []
    
    def _save(self) -> None:
        """保存记忆到文件"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump({
                "conversations": [t.to_dict() for t in self.conversations]
            }, f, ensure_ascii=False, indent=2)
    
    def _estimate_tokens(self, text: str) -> int:
        """
        估算文本的 token 数
        
        简单估算：
        - 中文：约 1.5 字符/token
        - 英文：约 4 字符/token
        """
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        other_chars = len(text) - chinese_chars
        return int(chinese_chars / 1.5 + other_chars / 4)
    
    def _get_total_tokens(self, turns: List[ConversationTurn]) -> int:
        """计算对话列表的总 token 数"""
        total = 0
        for turn in turns:
            total += self._estimate_tokens(turn.content)
        return total
    
    def _truncate(self) -> None:
        """
        截断记忆
        
        算法：
        1. 计算当前总 token 数
        2. 如果超过上限，从最早的轮次开始删除
        3. 保留至少 min_turns 轮
        """
        while len(self.conversations) > self.min_turns:
            total = self._get_total_tokens(self.conversations)
            if total <= self.max_tokens:
                break
            
            # 删除最早的一轮
            removed = self.conversations.pop(0)
            print(f"[Memory] 截断记忆，删除: {removed.content[:30]}...")
    
    def add_turn(self, role: str, content: str) -> None:
        """
        添加一轮对话
        
        Args:
            role: "user" 或 "assistant"
            content: 对话内容
        """
        turn = ConversationTurn(role=role, content=content)
        self.conversations.append(turn)
        self._truncate()
        self._save()
    
    def get_messages(self, max_turns: Optional[int] = None) -> List[Dict[str, str]]:
        """
        获取对话历史（转换为 LLM API 格式）
        
        Args:
            max_turns: 最多返回的轮数（None 表示不限制）
            
        Returns:
            消息列表 [{"role": "...", "content": "..."}]
        """
        turns = self.conversations
        if max_turns is not None:
            turns = turns[-max_turns:]
        
        return [t.to_message() for t in turns]
    
    def clear(self) -> None:
        """清空记忆"""
        self.conversations = []
        self._save()
    
    def get_summary(self) -> Dict:
        """获取记忆摘要"""
        return {
            "total_turns": len(self.conversations),
            "total_tokens": self._get_total_tokens(self.conversations),
            "max_tokens": self.max_tokens,
            "last_turn": self.conversations[-1].content[:50] if self.conversations else None
        }
