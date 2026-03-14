"""
ClawGame - AI 模块
提供 LLM 调用、记忆管理、NPC 人设等功能
"""

from .llm_client import LLMClient, LLMConfig, get_llm_client
from .memory import ConversationMemory, ConversationTurn
from .npc_persona import NPCPersona

__all__ = [
    'LLMClient',
    'LLMConfig', 
    'get_llm_client',
    'ConversationMemory',
    'ConversationTurn',
    'NPCPersona'
]
