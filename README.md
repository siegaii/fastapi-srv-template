# FastAPI 服务模板

一个现代化的 Python Web API 开发模板，基于 FastAPI 框架构建，提供开箱即用的项目结构和最佳实践。

## 🚀 特性

- **现代 Python**: 基于 Python 3.12+ 和 FastAPI 框架
- **类型安全**: 全面使用类型提示，提供更好的开发体验
- **异步支持**: 充分利用 Python 异步编程能力
- **数据库集成**: SQLAlchemy 2.0 + PostgreSQL + Alembic 迁移
- **认证系统**: JWT Token 认证机制
- **API 文档**: 自动生成的 Swagger/OpenAPI 文档
- **容器化**: Docker 和 Docker Compose 支持
- **开发工具**: Poetry 依赖管理，代码规范配置

## 📋 系统要求

- Python 3.12+
- Poetry
- PostgreSQL 15+
- Docker 和 Docker Compose

## 🛠️ 安装和设置

### 1. 克隆项目

```bash
git clone <repository-url>
cd fastapi-srv-template
```

### 2. 依赖管理

#### 使用 Poetry (推荐)

```bash
# 安装 Poetry (如果尚未安装)
curl -sSL https://install.python-poetry.org | python3 -

# 安装项目依赖
poetry install

# 激活虚拟环境
poetry shell
```

#### 使用 pip

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 环境变量配置

复制环境变量示例文件并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下变量：

```env
# 应用配置
APP_NAME=FastAPI 服务模板
APP_VERSION=1.0.0
DEBUG=True

# 服务器配置
HOST=127.0.0.1
PORT=8000
RELOAD=True

# JWT 配置
SECRET_KEY=your-super-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 数据库配置
DATABASE_URL=postgresql+asyncpg://fastapi_user:fastapi_password@localhost:5432/fastapi_db
TEST_DATABASE_URL=postgresql+asyncpg://fastapi_user:fastapi_password@localhost:5432/fastapi_test_db

# 数据库连接池配置
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
```

## 🗄️ 数据库设置

### 使用 Docker (推荐)

启动 PostgreSQL 数据库：

```bash
# 启动数据库服务
docker-compose up -d postgres

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs postgres
```

### 手动安装 PostgreSQL

如果不使用 Docker，请手动安装 PostgreSQL 并创建数据库：

```sql
-- 连接到 PostgreSQL
psql -U postgres

-- 创建用户和数据库
CREATE USER fastapi_user WITH PASSWORD 'fastapi_password';
CREATE DATABASE fastapi_db OWNER fastapi_user;
CREATE DATABASE fastapi_test_db OWNER fastapi_user;
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;
GRANT ALL PRIVILEGES ON DATABASE fastapi_test_db TO fastapi_user;
```

## 🔄 数据库迁移

使用 Alembic 进行数据库迁移管理：

```bash
# 初始化迁移 (仅首次)
alembic init alembic

# 创建新的迁移文件
alembic revision --autogenerate -m "描述你的更改"

# 应用迁移
alembic upgrade head

# 查看迁移历史
alembic history

# 回滚到指定版本
alembic downgrade <revision_id>

# 查看当前版本
alembic current
```

### 迁移最佳实践

1. **在修改模型后创建迁移**：

   ```bash
   alembic revision --autogenerate -m "add user table"
   ```

2. **检查生成的迁移文件**：

   - 查看 `alembic/versions/` 目录下的新文件
   - 确认迁移操作正确

3. **应用迁移**：
   ```bash
   alembic upgrade head
   ```

## 🚀 启动项目

### 开发模式

```bash
# 使用 Poetry
poetry run python run.py

# 或直接使用 Python
python run.py

# 或使用 uvicorn
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 生产模式

```bash
# 设置生产环境变量
export DEBUG=False
export RELOAD=False

# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 使用 Docker

```bash
# 构建并启动所有服务
docker-compose up --build

# 后台运行
docker-compose up -d

# 仅启动应用 (需要先启动数据库)
docker-compose up app
```

## 📚 API 文档

启动服务后，可以访问以下地址查看 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 开发和测试

### 代码规范

项目使用 Pylint 进行代码质量检查：

```bash
# 检查代码规范
pylint app/

# 格式化代码 (如果安装了 black)
black app/

# 类型检查 (如果安装了 mypy)
mypy app/
```

### 运行测试

```bash
# 安装测试依赖
poetry add --group dev pytest pytest-asyncio httpx

# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app
```

### 开发工具

- **热重载**: 开发模式下代码变更自动重启
- **调试模式**: 详细的错误信息和堆栈跟踪
- **API 文档**: 实时更新的交互式文档

## 🚢 部署

### Docker 部署

1. **构建镜像**：

   ```bash
   docker build -t fastapi-srv-template .
   ```

2. **运行容器**：

   ```bash
   docker run -p 8000:8000 --env-file .env fastapi-srv-template
   ```

3. **使用 Docker Compose**：
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### 传统部署

1. **安装依赖**：

   ```bash
   pip install -r requirements.txt
   ```

2. **配置环境变量**：

   ```bash
   export DATABASE_URL="postgresql+asyncpg://user:pass@host:port/db"
   export SECRET_KEY="your-production-secret-key"
   ```

3. **运行迁移**：

   ```bash
   alembic upgrade head
   ```

4. **启动服务**：
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### 生产环境注意事项

- 使用强密码和安全的 SECRET_KEY
- 配置 HTTPS 和反向代理 (Nginx)
- 设置适当的日志级别
- 配置监控和健康检查
- 使用环境变量管理敏感信息

## 📁 项目结构

```
fastapi-srv-template/
├── app/                    # 主应用目录
│   ├── main.py            # FastAPI 应用入口
│   ├── core/              # 核心配置
│   │   ├── config.py      # 应用配置
│   │   └── database.py    # 数据库配置
│   ├── api/               # API 路由
│   │   └── v1/           # API v1 版本
│   ├── models/            # ORM 模型
│   ├── schemas/           # Pydantic 模型
│   ├── crud/              # 数据访问层
│   ├── services/          # 业务逻辑层
│   └── utils/             # 工具函数
├── alembic/               # 数据库迁移
├── .ai-docs/              # 项目文档
├── .trae/                 # 开发规则
├── docker-compose.yml     # Docker 配置
├── pyproject.toml         # Poetry 配置
└── README.md              # 项目说明
```

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 常见问题

### Q: 如何更改数据库连接？

A: 修改 `.env` 文件中的 `DATABASE_URL` 变量。

### Q: 如何添加新的 API 端点？

A: 在 `app/api/v1/` 目录下创建新的路由文件，并在 `app/main.py` 中注册。

### Q: 如何自定义配置？

A: 修改 `app/core/config.py` 文件中的 `Settings` 类。

### Q: 数据库迁移失败怎么办？

A: 检查数据库连接，确认迁移文件正确，可以使用 `alembic downgrade` 回滚。

## 📞 支持

如果你遇到问题或有建议，请：

- 查看 [Issues](../../issues) 页面
- 创建新的 Issue
- 查看项目文档 `.ai-docs/` 目录

---

**Happy Coding! 🎉**
