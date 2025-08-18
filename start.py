#!/usr/bin/env python3
"""
启动脚本

提供多种启动方式的便捷脚本
"""

import argparse
import os
import sys
from pathlib import Path


def install_dependencies():
    """安装项目依赖"""
    print("📦 安装项目依赖...")
    os.system("pip install -r requirements.txt")
    print("✅ 依赖安装完成")


def start_dev_server(host="0.0.0.0", port=8000, reload=True):
    """启动开发服务器"""
    print(f"🚀 启动开发服务器 http://{host}:{port}")
    reload_flag = "--reload" if reload else "--no-reload"
    os.system(f"uvicorn main:app --host {host} --port {port} {reload_flag}")


def start_production_server(host="0.0.0.0", port=8000, workers=4):
    """启动生产服务器"""
    print(f"🏭 启动生产服务器 http://{host}:{port} (workers: {workers})")
    os.system(
        f"gunicorn main:app -w {workers} -k uvicorn.workers.UvicornWorker --bind {host}:{port}"
    )


def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    os.system("pytest -v")


def format_code():
    """格式化代码"""
    print("🎨 格式化代码...")
    os.system("black .")
    os.system("isort .")
    print("✅ 代码格式化完成")


def lint_code():
    """检查代码质量"""
    print("🔍 检查代码质量...")
    print("\n--- flake8 检查 ---")
    os.system("flake8 .")
    print("\n--- mypy 类型检查 ---")
    os.system("mypy .")
    print("✅ 代码检查完成")


def setup_env():
    """设置环境"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_example.exists() and not env_file.exists():
        print("📝 创建环境配置文件...")
        env_file.write_text(env_example.read_text())
        print("✅ 已创建 .env 文件，请根据需要修改配置")
    else:
        print("ℹ️  环境配置文件已存在")


def main():
    parser = argparse.ArgumentParser(description="FastAPI 项目启动脚本")
    parser.add_argument(
        "command",
        choices=[
            "dev", "prod", "install", "test", 
            "format", "lint", "setup", "all"
        ],
        help="要执行的命令"
    )
    parser.add_argument("--host", default="0.0.0.0", help="服务器主机地址")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口")
    parser.add_argument("--workers", type=int, default=4, help="生产环境工作进程数")
    parser.add_argument("--no-reload", action="store_true", help="禁用自动重载")
    
    args = parser.parse_args()
    
    if args.command == "dev":
        start_dev_server(args.host, args.port, not args.no_reload)
    elif args.command == "prod":
        start_production_server(args.host, args.port, args.workers)
    elif args.command == "install":
        install_dependencies()
    elif args.command == "test":
        run_tests()
    elif args.command == "format":
        format_code()
    elif args.command == "lint":
        lint_code()
    elif args.command == "setup":
        setup_env()
    elif args.command == "all":
        print("🔧 执行完整设置流程...")
        setup_env()
        install_dependencies()
        format_code()
        lint_code()
        print("\n🎉 设置完成！现在可以运行 'python start.py dev' 启动开发服务器")


if __name__ == "__main__":
    main()