"""
用户服务模块

处理用户管理相关的业务逻辑，包括用户认证、用户信息获取等
"""

import hashlib
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import HTTPException, status


class UserService:
    """用户服务类"""

    def __init__(self):
        # JWT配置
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
        )

        # 模拟用户数据库
        self.fake_users_db = {
            "admin@example.com": {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com",
                "hashed_password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # 'password' 的 SHA256
                "is_active": True,
            },
        }

    def hash_password(self, password: str) -> str:
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return self.hash_password(plain_password) == hashed_password

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """创建访问令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> str:
        """验证JWT令牌，返回email"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="令牌已过期",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

        except jwt.InvalidTokenError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭据",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

    def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        """用户认证"""
        user = self.fake_users_db.get(email)
        if not user:
            return None
        if not self.verify_password(password, user["hashed_password"]):
            return None
        return user

    def get_user_by_email(self, email: str) -> Optional[dict]:
        """根据邮箱获取用户信息"""
        return self.fake_users_db.get(email)

    def get_current_user(self, email: str) -> dict:
        """获取当前用户，如果用户不存在则抛出异常"""
        user = self.get_user_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在"
            )
        return user

    def create_user_login_response(self, user: dict) -> dict:
        """创建用户登录响应数据"""
        # 创建访问令牌
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = self.create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )

        # 返回登录结果
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "is_active": user["is_active"],
            },
        }

    def get_user_profile(self, user: dict) -> dict:
        """获取用户资料信息"""
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "is_active": user["is_active"],
        }

    def login(self, email: str, password: str) -> dict:
        """用户登录"""
        # 验证用户
        user = self.authenticate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 创建并返回登录响应
        return self.create_user_login_response(user)
