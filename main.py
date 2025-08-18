from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users

# 创建FastAPI应用实例
app = FastAPI(
    title="FastAPI Template",
    description="一个简单的FastAPI模版项目",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(users.router, prefix="/api/v1", tags=["users"])

# 根路径健康检查
@app.get("/")
async def root():
    """根路径健康检查接口"""
    return {
        "message": "FastAPI Template is running!",
        "status": "healthy",
        "version": "1.0.0"
    }

# 健康检查接口
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "message": "Service is running normally"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)