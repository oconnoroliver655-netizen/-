# 英语备考学习平台

面向中国国内英语学习者的多端学习系统，提供考试定制化学习路径、AI 辅助批改、模考与运营增长工具。本仓库提供第一版可运行的 FastAPI 后端服务，并配套完整的产品规划与架构设计资料。

## 仓库结构
- `backend/`：FastAPI 服务代码、数据模型、API 以及自动化测试。
- `docs/requirements.md`：产品需求文档（PRD）。
- `docs/architecture/backend.md`：后端架构设计方案。
- `docs/architecture/mobile.md`：移动端（安卓/iOS）技术规划。
- `docs/architecture/web.md`：网页端架构设计。
- `docs/ai_capabilities.md`：AI 能力规划与路线图。
- `docs/devops.md`：DevOps、CI/CD 与运维策略。
- `docs/roadmap.md`：阶段性开发路线图。

## 新手一键启动

对编程经验不多的同学，可直接运行仓库根目录的脚本：

```bash
python quickstart.py demo
```

脚本会自动完成以下步骤：

1. 创建虚拟环境并安装后端依赖。
2. 初始化数据库、写入示例考试/课程/课时数据，并创建可直接登录的演示账号（邮箱 `demo@student.local`，密码 `English123!`）。
3. 启动 FastAPI 服务（默认地址 http://127.0.0.1:8000/docs，可在浏览器中直接测试接口）。

如果只想安装依赖或启动服务，可执行：

```bash
python quickstart.py setup  # 仅安装依赖
python quickstart.py run    # 启动服务
python quickstart.py seed   # 手动写入演示数据
```

更详细的零基础上手说明可参考《[零基础快速体验指南](docs/beginner_quickstart.md)》。

## 后端服务快速开始（手动方式）

1. 安装依赖

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows 使用 .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

2. 启动开发服务器

   ```bash
   uvicorn app.main:app --reload
   ```

   默认会在项目根目录生成 `english_app.db` SQLite 数据库。可运行 `python -m app.seed` 写入示例考试、课程与演示账号。

3. 运行自动化测试

   ```bash
   pytest
   ```

4. 了解整体研发步骤

   阅读《[制作英语备考学习平台的实操指南](docs/how_to_build.md)》，文档提供了从团队搭建、项目初始化到多端研发与上线运营的详细步骤。

## 后续计划
- 扩展后端模块（练习记录、AI 批改、实时课堂等）。
- 搭建安卓 MVP Demo，验证学习流程与 AI 批改体验。
- 启动网页端原型设计与组件库搭建。
- 根据用户反馈迭代需求，持续完善文档与代码。

## 许可
本项目遵循 [MIT License](LICENSE)。
