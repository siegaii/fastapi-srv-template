"""用户服务模块

处理用户管理相关的业务逻辑，包括用户认证、用户信息获取等
"""

import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.user import user_crud
from app.models.user import User


class UserService:
    """用户服务类"""

    def __init__(self):
        # JWT配置
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes

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
        """验证JWT令牌，返回用户标识(username)"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
            username: str | None = payload.get("sub")
            if not username:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="无效的认证凭据",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return username

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

    async def authenticate_user(
        self, db: AsyncSession, username: str, password: str
    ) -> Optional[User]:
        """验证用户身份"""
        user = await user_crud.get_user_by_username(db, username)
        if (
            not user
            or not user.is_active
            or not self.verify_password(password, user.hashed_password)
        ):
            return None

        # 更新最后登录时间
        await user_crud.update_last_login(db, user.id)
        return user

    async def get_user_by_username(
        self, db: AsyncSession, username: str
    ) -> Optional[User]:
        """根据用户名获取用户"""
        return await user_crud.get_user_by_username(db, username)

    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return await user_crud.get_user_by_email(db, email)

    async def get_current_user(self, db: AsyncSession, username: str) -> User:
        """获取当前用户，如果用户不存在则抛出异常"""
        user = await self.get_user_by_username(db, username)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="用户不存在或已被禁用"
            )
        return user

    def create_user_login_response(self, user: User) -> dict:
        """创建用户登录响应"""
        # 创建访问令牌
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        # 返回登录响应
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "full_name": user.full_name,
            },
        }

    def get_user_profile(self, user: User) -> dict:
        """获取用户资料"""
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "full_name": user.full_name,
            "phone": user.phone,
            "avatar": user.avatar,
            "bio": user.bio,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_login_at": (
                user.last_login_at.isoformat() if user.last_login_at else None
            ),
        }

    async def login(self, db: AsyncSession, username: str, password: str) -> dict:
        """用户登录"""
        # 验证用户身份
        user = await self.authenticate_user(db, username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # 创建并返回登录响应
        return self.create_user_login_response(user)

    async def register_user(
        self,
        db: AsyncSession,
        username: str,
        password: str,
        full_name: str = None,
    ) -> dict:
        """用户注册"""
        # 检查用户名是否已存在
        if await user_crud.check_username_exists(db, username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在"
            )

        # 创建用户
        hashed_password = self.hash_password(password)
        user = await user_crud.create_user(
            db=db,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True,
            is_superuser=False,
        )

        # 返回用户信息（不包含密码）
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }
