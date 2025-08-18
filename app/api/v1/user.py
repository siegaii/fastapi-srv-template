from datetime import datetime, timedelta
from typing import Optional

import hashlib
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import jwt

# 创建路由器
router = APIRouter(prefix="/user", tags=["用户管理"])

# JWT配置
SECRET_KEY = "your-secret-key-here"  # 实际项目中应该从环境变量读取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
    "user@example.com": {
        "id": 2,
        "username": "user",
        "email": "user@example.com",
        "hashed_password": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # 'secret123' 的 SHA256
        "is_active": True,
    },
}


# 数据模型
class LoginRequest(BaseModel):
    """登录请求模型"""

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """登录响应模型"""

    access_token: str
    token_type: str
    user_info: dict


class UserInfo(BaseModel):
    """用户信息模型"""

    id: int
    username: str
    email: str
    is_active: bool


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
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """验证JWT令牌"""
    try:
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭据",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )


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
