# 零基础快速体验指南

如果你刚开始学习编程，只需按照下面的步骤，就可以在自己的电脑上体验英语备考学习平台的后端接口：

1. **安装 Python 3.10 以上版本**
   - Windows/macOS 可在 [Python 官网](https://www.python.org/downloads/) 下载图形化安装包。
   - 安装时记得勾选 “Add Python to PATH”。

2. **克隆或下载本仓库**
   - 安装好 Git 后可以运行：
     ```bash
     git clone <你的仓库存放地址>
     ```
   - 或者直接在 GitHub 上点击 “Code -> Download ZIP”，解压到任意文件夹。

3. **一键启动后端服务**
   - 打开命令行（Windows 使用 PowerShell，macOS 使用 Terminal）。
   - 进入项目根目录后执行：
     ```bash
     python quickstart.py demo
     ```
   - 脚本会自动完成依赖安装、数据库初始化并启动服务。命令行会显示如下关键信息：
     - API 地址：`http://127.0.0.1:8000/docs`
     - 演示账号：邮箱 `demo@student.local`，密码 `English123!`

4. **在浏览器体验接口**
   - 打开上述 API 地址即可看到自动生成的 Swagger 界面。
   - 点击 “Authorize” 按钮，输入演示账号完成登录后，即可尝试创建学习计划、查询课程等接口。

5. **遇到问题怎么办？**
   - 如果命令行提示找不到 `python`，请确认第 1 步安装成功，并重新打开命令行。
   - 如果依赖安装失败（常见于网络受限环境），可尝试切换到国内镜像，例如执行：
     ```bash
     python quickstart.py setup --pip-extra-index-url https://pypi.tuna.tsinghua.edu.cn/simple
     ```
     若希望完全替换官方源，可使用 `--pip-index-url` 参数。
     或者按照 [backend/README.md](../backend/README.md) 中的手动步骤逐条执行，查看具体报错并截图反馈。

完成以上步骤后，你就拥有了一个可用的后端接口，可以继续根据《[制作英语备考学习平台的实操指南](how_to_build.md)》逐步拓展前端、AI 和运营功能。
