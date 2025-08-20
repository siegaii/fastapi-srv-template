# 技术栈文档

## 核心技术栈

### 后端框架
- **FastAPI (>=0.116.1)**: 现代、快速的 Python Web 框架
  - 自动 API 文档生成 (Swagger/OpenAPI)
  - 基于标准 Python 类型提示的数据验证
  - 高性能异步支持
  - 内置依赖注入系统

### Python 版本
- **Python 3.12+**: 项目要求的最低 Python 版本
  - 利用最新的 Python 特性和性能优化
  - 更好的类型系统支持
  - 改进的错误消息

### 依赖管理
- **Poetry**: 现代 Python 依赖管理和打包工具
  - 依赖解析和锁定
  - 虚拟环境管理
  - 项目打包和发布
  - 配置文件: `pyproject.toml`

### Web 服务器
- **Uvicorn (>=0.35.0)**: ASGI 服务器
  - 高性能异步服务器
  - 支持 WebSocket
  - 热重载开发模式
  - 生产环境优化

## 核心依赖库

### 认证和安全
- **PyJWT (>=2.8.0)**: JSON Web Token 实现
  - Token 生成和验证
  - 支持多种算法 (HS256, RS256 等)
  - 过期时间管理

- **email-validator (>=2.0.0)**: 邮箱地址验证
  - 符合 RFC 标准的邮箱验证
  - 与 Pydantic 集成

### 数据库和 ORM
- **SQLAlchemy (>=2.0.0)**: Python SQL 工具包和 ORM
  - 异步支持 (AsyncSession)
  - 声明式模型定义
  - 查询构建器和原生 SQL 支持
  - 连接池管理

- **AsyncPG (>=0.29.0)**: PostgreSQL 异步驱动
  - 高性能异步 PostgreSQL 连接
  - 与 SQLAlchemy 完美集成
  - 支持连接池和事务

- **Alembic (>=1.13.0)**: 数据库迁移工具
  - 版本化数据库 schema 管理
  - 自动迁移脚本生成
  - 支持多环境配置

### 配置管理
- **Pydantic Settings (>=2.0.0)**: 现代配置管理
  - 基于 Pydantic 的设置验证
  - 环境变量自动映射
  - 类型安全的配置

- **python-dotenv (load-dotenv)**: 环境变量管理
  - `.env` 文件支持
  - 开发/生产环境配置分离

## 开发工具和配置

### 代码质量
- **Pylint**: Python 代码静态分析
  - 配置最大行长度: 150
  - 禁用文档字符串检查 (适合快速开发)
  - 代码风格检查

### 包源配置
- **清华大学 PyPI 镜像**: 国内加速源
  - URL: `https://pypi.tuna.tsinghua.edu.cn/simple/`
  - 提高依赖安装速度

## 项目架构模式

### 分层架构
```
app/
├── main.py              # 应用入口点
├── api/                 # API 路由层
│   └── v1/             # API 版本化
├── schemas/            # 数据验证层 (Pydantic)
├── models/             # 数据模型层 (ORM)
├── crud/               # 数据访问层
├── services/           # 业务逻辑层
├── core/               # 核心配置
└── utils/              # 工具函数
```

### 设计模式
- **依赖注入**: FastAPI 内置 DI 系统
- **Repository 模式**: CRUD 层抽象数据访问
- **Service 模式**: 业务逻辑封装
- **Schema 模式**: 请求/响应数据验证

## 安全机制

### 认证方式
- **JWT Bearer Token**: 无状态认证
- **密码哈希**: SHA256 哈希存储
- **Token 过期**: 可配置的过期时间

### 安全配置
- 环境变量存储敏感信息
- HTTPS 支持 (生产环境)
- CORS 配置
- 请求验证和清理

## 开发环境

### 本地开发
- **热重载**: 代码变更自动重启
- **调试模式**: 详细错误信息
- **API 文档**: 自动生成的交互式文档

### 环境配置
- `.env` 文件配置
- 开发/生产环境分离
- 可配置的服务器参数

## 扩展计划

### 数据库支持
- **SQLAlchemy**: ORM 框架
- **Alembic**: 数据库迁移
- **PostgreSQL/MySQL**: 生产数据库
- **SQLite**: 开发测试数据库

### 缓存和队列
- **Redis**: 缓存和会话存储
- **Celery**: 异步任务队列
- **RabbitMQ/Redis**: 消息代理

### 监控和日志
- **Prometheus**: 指标收集
- **Grafana**: 监控面板
- **Sentry**: 错误追踪
- **Structured Logging**: 结构化日志

### 部署和运维
- **Docker**: 容器化部署
- **Kubernetes**: 容器编排
- **GitHub Actions**: CI/CD 流水线
- **Nginx**: 反向代理和负载均衡