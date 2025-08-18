# FastAPI 服务模版

一个简单、易用的 FastAPI 项目模版，包含完整的项目结构、依赖管理和开发工具配置。

## 🚀 特性

- ✅ **FastAPI** - 现代、快速的 Web 框架
- ✅ **Pydantic** - 数据验证和序列化
- ✅ **Uvicorn** - ASGI 服务器
- ✅ **模块化路由** - 清晰的代码组织结构
- ✅ **类型提示** - 完整的 Python 类型注解
- ✅ **自动文档** - Swagger UI 和 ReDoc
- ✅ **开发工具** - Black、isort、flake8、mypy
- ✅ **环境配置** - 支持环境变量配置
- ✅ **现代依赖管理** - pyproject.toml 配置

## 📁 项目结构

```
fastapi-srv-template/
├── main.py                 # 应用入口文件
├── models.py               # Pydantic 数据模型
├── routers/                # 路由模块
│   ├── __init__.py
│   └── users.py           # 用户相关路由
├── requirements.txt        # 依赖列表
├── pyproject.toml         # 项目配置文件
├── .env.example           # 环境变量示例
└── README.md              # 项目说明
```

## 🛠️ 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd fastapi-srv-template
```

### 2. 创建虚拟环境

```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 使用 conda
conda create -n fastapi-env python=3.11
conda activate fastapi-env
```

### 3. 安装依赖

```bash
# 使用 pip
pip install -r requirements.txt

# 或使用 pip 安装开发依赖
pip install -e ".[dev]"
```

### 4. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，根据需要修改配置
```

### 5. 启动服务

```bash
# 开发模式启动
uvicorn main:app --reload

# 或直接运行
python main.py

# 指定端口启动
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. 访问应用

- **应用首页**: http://localhost:8000
- **API 文档 (Swagger)**: http://localhost:8000/docs
- **API 文档 (ReDoc)**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

## 📚 API 接口

### 用户管理

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/users` | 获取用户列表（支持分页） |
| GET | `/api/v1/users/{user_id}` | 获取单个用户信息 |
| POST | `/api/v1/users` | 创建新用户 |
| PUT | `/api/v1/users/{user_id}` | 更新用户信息 |
| DELETE | `/api/v1/users/{user_id}` | 删除用户 |

### 示例请求

#### 创建用户

```bash
curl -X POST "http://localhost:8000/api/v1/users" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "张三",
       "email": "zhangsan@example.com",
       "age": 25
     }'
```

#### 获取用户列表

```bash
curl "http://localhost:8000/api/v1/users?page=1&size=10"
```

## 🧪 开发工具

### 代码格式化

```bash
# 使用 Black 格式化代码
black .

# 使用 isort 排序导入
isort .
```

### 代码检查

```bash
# 使用 flake8 检查代码风格
flake8 .

# 使用 mypy 进行类型检查
mypy .
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并显示覆盖率
pytest --cov=.
```

## 🔧 配置说明

### 环境变量

项目支持通过环境变量进行配置，主要配置项包括：

- `APP_NAME`: 应用名称
- `HOST`: 服务器主机地址
- `PORT`: 服务器端口
- `ENVIRONMENT`: 运行环境 (development/production)
- `DEBUG`: 是否开启调试模式

详细配置请参考 `.env.example` 文件。

### pyproject.toml

项目使用 `pyproject.toml` 进行现代化的依赖管理和工具配置，包括：

- 项目元数据和依赖
- Black 代码格式化配置
- isort 导入排序配置
- mypy 类型检查配置
- pytest 测试配置

## 🚀 部署

### Docker 部署

```dockerfile
# Dockerfile 示例
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产环境部署

```bash
# 使用 gunicorn + uvicorn workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 联系

如有问题，请通过以下方式联系：

- 邮箱: your.email@example.com
- GitHub: https://github.com/yourusername/fastapi-srv-template