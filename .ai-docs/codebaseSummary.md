# 代码库概览

## 项目结构

```
fastapi-srv-template/
├── .env.example              # 环境变量示例文件
├── .gitignore               # Git 忽略文件配置
├── .trae/                   # Trae IDE 配置目录
│   └── rules/              # 项目开发规则
│       ├── document.mdc    # 文档规范
│       ├── fastapi.mdc     # FastAPI 开发规范
│       ├── git.mdc         # Git 提交规范
│       ├── project_rules.md # 项目通用规范
│       └── python.mdc      # Python 开发规范
├── .ai-docs/               # AI 协作文档目录
│   ├── productIdea.md      # 产品思路
│   ├── techStack.md        # 技术栈文档
│   ├── codebaseSummary.md  # 代码库概览 (本文件)
│   ├── API.md              # 接口文档
│   ├── projectRoadmap.md   # 项目路线图
│   ├── rules.md            # 项目规则
│   ├── currentTask.md      # 当前任务
│   └── tasks/              # 任务中心目录
├── README.md               # 项目说明文档
├── DEPLOYMENT.md           # 部署说明文档
├── pyproject.toml          # Poetry 项目配置文件
├── poetry.lock             # Poetry 依赖锁定文件
├── run.py                  # 应用启动入口
├── docker-compose.yml      # Docker Compose 配置
├── init.sql                # 数据库初始化脚本
├── alembic.ini             # Alembic 数据库迁移配置
├── alembic/                # 数据库迁移目录
│   ├── env.py              # Alembic 环境配置
│   ├── script.py.mako      # 迁移脚本模板
│   └── versions/           # 迁移版本文件
│       └── 19dfe76188cb_initial_migration.py
└── app/                    # 主应用目录
    ├── __init__.py         # 包初始化文件
    ├── main.py             # FastAPI 应用主文件
    ├── core/               # 核心配置模块
    │   ├── config.py       # 应用配置
    │   └── database.py     # 数据库配置
    ├── api/                # API 路由目录
    │   ├── __init__.py     # API 包初始化
    │   └── v1/             # API v1 版本
    │       ├── __init__.py # v1 包初始化
    │       └── user.py     # 用户相关路由
    ├── schemas/            # Pydantic 数据模型
    │   ├── __init__.py     # Schemas 包初始化
    │   └── user.py         # 用户数据模型
    ├── models/             # ORM 数据模型
    │   └── user.py         # 用户数据模型
    ├── crud/               # 数据访问层
    │   └── user.py         # 用户 CRUD 操作
    ├── services/           # 业务逻辑层
    │   ├── __init__.py     # Services 包初始化
    │   └── user_service.py # 用户业务逻辑
    └── utils/              # 工具模块
        └── snowflake.py    # 雪花算法 ID 生成
```

## 核心模块详解

### 应用入口 (`run.py`)
- **功能**: 应用启动脚本
- **职责**: 
  - 加载环境变量
  - 启动 Uvicorn 服务器
  - 配置服务器参数 (host, port, reload)
- **关键特性**: 支持环境变量配置的灵活启动

### 主应用 (`app/main.py`)
- **功能**: FastAPI 应用实例和核心配置
- **职责**:
  - 创建 FastAPI 应用实例
  - 配置应用元数据 (title, description, version)
  - 注册路由模块
  - 定义根路径和示例端点
- **当前路由**:
  - `GET /`: 健康检查端点
  - `GET /items/{item_id}`: 示例参数化端点
  - `/api/v1/user/*`: 用户管理路由组

### API 路由层 (`app/api/`)

#### 用户路由 (`app/api/v1/user.py`)
- **功能**: 用户认证和管理相关的 API 端点
- **核心组件**:
  - **JWT 认证系统**:
    - SECRET_KEY: JWT 签名密钥
    - ALGORITHM: 签名算法 (HS256)
    - ACCESS_TOKEN_EXPIRE_MINUTES: Token 过期时间
  - **安全机制**:
    - HTTPBearer 认证方案
    - 密码 SHA256 哈希
    - Token 验证和解析
  - **模拟数据库**: `fake_users_db` 字典存储用户数据

