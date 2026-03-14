"""
ClawGame - LLM 调用模块
封装智谱 GLM API 调用
"""

import json
import os
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """LLM 配置"""
    api_key: str
    base_url: str
    model: str
    max_tokens: int = 150  # 限制回复长度
    temperature: float = 0.8
    
    @classmethod
    def from_env(cls) -> 'LLMConfig':
        """从环境变量或配置文件加载"""
        # 尝试从配置文件读取
        config_path = os.path.join(
            os.path.dirname(__file__), 
            '..', '..', 'config', 'llm_config.json'
        )
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        
        # 默认配置（智谱 GLM）
        return cls(
            api_key=os.getenv('ZHIPU_API_KEY', ''),
            base_url='https://open.bigmodel.cn/api/paas/v4',
            model='glm-4-flash',  # 使用更快的模型
            max_tokens=150,
            temperature=0.8
        )


class LLMClient:
    """LLM 客户端"""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig.from_env()
    
    def chat(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None
    ) -> str:
        """
        发送对话请求
        
        Args:
            messages: 对话历史 [{"role": "user/assistant", "content": "..."}]
            system_prompt: 系统提示词
            
        Returns:
            AI 回复文本
        """
        # 构建消息列表
        full_messages = []
        
        if system_prompt:
            full_messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        full_messages.extend(messages)
        
        # 调用 API
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.config.model,
            "messages": full_messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data['choices'][0]['message']['content']
            
        except requests.exceptions.Timeout:
            raise Exception("LLM 请求超时")
        except requests.exceptions.RequestException as e:
            raise Exception(f"LLM 请求失败: {e}")
        except (KeyError, IndexError) as e:
            raise Exception(f"LLM 响应解析失败: {e}")


# 单例实例
_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """获取 LLM 客户端单例"""
    global _client
    if _client is None:
        _client = LLMClient()
    return _client
