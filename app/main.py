from typing import Union
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError

from app.api.v1.user import router as user_router
from app.core.database import init_db, close_db
from app.core.exceptions import (
    http_exception_handler,
    starlette_exception_handler,
    validation_exception_handler,
    pydantic_validation_exception_handler,
    general_exception_handler,
)
from app.schemas.base import success_response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    await init_db()
    yield
    # 关闭时清理数据库连接
    await close_db()


app = FastAPI(
    title="FastAPI 服务模板",
    description="包含用户认证功能的FastAPI服务模板",
    version="1.0.0",
    lifespan=lifespan,
)

# 注册异常处理器
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(StarletteHTTPException, starlette_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 注册路由
app.include_router(user_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return success_response(
        data={"Hello": "World", "service": "FastAPI服务模板"},
        msg="服务正在运行"
    )


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return success_response(
        data={"item_id": item_id, "q": q},
        msg="获取数据成功"
    )