- **API 端点**:
  - `POST /api/v1/user/login`: 用户登录
    - 输入: LoginRequest (email, password)
    - 输出: LoginResponse (access_token, token_type, user_info)
    - 功能: 验证用户凭据，生成 JWT Token
  
  - `GET /api/v1/user/profile`: 获取用户信息
    - 认证: 需要有效 JWT Token
    - 输出: UserInfo (id, username, email, is_active)
    - 功能: 返回当前认证用户的详细信息
  
  - `POST /api/v1/user/logout`: 用户登出
    - 认证: 需要有效 JWT Token
    - 输出: 成功消息
    - 功能: 客户端 Token 失效提示

- **核心函数**:
  - `hash_password()`: 密码哈希处理
  - `verify_password()`: 密码验证
  - `authenticate_user()`: 用户身份验证
  - `create_access_token()`: JWT Token 生成
  - `verify_token()`: Token 验证和解析
  - `get_current_user()`: 获取当前用户依赖

### 数据模型层 (`app/schemas/`)

#### 用户模型 (`app/schemas/user.py`)
- **功能**: 定义用户相关的 Pydantic 数据模型
- **模型定义**:
  - `LoginRequest`: 登录请求数据验证
    - email: EmailStr (邮箱格式验证)
    - password: str (密码字段)
  
  - `LoginResponse`: 登录响应数据结构
    - access_token: str (JWT Token)
    - token_type: str (Token 类型)
    - user_info: dict (用户信息)
  
  - `UserInfo`: 用户信息数据结构
    - id: int (用户 ID)
    - username: str (用户名)
    - email: str (邮箱地址)
    - is_active: bool (激活状态)

## 配置和环境

### 项目配置 (`pyproject.toml`)
- **项目元数据**: 名称、版本、描述、作者信息
- **Python 版本要求**: >=3.12
- **核心依赖**:
  - fastapi: Web 框架
  - uvicorn: ASGI 服务器
  - load-dotenv: 环境变量加载
  - pyjwt: JWT 处理
  - email-validator: 邮箱验证
- **构建系统**: Poetry Core
- **代码质量配置**: Pylint 规则设置

### 环境变量 (`.env.example`)
- 当前为空，建议包含:
  - `SECRET_KEY`: JWT 签名密钥
  - `ALGORITHM`: JWT 算法
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token 过期时间
  - `HOST`: 服务器主机地址
  - `PORT`: 服务器端口
  - `RELOAD`: 开发模式重载

## 架构特点

### 设计模式
1. **分层架构**: 清晰的职责分离
   - API 层: 路由和请求处理
   - Schema 层: 数据验证和序列化
   - (规划) Service 层: 业务逻辑
   - (规划) CRUD 层: 数据访问
   - (规划) Model 层: 数据模型

2. **依赖注入**: FastAPI 内置 DI 系统
   - 认证依赖: `get_current_user`
   - 安全依赖: `verify_token`

3. **版本化 API**: 支持 API 版本管理
   - 当前版本: v1
   - 路径前缀: `/api/v1`

### 安全实现
1. **JWT 认证流程**:
   - 用户登录 → 验证凭据 → 生成 Token → 返回给客户端
   - 受保护端点 → 验证 Token → 提取用户信息 → 处理请求

2. **密码安全**:
   - SHA256 哈希存储
   - 明文密码不存储
   - 登录时哈希比较

3. **Token 管理**:
   - 可配置过期时间
   - Bearer Token 传输
   - 自动验证和解析

## 扩展点

### 待实现模块
1. **核心配置** (`app/core/`)
   - `config.py`: 应用配置管理
   - `security.py`: 安全相关工具
   - `deps.py`: 通用依赖注入

2. **数据层** (`app/models/`, `app/crud/`)
   - ORM 模型定义
   - 数据库操作抽象
   - 数据访问层实现

3. **业务层** (`app/services/`)
   - 业务逻辑封装
   - 服务间协调
   - 复杂业务流程

4. **工具模块** (`app/utils/`)
   - 日志配置
   - 异常处理
   - 通用工具函数

### 技术债务
1. **硬编码配置**: 部分配置直接写在代码中
2. **模拟数据**: 使用内存字典代替真实数据库
3. **错误处理**: 缺少统一的异常处理机制
4. **日志系统**: 基础日志配置，需要结构化改进
5. **测试覆盖**: 缺少单元测试和集成测试