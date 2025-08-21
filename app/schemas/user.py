from typing import Optional

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """登录请求模型"""

    username: str
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
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    created_at: Optional[str] = None
    last_login_at: Optional[str] = None


class UserCreate(BaseModel):
    """用户创建模型"""

    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False


class UserUpdate(BaseModel):
    """用户更新模型"""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None


class UserRegisterRequest(BaseModel):
    """用户注册请求模型"""

    username: str
    email: Optional[EmailStr] = None
    password: str
    full_name: Optional[str] = None


class UserRegisterResponse(BaseModel):
    """用户注册响应模型"""

    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: Optional[str] = None
    message: str = "用户注册成功"
