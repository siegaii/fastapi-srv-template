from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from models import UserCreate, UserUpdate, UserResponse, UserListResponse, MessageResponse

# 创建路由器
router = APIRouter()

# 模拟数据库存储（实际项目中应该使用真实数据库）
fake_users_db = [
    {
        "id": 1,
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 25,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 2,
        "name": "李四",
        "email": "lisi@example.com",
        "age": 30,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

# 用于生成新用户ID的计数器
next_user_id = 3


@router.get("/users", response_model=UserListResponse, summary="获取用户列表")
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页大小")
):
    """获取用户列表，支持分页"""
    start_index = (page - 1) * size
    end_index = start_index + size
    
    users_page = fake_users_db[start_index:end_index]
    
    return UserListResponse(
        users=users_page,
        total=len(fake_users_db),
        page=page,
        size=size
    )


@router.get("/users/{user_id}", response_model=UserResponse, summary="获取单个用户")
async def get_user(user_id: int):
    """根据用户ID获取单个用户信息"""
    user = next((user for user in fake_users_db if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.post("/users", response_model=UserResponse, status_code=201, summary="创建用户")
async def create_user(user: UserCreate):
    """创建新用户"""
    global next_user_id
    
    # 检查邮箱是否已存在
    existing_user = next((u for u in fake_users_db if u["email"] == user.email), None)
    if existing_user:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    # 创建新用户
    new_user = {
        "id": next_user_id,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    fake_users_db.append(new_user)
    next_user_id += 1
    
    return new_user


@router.put("/users/{user_id}", response_model=UserResponse, summary="更新用户")
async def update_user(user_id: int, user_update: UserUpdate):
    """更新用户信息"""
    user_index = next((i for i, user in enumerate(fake_users_db) if user["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    user = fake_users_db[user_index]
    
    # 如果更新邮箱，检查是否与其他用户冲突
    if user_update.email and user_update.email != user["email"]:
        existing_user = next((u for u in fake_users_db if u["email"] == user_update.email), None)
        if existing_user:
            raise HTTPException(status_code=400, detail="邮箱已存在")
    
    # 更新用户信息
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        user[field] = value
    
    user["updated_at"] = datetime.now()
    fake_users_db[user_index] = user
    
    return user


@router.delete("/users/{user_id}", response_model=MessageResponse, summary="删除用户")
async def delete_user(user_id: int):
    """删除用户"""
    user_index = next((i for i, user in enumerate(fake_users_db) if user["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    deleted_user = fake_users_db.pop(user_index)
    
    return MessageResponse(
        message=f"用户 {deleted_user['name']} 已成功删除",
        success=True
    )