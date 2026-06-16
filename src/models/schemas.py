from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    """统一 API 响应格式"""
    code: int = Field(default=200, description="状态码")
    data: Any = Field(default=None, description="响应数据")
    message: str = Field(default="success", description="消息")


class CausalNode(BaseModel):
    """因果链节点"""
    id: str = Field(description="节点 ID")
    label: str = Field(description="节点标签")
    type: str = Field(default="event", description="节点类型: event/factor/root")
    description: str = Field(default="", description="节点描述")


class CausalEdge(BaseModel):
    """因果链边"""
    source: str = Field(description="源节点 ID")
    target: str = Field(description="目标节点 ID")
    label: str = Field(default="", description="关系标签")
    strength: float = Field(default=1.0, description="因果强度 0-1")


class CausalChain(BaseModel):
    """因果链"""
    nodes: List[CausalNode] = Field(default=[], description="节点列表")
    edges: List[CausalEdge] = Field(default=[], description="边列表")


class TrizContradiction(BaseModel):
    """TRIZ 矛盾"""
    improving_parameter: str = Field(description="改善参数")
    worsening_parameter: str = Field(description="恶化参数")
    description: str = Field(default="", description="矛盾描述")


class TrizPrinciple(BaseModel):
    """TRIZ 创新原理"""
    id: int = Field(description="原理编号")
    name: str = Field(description="原理名称")
    description: str = Field(description="原理描述")
    examples: List[str] = Field(default=[], description="应用示例")


class AnalyzeRequest(BaseModel):
    """分析请求"""
    problem: str = Field(description="问题描述")
    context: str = Field(default="", description="背景信息")
    depth: int = Field(default=3, ge=1, le=5, description="分析深度 1-5")


class AnalyzeResponse(BaseModel):
    """分析响应"""
    problem: str = Field(description="原始问题")
    causal_chain: CausalChain = Field(description="因果链")
    root_causes: List[str] = Field(description="根本原因列表")
    triz_contradictions: List[TrizContradiction] = Field(description="TRIZ 矛盾")
    recommended_principles: List[TrizPrinciple] = Field(description="推荐创新原理")
    solutions: List[str] = Field(description="解决方案建议")


class ContradictionRequest(BaseModel):
    """矛盾分析请求"""
    problem: str = Field(description="问题描述")
    improving: str = Field(description="想要改善的参数")
    worsening: str = Field(description="可能恶化的参数")


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str = Field(default="ok")
    agent: str = Field(default="causal-chain-triz")
    version: str = Field(default="1.0.0")
