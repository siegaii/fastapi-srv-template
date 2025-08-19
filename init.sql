-- 数据库初始化脚本
-- 在PostgreSQL容器启动时自动执行

-- 创建UUID扩展（用于生成UUID主键）
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建时间戳函数（用于自动更新updated_at字段）
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 设置时区
SET timezone = 'Asia/Shanghai';

-- 输出初始化完成信息
SELECT 'Database initialization completed' as status;