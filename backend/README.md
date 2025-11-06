# FastAPI Backend

该目录提供英语备考学习平台的首个可运行后端服务，实现用户注册、鉴权、考试/课程/课时管理、学习计划以及仪表盘统计等核心接口。

## 功能特性
- 用户注册、登录（JWT 鉴权）。
- 考试、课程、课时的 CRUD 接口。
- 学习计划创建、更新、查询。
- 仪表盘概览（课程、课时、学习计划统计与最近课时）。
- 一键初始化示例数据的 `/seed/basic` 接口。

## 技术栈
- [FastAPI](https://fastapi.tiangolo.com/)：构建 RESTful API。
- [SQLAlchemy 2.0](https://www.sqlalchemy.org/)：关系型数据建模。
- [SQLite](https://www.sqlite.org/)：默认轻量级数据库，可替换为 MySQL/PostgreSQL。
- [PyJWT](https://pyjwt.readthedocs.io/) + [Passlib](https://passlib.readthedocs.io/)：身份认证与密码加密。

## 本地开发
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows 使用 .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

默认使用 `english_app.db` SQLite 文件。生产环境可通过设置 `ENGLISH_APP_DB_PATH` 环境变量更换数据库路径；若切换到 MySQL/PostgreSQL，请在 `app/database.py` 中调整连接字符串。

如需直接写入示例考试/课程/课时和演示账号，可执行：

```bash
python -m app.seed
```

命令会输出数据库位置以及演示账号（邮箱 `demo@student.local`、密码 `English123!`）。

## 运行测试
```bash
pytest
```

测试使用独立的内存数据库，不会污染本地开发数据。

## 下一步建议
- 引入基于角色的权限控制（管理员、教师、学员）。
- 接入对象存储用于音视频、练习素材的管理。
- 与 AI 模块对接，实现口语/写作自动批改接口。
- 结合 Celery/Redis 实现学习提醒、计划调度等异步任务。
