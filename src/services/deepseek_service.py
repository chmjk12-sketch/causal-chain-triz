import json
import httpx
from typing import List, Dict, Any
from src.config import settings


class DeepSeekService:
    """DeepSeek AI 服务"""

    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_url = settings.DEEPSEEK_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def analyze_causal_chain(self, problem: str, context: str = "", depth: int = 3) -> Dict[str, Any]:
        """使用 DeepSeek 分析因果链"""
        prompt = self._build_causal_prompt(problem, context, depth)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "你是一个专业的因果链分析专家，擅长使用 TRIZ 理论解决问题。请用中文回复。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 4000
                },
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return self._parse_causal_response(content)

    async def analyze_triz_contradictions(self, problem: str, improving: str, worsening: str) -> Dict[str, Any]:
        """分析 TRIZ 矛盾"""
        prompt = f"""
请分析以下问题中的 TRIZ 技术矛盾，并推荐创新原理。

问题: {problem}
想要改善的参数: {improving}
可能恶化的参数: {worsening}

请按以下 JSON 格式返回:
{{
    "contradictions": [
        {{
            "improving_parameter": "改善参数名称",
            "worsening_parameter": "恶化参数名称",
            "description": "矛盾描述"
        }}
    ],
    "principles": [
        {{
            "id": 1,
            "name": "原理名称",
            "description": "原理描述",
            "examples": ["示例1", "示例2"]
        }}
    ],
    "solutions": ["解决方案1", "解决方案2"]
}}
"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "你是 TRIZ 理论专家。请用中文回复，只返回 JSON 格式。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.5,
                    "max_tokens": 3000
                },
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return self._parse_json_response(content)

    def _build_causal_prompt(self, problem: str, context: str, depth: int) -> str:
        """构建因果分析提示词"""
        return f"""
请对以下问题进行深入的因果链分析，并结合 TRIZ 理论提供创新解决方案。

问题: {problem}
背景: {context}
分析深度: {depth} 层

请按以下 JSON 格式返回分析结果:
{{
    "causal_chain": {{
        "nodes": [
            {{"id": "1", "label": "问题", "type": "event", "description": "..."}},
            {{"id": "2", "label": "原因1", "type": "factor", "description": "..."}},
            {{"id": "3", "label": "根本原因", "type": "root", "description": "..."}}
        ],
        "edges": [
            {{"source": "2", "target": "1", "label": "导致", "strength": 0.9}},
            {{"source": "3", "target": "2", "label": "引发", "strength": 0.8}}
        ]
    }},
    "root_causes": ["根本原因1", "根本原因2"],
    "triz_contradictions": [
        {{
            "improving_parameter": "改善参数",
            "worsening_parameter": "恶化参数",
            "description": "矛盾描述"
        }}
    ],
    "recommended_principles": [
        {{
            "id": 1,
            "name": "分割原理",
            "description": "将物体分成独立的部分",
            "examples": ["示例1"]
        }}
    ],
    "solutions": ["解决方案1", "解决方案2"]
}}

注意:
1. 节点和边的数量要足够展示完整的因果链
2. 根本原因要追溯到最深层次
3. TRIZ 矛盾要准确识别
4. 创新原理要有针对性
5. 解决方案要具体可行
"""

    def _parse_causal_response(self, content: str) -> Dict[str, Any]:
        """解析因果分析响应"""
        return self._parse_json_response(content)

    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """解析 JSON 响应"""
        # 尝试提取 JSON 部分
        try:
            # 查找 JSON 代码块
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content.strip()
            return json.loads(json_str)
        except (json.JSONDecodeError, IndexError):
            # 如果解析失败，返回原始内容
            return {"raw_content": content}


deepseek_service = DeepSeekService()
