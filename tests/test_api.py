import pytest
import respx
from httpx import Response


def test_mcp_tools(client):
    """测试 MCP 工具列表"""
    response = client.get("/mcp/tools")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert len(data["data"]) > 0
    assert data["data"][0]["name"] == "causal_chain_analyze"


def test_get_principles(client):
    """测试获取 TRIZ 原理"""
    response = client.get("/api/v1/triz/principles")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert len(data["data"]) == 40


def test_get_parameters(client):
    """测试获取 TRIZ 参数"""
    response = client.get("/api/v1/triz/parameters")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert len(data["data"]) == 39


def test_analyze_contradiction_local(client):
    """测试本地矛盾分析"""
    payload = {
        "problem": "测试问题",
        "improving": "速度",
        "worsening": "运动物体的重量"
    }
    response = client.post("/api/v1/triz/contradictions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert len(data["data"]["principles"]) > 0


@respx.mock
def test_analyze_causal_chain(client):
    """测试因果链分析（模拟 DeepSeek）"""
    # 模拟 DeepSeek API 响应
    mock_response = {
        "choices": [{
            "message": {
                "content": """
                ```json
                {
                    "causal_chain": {
                        "nodes": [
                            {"id": "1", "label": "产品故障", "type": "event", "description": "..."},
                            {"id": "2", "label": "温度过高", "type": "factor", "description": "..."}
                        ],
                        "edges": [
                            {"source": "2", "target": "1", "label": "导致", "strength": 0.9}
                        ]
                    },
                    "root_causes": ["散热设计不足"],
                    "triz_contradictions": [
                        {"improving_parameter": "可靠性", "worsening_parameter": "成本", "description": "..."}
                    ],
                    "recommended_principles": [
                        {"id": 1, "name": "分割", "description": "...", "examples": []}
                    ],
                    "solutions": ["改进散热设计"]
                }
                ```
                """
            }
        }]
    }

    route = respx.post("https://api.deepseek.com/v1/chat/completions").mock(
        return_value=Response(200, json=mock_response)
    )

    payload = {
        "problem": "产品在高温下故障",
        "context": "工业环境",
        "depth": 3
    }
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "causal_chain" in data["data"]
    assert route.called
