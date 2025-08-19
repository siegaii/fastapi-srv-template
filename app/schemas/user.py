from pydantic import BaseModel, EmailStr


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