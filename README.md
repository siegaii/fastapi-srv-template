# fastapi-srv-template

## 开发

### 安装 poetry

pip install poetry

### 安装依赖根目录执行

```shell
poetry install --no-root
```

### 设置国内仓库

```shell
poetry source add --priority=primary mirrors https://pypi.tuna.tsinghua.edu.cn/simple/
poetry install --no-root
```

### 开发模式运行

```shell
python run.py
```

## 部署

## 推荐目录结构

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── core/                # 核心配置 & 初始化
│   │   ├── config.py        # 配置文件
│   │   ├── security.py      # 安全相关（JWT/OAuth）
│   │   └── deps.py          # 依赖注入
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/              # 版本化 API
│   │   │   ├── __init__.py
│   │   │   ├── user.py      # 用户路由
│   │   │   └── order.py
│   ├── schemas/             # Pydantic 模型（请求/响应校验）
│   │   ├── user.py
│   │   └── order.py
│   ├── models/              # ORM 模型（SQLAlchemy/Tortoise）
│   │   ├── user.py
│   │   └── order.py
│   ├── crud/                # 数据访问层（面向数据库）
│   │   ├── user.py
│   │   └── order.py
│   ├── services/            # 业务逻辑层
│   │   ├── user_service.py
│   │   └── order_service.py
│   ├── utils/               # 工具模块
│   │   ├── logging.py
│   │   └── exceptions.py
│   └── workers/             # 后台任务/消息队列
│
├── alembic/                 # 数据库迁移（如用 Alembic）
├── tests/                   # 测试用例
├── requirements.txt
└── run.py                   # 入口，调用 `uvicorn app.main:app`

```
