# Agent 开发规范

## 项目结构
- `src/` - 后端源代码
- `frontend/` - React 前端
- `tests/` - 测试文件
- `.github/workflows/` - CI/CD 配置

## 代码规范
- Python: PEP 8, 类型注解
- React: Functional Components, Hooks
- 注释: 中文

## API 规范
- 统一响应格式: `{code: int, data: any, message: str}`
- 错误码: 200 成功, 400 参数错误, 500 服务器错误

## TRIZ 分析流程
1. 接收问题描述
2. 识别关键参数和矛盾
3. 构建因果链
4. 映射 TRIZ 矛盾矩阵
5. 推荐创新原理
6. 生成解决方案
