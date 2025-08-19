from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.user import LoginRequest, LoginResponse, UserInfo
from app.services import UserService

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


def get_current_user(username: str = Depends(verify_token)):
    """获取当前用户"""
    return user_service.get_current_user(username)


# API接口
@router.post("/login", response_model=LoginResponse, summary="用户登录")
async def login(login_request: LoginRequest):
    """
    用户登录接口

    - **username**: 用户名
    - **password**: 用户密码

    测试账号:
    - admin / password
    """
    return user_service.login(login_request.username, login_request.password)


@router.get("/profile", response_model=UserInfo, summary="获取用户信息")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
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
