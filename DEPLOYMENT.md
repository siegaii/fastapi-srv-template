# PostgreSQL Docker 部署指南

本指南将帮助您完成 FastAPI 项目与 PostgreSQL 数据库的完整部署。

## 🎯 当前状态

✅ **已完成的工作：**

- PostgreSQL 15 Docker 配置
- 数据库连接和配置管理
- 用户数据模型设计
- CRUD 操作实现
- 用户服务层集成
- 代码验证测试

## 📋 部署步骤

### 1. 安装 Docker Desktop

**macOS:**

```bash
# 方法1: 直接下载安装
# 访问 https://www.docker.com/products/docker-desktop
# 下载并安装 Docker Desktop for Mac

# 方法2: 使用 Homebrew（如果已安装）
brew install --cask docker
```

**验证安装：**

```bash
docker --version
docker compose version
```

### 2. 启动 PostgreSQL 数据库

```bash
# 在项目根目录执行
docker compose up -d postgres

# 查看容器状态
docker compose ps

# 查看数据库日志
docker compose logs postgres
```

### 3. 验证数据库连接

```bash
# 运行验证脚本
poetry run python test_setup.py

# 应该看到所有测试通过的消息
```

### 4. 启动 FastAPI 应用

```bash
# 方法1: 使用 Poetry
poetry run python run.py

# 方法2: 直接运行
python run.py
```

### 5. 测试 API 功能

**访问 API 文档：**

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**测试用户登录：**

```bash
# 使用 curl 测试（需要先创建用户）
curl -X POST "http://localhost:8000/api/v1/user/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "password"}'
```

## 🔧 配置说明

### 环境变量配置 (.env)

```env
# 服务器配置
PORT=8000
HOST=127.0.0.1
RELOAD=True

# JWT 配置
SECRET_KEY=coxie-secret-key
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

### Docker Compose 配置

数据库服务配置在 `docker-compose.yml` 中：

- **镜像**: PostgreSQL 15 Alpine
- **端口**: 5432
- **数据库**: fastapi_db
- **用户**: fastapi_user
- **密码**: fastapi_password

## 🗄️ 数据库管理

### 连接数据库

```bash
# 使用 Docker 连接
docker compose exec postgres psql -U fastapi_user -d fastapi_db

# 或使用外部工具连接
# Host: localhost
# Port: 5432
# Database: fastapi_db
# Username: fastapi_user
# Password: fastapi_password
```

### 查看用户表

```sql
-- 连接数据库后执行
\dt  -- 查看所有表
\d users  -- 查看用户表结构
SELECT * FROM users;  -- 查看用户数据
```

### 创建测试用户

```sql
-- 插入测试用户（密码已哈希）
INSERT INTO users (username, email, hashed_password, is_active, full_name)
VALUES (
    'admin',
    'admin@example.com',
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',  -- 密码: password
    true,
    'Administrator'
);
```

## 🚀 生产部署建议

### 安全配置

1. **更改默认密码**：

   ```env
   SECRET_KEY=your-super-secret-key-here
   POSTGRES_PASSWORD=your-secure-database-password
   ```

2. **使用环境变量**：

   - 不要在代码中硬编码敏感信息
   - 使用 `.env` 文件管理配置

3. **数据库安全**：
   - 限制数据库访问权限
   - 使用 SSL 连接
   - 定期备份数据

### 性能优化

1. **连接池配置**：

   ```env
   DB_POOL_SIZE=20
   DB_MAX_OVERFLOW=40
   DB_POOL_TIMEOUT=60
   ```

2. **数据库索引**：
   - 用户名和邮箱已自动创建索引
   - 根据查询模式添加额外索引

## 🔍 故障排除

### 常见问题

1. **Docker 未启动**：

   ```bash
   # 启动 Docker Desktop
   open -a Docker
   ```

2. **端口冲突**：

   ```bash
   # 检查端口占用
   lsof -i :5432
   lsof -i :8000
   ```

3. **数据库连接失败**：

   ```bash
   # 检查容器状态
   docker compose ps
   docker compose logs postgres
   ```

4. **依赖安装问题**：
   ```bash
   # 重新安装依赖
   poetry install --no-root
   ```

### 日志查看

```bash
# 应用日志
poetry run python run.py

# 数据库日志
docker compose logs -f postgres

# 所有服务日志
docker compose logs -f
```

## 📚 相关文档

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [PostgreSQL 文档](https://www.postgresql.org/docs/)
- [Docker Compose 文档](https://docs.docker.com/compose/)

---

🎉 **恭喜！** 您已成功完成 FastAPI + PostgreSQL 的集成部署！
