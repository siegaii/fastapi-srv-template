# API 接口文档

## 基础信息

- **基础 URL**: `http://localhost:8000` (开发环境)
- **API 版本**: v1
- **API 前缀**: `/api/v1`
- **认证方式**: JWT Bearer Token
- **内容类型**: `application/json`

## 认证说明

### JWT Token 认证
- **Token 类型**: Bearer Token
- **Header 格式**: `Authorization: Bearer <access_token>`
- **Token 过期时间**: 30 分钟 (可配置)
- **算法**: HS256

### 获取 Token
通过 `/api/v1/user/login` 端点登录获取 access_token

## API 端点

### 1. 健康检查

#### GET `/`
**描述**: 服务健康检查端点

**请求**:
- 方法: GET
- 认证: 无需认证
- 参数: 无

**响应**:
```json
{
  "Hello": "World",
  "message": "FastAPI服务正在运行"
}
```

**状态码**:
- `200`: 服务正常运行

---

### 2. 示例端点

#### GET `/items/{item_id}`
**描述**: 获取指定 ID 的项目信息 (示例端点)

**请求**:
- 方法: GET
- 认证: 无需认证
- 路径参数:
  - `item_id` (integer, required): 项目 ID
- 查询参数:
  - `q` (string, optional): 查询字符串

**响应**:
```json
{
  "item_id": 123,
  "q": "search_term"
}
```

**状态码**:
- `200`: 请求成功

---

## 用户管理 API

### 3. 用户登录

#### POST `/api/v1/user/login`
**描述**: 用户登录认证，获取访问令牌

**请求**:
- 方法: POST
- 认证: 无需认证
- Content-Type: `application/json`

**请求体**:
```json
{
  "email": "admin@example.com",
  "password": "password"
}
```

**字段说明**:
- `email` (string, required): 用户邮箱地址，必须符合邮箱格式
- `password` (string, required): 用户密码

**成功响应** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_info": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "is_active": true
  }
}
```

**错误响应**:

**401 Unauthorized** - 认证失败:
```json
{
  "detail": "用户名或密码错误"
}
```

**422 Validation Error** - 请求数据格式错误:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**状态码**:
- `200`: 登录成功
- `401`: 认证失败
- `422`: 请求数据验证失败

---

### 4. 获取用户信息

#### GET `/api/v1/user/profile`
**描述**: 获取当前认证用户的详细信息

**请求**:
- 方法: GET
- 认证: **需要 JWT Token**
- Headers:
  ```
  Authorization: Bearer <access_token>
  ```

**成功响应** (200):
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "is_active": true
}
```

**错误响应**:

**401 Unauthorized** - Token 无效或过期:
```json
{
  "detail": "Token 已过期"
}
```

**401 Unauthorized** - 缺少认证头:
```json
{
  "detail": "Not authenticated"
}
```

**404 Not Found** - 用户不存在:
```json
{
  "detail": "用户不存在"
}
```

**状态码**:
- `200`: 获取成功
- `401`: 认证失败或 Token 无效
- `404`: 用户不存在

---

### 5. 用户登出

#### POST `/api/v1/user/logout`
**描述**: 用户登出 (客户端 Token 失效提示)

**请求**:
- 方法: POST
- 认证: **需要 JWT Token**
- Headers:
  ```
  Authorization: Bearer <access_token>
  ```

**成功响应** (200):
```json
{
  "message": "登出成功"
}
```

**错误响应**:

**401 Unauthorized** - Token 无效:
```json
{
  "detail": "Token 已过期"
}
```

**状态码**:
- `200`: 登出成功
- `401`: 认证失败

**注意**: 当前实现为客户端登出，服务端不维护 Token 黑名单。客户端需要删除本地存储的 Token。

---

## 数据模型

### LoginRequest
```json
{
  "email": "string (EmailStr)",
  "password": "string"
}
```

### LoginResponse
```json
{
  "access_token": "string",
  "token_type": "string",
  "user_info": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "is_active": "boolean"
  }
}
```

### UserInfo
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "is_active": "boolean"
}
```

## 错误处理

### 通用错误格式
```json
{
  "detail": "错误描述信息"
}
```

### 验证错误格式
```json
{
  "detail": [
    {
      "loc": ["字段位置"],
      "msg": "错误消息",
      "type": "错误类型"
    }
  ]
}
```

### 常见状态码
- `200`: 请求成功
- `201`: 创建成功
- `400`: 请求参数错误
- `401`: 认证失败或未认证
- `403`: 权限不足
- `404`: 资源不存在
- `422`: 请求数据验证失败
- `500`: 服务器内部错误

## 测试用户

### 默认测试账户
- **邮箱**: `admin@example.com`
- **密码**: `password`
- **用户名**: `admin`
- **状态**: 激活

## API 文档访问

### 自动生成文档
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## 使用示例

### 完整认证流程

1. **登录获取 Token**:
```bash
curl -X POST "http://localhost:8000/api/v1/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password"
  }'
```

2. **使用 Token 访问受保护端点**:
```bash
curl -X GET "http://localhost:8000/api/v1/user/profile" \
  -H "Authorization: Bearer <your_access_token>"
```

3. **登出**:
```bash
curl -X POST "http://localhost:8000/api/v1/user/logout" \
  -H "Authorization: Bearer <your_access_token>"
```

## 扩展计划

### 即将添加的端点
1. **用户注册**: `POST /api/v1/user/register`
2. **密码重置**: `POST /api/v1/user/reset-password`
3. **用户列表**: `GET /api/v1/user/list` (管理员)
4. **用户管理**: `PUT/DELETE /api/v1/user/{user_id}` (管理员)
5. **权限管理**: 基于角色的访问控制

### 功能增强
1. **分页支持**: 列表端点添加分页参数
2. **搜索过滤**: 支持复杂查询条件
3. **批量操作**: 支持批量创建/更新/删除
4. **文件上传**: 支持头像和文件上传
5. **实时通知**: WebSocket 支持