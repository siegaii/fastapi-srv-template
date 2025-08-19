#!/usr/bin/env python3
"""
测试脚本：验证PostgreSQL集成设置

此脚本用于验证：
1. 所有依赖是否正确安装
2. 配置文件是否正确
3. 数据库模型是否正确定义
4. 服务层是否正确实现
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试所有必要的导入"""
    print("🔍 测试导入...")
    
    try:
        # 测试核心依赖
        import fastapi
        import sqlalchemy
        import asyncpg
        import pydantic_settings
        print("✅ 核心依赖导入成功")
        
        # 测试项目模块
        from app.core.config import settings
        from app.core.database import Base, engine, get_db
        from app.models.user import User
        from app.crud.user import user_crud
        from app.services.user_service import UserService
        from app.schemas.user import LoginRequest, LoginResponse, UserInfo
        print("✅ 项目模块导入成功")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_config():
    """测试配置"""
    print("\n🔍 测试配置...")
    
    try:
        from app.core.config import settings
        
        # 检查必要的配置项
        required_configs = [
            'database_url',
            'secret_key',
            'algorithm',
            'access_token_expire_minutes'
        ]
        
        for config in required_configs:
            value = getattr(settings, config, None)
            if value:
                print(f"✅ {config}: 已配置")
            else:
                print(f"❌ {config}: 未配置")
                return False
        
        return True
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def test_database_models():
    """测试数据库模型"""
    print("\n🔍 测试数据库模型...")
    
    try:
        from app.models.user import User
        from app.core.database import Base
        
        # 检查User模型是否正确继承Base
        if issubclass(User, Base):
            print("✅ User模型继承正确")
        else:
            print("❌ User模型继承错误")
            return False
        
        # 检查必要的字段
        required_fields = ['id', 'username', 'email', 'hashed_password']
        for field in required_fields:
            if hasattr(User, field):
                print(f"✅ User.{field}: 字段存在")
            else:
                print(f"❌ User.{field}: 字段缺失")
                return False
        
        return True
    except Exception as e:
        print(f"❌ 数据库模型测试失败: {e}")
        return False

def test_services():
    """测试服务层"""
    print("\n🔍 测试服务层...")
    
    try:
        from app.services.user_service import UserService
        
        service = UserService()
        
        # 检查必要的方法
        required_methods = [
            'hash_password',
            'verify_password',
            'create_access_token',
            'verify_token'
        ]
        
        for method in required_methods:
            if hasattr(service, method):
                print(f"✅ UserService.{method}: 方法存在")
            else:
                print(f"❌ UserService.{method}: 方法缺失")
                return False
        
        # 测试密码哈希
        test_password = "test123"
        hashed = service.hash_password(test_password)
        if service.verify_password(test_password, hashed):
            print("✅ 密码哈希验证正常")
        else:
            print("❌ 密码哈希验证失败")
            return False
        
        return True
    except Exception as e:
        print(f"❌ 服务层测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始PostgreSQL集成设置验证\n")
    
    tests = [
        ("导入测试", test_imports),
        ("配置测试", test_config),
        ("数据库模型测试", test_database_models),
        ("服务层测试", test_services)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"\n❌ {test_name} 失败")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！PostgreSQL集成设置正确。")
        print("\n📋 下一步操作：")
        print("1. 安装Docker Desktop: https://www.docker.com/products/docker-desktop")
        print("2. 启动PostgreSQL: docker compose up -d postgres")
        print("3. 运行应用: python run.py")
        print("4. 测试API: http://localhost:8000/docs")
        return True
    else:
        print("\n❌ 部分测试失败，请检查上述错误。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)