from __future__ import annotations

"""一键启动脚本，帮助零基础同学快速跑起后端服务。

使用示例：
    python quickstart.py demo   # 安装依赖、写入演示数据并启动服务
    python quickstart.py run    # 已安装依赖后仅启动服务
    python quickstart.py setup  # 只安装依赖，不启动服务
    python quickstart.py seed   # 单独写入演示数据
"""

import argparse
import os
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import List
import venv

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
VENV_DIR = BACKEND_DIR / ".venv"
PYTHON_DIR = "Scripts" if os.name == "nt" else "bin"


def _venv_python() -> Path:
    return VENV_DIR / PYTHON_DIR / "python"


def _venv_pip() -> Path:
    return VENV_DIR / PYTHON_DIR / "pip"


def ensure_python_version() -> None:
    if sys.version_info < (3, 10):
        raise SystemExit("请使用 Python 3.10 及以上版本运行该脚本。")


def ensure_virtualenv() -> None:
    if VENV_DIR.exists():
        return
    print("[1/3] 创建虚拟环境…")
    venv.EnvBuilder(with_pip=True).create(VENV_DIR)


def install_dependencies(index_url: str | None = None, extra_index_url: str | None = None) -> None:
    ensure_virtualenv()
    pip_executable = _venv_pip()
    print("[2/3] 安装后端依赖…（首次运行可能需要几分钟）")
    cmd: List[str] = [
        str(pip_executable),
        "install",
        "-r",
        str(BACKEND_DIR / "requirements.txt"),
    ]
    if index_url:
        cmd.extend(["--index-url", index_url])
    if extra_index_url:
        cmd.extend(["--extra-index-url", extra_index_url])
    subprocess.check_call(cmd)


def run_seed() -> None:
    ensure_virtualenv()
    python_executable = _venv_python()
    print("[3/3] 写入演示数据（考试、课程、演示账号）…")
    subprocess.check_call([str(python_executable), "-m", "app.seed"], cwd=str(BACKEND_DIR))


def run_server(port: int) -> None:
    ensure_virtualenv()
    python_executable = _venv_python()
    cmd: List[str] = [
        str(python_executable),
        "-m",
        "uvicorn",
        "app.main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        str(port),
    ]
    print(
        textwrap.dedent(
            f"""
            ✅ 服务已启动，打开浏览器访问 http://127.0.0.1:{port}/docs 即可测试接口。
            若要停止服务，请在当前窗口按下 Ctrl+C。
            """
        ).strip()
    )
    subprocess.call(cmd, cwd=str(BACKEND_DIR))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="快速搭建并体验英语学习平台后端")
    parser.add_argument(
        "command",
        choices=["demo", "run", "setup", "seed"],
        default="demo",
        nargs="?",
        help="demo=安装依赖+写入演示数据+启动服务",
    )
    parser.add_argument("--port", type=int, default=8000, help="启动服务的端口，默认 8000")
    parser.add_argument(
        "--pip-index-url",
        dest="pip_index_url",
        help="自定义 PyPI 源地址，例如 https://pypi.tuna.tsinghua.edu.cn/simple",
    )
    parser.add_argument(
        "--pip-extra-index-url",
        dest="pip_extra_index_url",
        help="附加 PyPI 源地址，与官方源共同使用",
    )
    return parser.parse_args()


def main() -> None:
    ensure_python_version()
    args = parse_args()
    pip_kwargs = {
        "index_url": args.pip_index_url,
        "extra_index_url": args.pip_extra_index_url,
    }

    if args.command == "setup":
        install_dependencies(**pip_kwargs)
        print("全部准备就绪，可以运行 python quickstart.py run 来启动服务。")
        return

    if args.command == "seed":
        install_dependencies(**pip_kwargs)
        run_seed()
        return

    if args.command == "run":
        install_dependencies(**pip_kwargs)
        run_server(args.port)
        return

    # demo 模式：安装依赖 -> 写入演示数据 -> 启动服务
    install_dependencies(**pip_kwargs)
    run_seed()
    run_server(args.port)


if __name__ == "__main__":
    main()
