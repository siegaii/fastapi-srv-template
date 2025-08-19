"""数据库连接和会话管理模块"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

from app.core.config import settings

from app.crud.user import user_crud
from app.services.user_service import UserService


class Base(DeclarativeBase):
    """数据库模型基类"""

    metadata = MetaData()


# 创建异步数据库引擎
engine = create_async_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_timeout=settings.db_pool_timeout,
    echo=settings.debug,  # 在调试模式下打印SQL语句
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """获取数据库会话的依赖注入函数"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """初始化数据库表"""
    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)

    # 创建默认超级用户
    await create_default_superuser()


async def close_db():
    """关闭数据库连接"""
    await engine.dispose()


async def create_default_superuser():
    """创建默认超级用户"""

    async with AsyncSessionLocal() as db:
        try:
            # 检查是否已存在超级用户
            existing_admin = await user_crud.get_user_by_username(db, "admin")
            if existing_admin:
                return

            # 创建用户服务实例
            user_service = UserService()

            # 创建超级用户
            hashed_password = user_service.hash_password("admin123")
            await user_crud.create_user(
                db=db,
                username="admin",
                email="admin@example.com",
                hashed_password=hashed_password,
                full_name="系统管理员",
                is_active=True,
                is_superuser=True,
            )

        except Exception as e:
            print(f"创建默认超级用户失败: {e}")
            await db.rollback()
            raise
