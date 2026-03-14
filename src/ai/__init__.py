"""
ClawGame - AI 模块
提供 LLM 调用、记忆管理、NPC 人设、指令解析等功能
"""

from .llm_client import LLMClient, LLMConfig, get_llm_client
from .memory import ConversationMemory, ConversationTurn
from .npc_persona import NPCPersona
from .command_parser import CommandParser, ParsedCommand, parse_command, get_command_parser

__all__ = [
    'LLMClient',
    'LLMConfig', 
    'get_llm_client',
    'ConversationMemory',
    'ConversationTurn',
    'NPCPersona',
    'CommandParser',
    'ParsedCommand',
    'parse_command',
    'get_command_parser',
]
