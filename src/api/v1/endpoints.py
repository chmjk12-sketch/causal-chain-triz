from typing import Any
from fastapi import APIRouter, HTTPException
from src.models.schemas import (
    ApiResponse, AnalyzeRequest, AnalyzeResponse,
    ContradictionRequest, HealthResponse
)
from src.services.deepseek_service import deepseek_service
from src.services.triz_service import triz_service

router = APIRouter(prefix="/api/v1")


@router.post("/analyze", response_model=ApiResponse)
async def analyze_problem(request: AnalyzeRequest):
    """因果链分析"""
    try:
        result = await deepseek_service.analyze_causal_chain(
            problem=request.problem,
            context=request.context,
            depth=request.depth
        )
        return ApiResponse(code=200, data=result, message="分析成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/triz/contradictions", response_model=ApiResponse)
async def analyze_contradiction(request: ContradictionRequest):
    """TRIZ 矛盾分析"""
    try:
        # 先尝试本地矛盾矩阵
        local_result = triz_service.analyze_contradiction(
            problem=request.problem,
            improving=request.improving,
            worsening=request.worsening
        )

        # 如果本地没有匹配，调用 DeepSeek
        if not local_result["principles"]:
            ai_result = await deepseek_service.analyze_triz_contradictions(
                problem=request.problem,
                improving=request.improving,
                worsening=request.worsening
            )
            return ApiResponse(code=200, data=ai_result, message="AI 分析成功")

        return ApiResponse(code=200, data=local_result, message="分析成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/triz/principles", response_model=ApiResponse)
async def get_principles():
    """获取所有 TRIZ 创新原理"""
    principles = triz_service.get_all_principles()
    return ApiResponse(code=200, data=principles, message="获取成功")


@router.get("/triz/parameters", response_model=ApiResponse)
async def get_parameters():
    """获取所有 TRIZ 工程参数"""
    parameters = triz_service.get_all_parameters()
    return ApiResponse(code=200, data=parameters, message="获取成功")
