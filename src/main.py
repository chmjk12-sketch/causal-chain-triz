import os
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, FileResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from src.config import settings
from src.api.v1.router import router as api_router
from src.models.schemas import HealthResponse, ApiResponse

app = FastAPI(
    title="因果链分析 Agent",
    description="深挖分析问题背后的因果关系，并结合 TRIZ 理论提供创新解决方案",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router)

# 前端构建产物路径
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
index_html = os.path.join(frontend_dir, "index.html")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    return HealthResponse(status="ok", agent=settings.AGENT_SLUG, version="1.0.0")


@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    """Prometheus 监控指标"""
    return PlainTextResponse(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/mcp/tools", response_model=ApiResponse)
async def list_tools():
    """MCP 工具列表"""
    tools = [
        {
            "name": "causal_chain_analyze",
            "description": "因果链分析：深挖问题背后的因果关系",
            "parameters": {
                "problem": "问题描述（必填）",
                "context": "背景信息（可选）",
                "depth": "分析深度 1-5（可选，默认3）"
            }
        },
        {
            "name": "triz_contradiction_analyze",
            "description": "TRIZ 矛盾分析：识别技术矛盾并推荐创新原理",
            "parameters": {
                "problem": "问题描述（必填）",
                "improving": "想要改善的参数（必填）",
                "worsening": "可能恶化的参数（必填）"
            }
        },
        {
            "name": "get_triz_principles",
            "description": "获取 TRIZ 40 个创新原理列表",
            "parameters": {}
        }
    ]
    return ApiResponse(code=200, data=tools, message="获取成功")


@app.get("/{full_path:path}", include_in_schema=False)
async def serve_frontend(full_path: str):
    """SPA 前端路由（所有非 API 请求返回 index.html）"""
    if not os.path.exists(index_html):
        return {"status": "frontend not built"}
    
    # 检查是否有对应静态文件
    static_file = os.path.join(frontend_dir, full_path)
    if os.path.isfile(static_file):
        return FileResponse(static_file)
    
    # SPA 路由：返回 index.html
    return FileResponse(index_html)


@app.on_event("startup")
async def register_agent():
    """注册 Agent 到控制平面"""
    if settings.CP_API_KEY and settings.CP_BASE_URL:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{settings.CP_BASE_URL}/api/agents/register",
                    headers={"Authorization": f"Bearer {settings.CP_API_KEY}"},
                    json={
                        "slug": settings.AGENT_SLUG,
                        "endpoint": f"http://{settings.AGENT_SLUG}_app:80"
                    },
                    timeout=10.0
                )
        except Exception as e:
            print(f"Agent 注册失败: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )
