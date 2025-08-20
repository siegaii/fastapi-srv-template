from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import (
    LoginRequest,
    LoginResponse,
    UserInfo,
    UserRegisterRequest,
    UserRegisterResponse,
)
from app.services.user_service import UserService

# 创建路由器
router = APIRouter(prefix="/user", tags=["用户管理"])

# 安全认证
security = HTTPBearer()

# 创建用户服务实例
user_service = UserService()


# 依赖注入函数
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """验证JWT令牌，返回username"""
    token = credentials.credentials
    return user_service.verify_token(token)


async def get_current_user(
    username: str = Depends(verify_token), db: AsyncSession = Depends(get_db)
):
    """获取当前用户"""
    return await user_service.get_current_user(db, username)


# API接口
@router.post("/login", response_model=LoginResponse, summary="用户登录")
async def login(login_request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    用户登录接口

    - **username**: 用户名
    - **password**: 用户密码

    测试账号:
    - admin / password
    """
    return await user_service.login(db, login_request.username, login_request.password)


@router.get("/profile", response_model=UserInfo, summary="获取用户信息")
async def get_user_profile(current_user=Depends(get_current_user)):
    """
    获取当前登录用户的信息

    需要在请求头中携带 Authorization: Bearer <token>
    """
    profile = user_service.get_user_profile(current_user)
    return UserInfo(**profile)


@router.post("/logout", summary="用户登出")
async def logout():
    """
    用户登出接口

    注意：JWT是无状态的，实际项目中可能需要维护黑名单或使用短期令牌
    """
    return {"message": "登出成功"}


@router.post("/register", response_model=UserRegisterResponse, summary="用户注册")
async def register(
    register_request: UserRegisterRequest, db: AsyncSession = Depends(get_db)
):
    """
    用户注册接口

    - **username**: 用户名（必填，唯一）
    - **email**: 邮箱（必填，唯一）
    - **password**: 密码（必填）
    - **full_name**: 全名（可选）
    """
    user_data = await user_service.register_user(
        db=db,
        username=register_request.username,
        email=register_request.email,
        password=register_request.password,
        full_name=register_request.full_name,
    )

    return UserRegisterResponse(**user_data)
