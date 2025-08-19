from datetime import datetime, timedelta, timezone
from typing import Optional
import logging
import os

import hashlib
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter(prefix="/user", tags=["用户管理"])

# JWT配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 安全认证
security = HTTPBearer()

# 模拟用户数据库
fake_users_db = {
    "admin@example.com": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # 'password' 的 SHA256
        "is_active": True,
    },
}


# 工具函数
def hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return hash_password(plain_password) == hashed_password


def authenticate_user(email: str, password: str) -> Optional[dict]:
    """用户认证"""
    user = fake_users_db.get(email)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """验证JWT令牌，返回email"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        email: str | None = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭据",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email

    except jwt.ExpiredSignatureError as exc:
        logger.warning("JWT 令牌已过期: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌已过期",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    except jwt.InvalidTokenError as exc:  # PyJWT 所有 token 错误的基类
        logger.warning("JWT 验证失败: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def get_current_user(email: str = Depends(verify_token)):
    """获取当前用户"""
    user = fake_users_db.get(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在"
        )
    return user


# API接口
@router.post("/login", response_model=LoginResponse, summary="用户登录")
async def login(login_data: LoginRequest):
    """
    用户登录接口

    - **email**: 用户邮箱
    - **password**: 用户密码

    测试账号:
    - admin@example.com / password
    - user@example.com / secret123
    """
    # 验证用户
    user = authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 创建访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )

    # 返回登录结果
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_info={
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "is_active": user["is_active"],
        },
    )


@router.get("/profile", response_model=UserInfo, summary="获取用户信息")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """
    获取当前登录用户的信息

    需要在请求头中携带 Authorization: Bearer <token>
    """
    return UserInfo(
        id=current_user["id"],
        username=current_user["username"],
        email=current_user["email"],
        is_active=current_user["is_active"],
    )


@router.post("/logout", summary="用户登出")
async def logout():
    """
    用户登出接口

    注意：JWT是无状态的，实际项目中可能需要维护黑名单或使用短期令牌
    """
    return {"message": "登出成功"}
