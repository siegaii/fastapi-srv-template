"""用户CRUD操作模块"""

from datetime import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.utils.snowflake import snowflake_generator


class UserCRUD:
    """用户CRUD操作类"""

    async def create_user(
        self,
        db: AsyncSession,
        username: str,
        email: str,
        hashed_password: str,
        full_name: Optional[str] = None,
        is_active: bool = True,
        is_superuser: bool = False,
    ) -> User:
        """创建用户"""
        db_user = User(
            id=snowflake_generator.generate(),
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=is_active,
            is_superuser=is_superuser,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_username(
        self, db: AsyncSession, username: str
    ) -> Optional[User]:
        """根据用户名获取用户"""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def update_user(
        self, db: AsyncSession, user_id: int, **kwargs
    ) -> Optional[User]:
        """更新用户信息"""
        # 过滤掉None值
        update_data = {k: v for k, v in kwargs.items() if v is not None}

        if not update_data:
            return await self.get_user_by_id(db, user_id)

        # 添加更新时间
        update_data["updated_at"] = datetime.utcnow()

        await db.execute(update(User).where(User.id == user_id).values(**update_data))
        await db.commit()

        return await self.get_user_by_id(db, user_id)

    async def update_last_login(self, db: AsyncSession, user_id: int) -> None:
        """更新最后登录时间"""
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(last_login_at=datetime.utcnow())
        )
        await db.commit()

    async def delete_user(self, db: AsyncSession, user_id: int) -> bool:
        """删除用户"""
        user = await self.get_user_by_id(db, user_id)
        if user:
            await db.delete(user)
            await db.commit()
            return True
        return False

    async def activate_user(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """激活用户"""
        return await self.update_user(db, user_id, is_active=True)

    async def deactivate_user(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """停用用户"""
        return await self.update_user(db, user_id, is_active=False)

    async def check_username_exists(self, db: AsyncSession, username: str) -> bool:
        """检查用户名是否存在"""
        user = await self.get_user_by_username(db, username)
        return user is not None

    async def check_email_exists(self, db: AsyncSession, email: str) -> bool:
        """检查邮箱是否存在"""
        user = await self.get_user_by_email(db, email)
        return user is not None


# 创建全局CRUD实例
user_crud = UserCRUD()
