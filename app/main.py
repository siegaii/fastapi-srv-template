from typing import Union

from fastapi import FastAPI
from app.api.v1.user import router as user_router

app = FastAPI(
    title="FastAPI 服务模板",
    description="包含用户认证功能的FastAPI服务模板",
    version="1.0.0"
)

# 注册路由
app.include_router(user_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"Hello": "World", "message": "FastAPI服务正在运行"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
