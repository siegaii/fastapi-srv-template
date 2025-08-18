from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# 用户基础模型
class UserBase(BaseModel):
    """用户基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="用户姓名")
    email: EmailStr = Field(..., description="用户邮箱")
    age: Optional[int] = Field(None, ge=0, le=150, description="用户年龄")

# 创建用户请求模型
class UserCreate(UserBase):
    """创建用户请求模型"""
    pass

# 更新用户请求模型
class UserUpdate(BaseModel):
    """更新用户请求模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="用户姓名")
    email: Optional[EmailStr] = Field(None, description="用户邮箱")
    age: Optional[int] = Field(None, ge=0, le=150, description="用户年龄")

# 用户响应模型
class UserResponse(UserBase):
    """用户响应模型"""
    id: int = Field(..., description="用户ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True

# 用户列表响应模型
class UserListResponse(BaseModel):
    """用户列表响应模型"""
    users: list[UserResponse] = Field(..., description="用户列表")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页大小")

# 通用响应模型
class MessageResponse(BaseModel):
    """通用消息响应模型"""
    message: str = Field(..., description="响应消息")
    success: bool = Field(True, description="操作是否成功")

# 错误响应模型
class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: str = Field(..., description="错误信息")
    detail: Optional[str] = Field(None, description="错误详情")
    success: bool = Field(False, description="操作是否成功")