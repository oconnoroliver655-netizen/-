# 制作英语备考学习平台的实操指南

本文面向技术团队，提供从 0 到 1 搭建本仓库所规划英语备考学习平台的详细步骤。内容覆盖基础设施准备、后端与数据库、AI 能力接入、安卓 App、网页端以及发布运营流程。可根据团队规模拆分任务并并行推进。

## 1. 团队与工具准备

1. **组建核心团队**：
   - 产品经理（1）：负责需求拆分与版本节奏。
   - 技术负责人（1）：总体架构与技术决策。
   - 后端工程师（2-3）：API、数据库、AI 服务对接。
   - 安卓工程师（2）：移动端实现与适配。
   - Web 前端工程师（2）：网页端实现与组件库搭建。
   - 测试/QA（1）：测试用例、自动化测试。
   - 教研与内容团队（1-2）：题库、课程内容、AI 训练语料。

2. **账号与服务**：
   - 代码托管：GitHub/GitLab/国内平台，创建组织与私有仓库。
   - 项目管理：Jira、Tapd、飞书多维表格，用于需求与迭代跟踪。
   - 云资源：阿里云/腾讯云，准备 ECS、RDS、OSS、短信与语音合成服务。
   - 合规：ICP备案主体、公安网备、隐私合规咨询。

3. **开发环境要求**：
   - Node.js ≥ 18、pnpm 或 npm、Java ≥ 17（若采用 Spring Boot）。
   - PostgreSQL 15、Redis 7、Elasticsearch（可选，用于搜索）。
   - Android Studio 最新版、JDK 17、Android SDK 34。
   - 前端：pnpm、Next.js、TypeScript、Tailwind CSS。
   - AI：接入合规大模型（如文心、讯飞星火、百川），并准备模型密钥管理方案。

## 2. 仓库初始化与基础设施

1. **仓库结构建议**：
   ```text
   /
   ├─ backend/           # 后端服务（NestJS 或 Spring Boot）
   ├─ web/               # 网页端（Next.js）
   ├─ android/           # 安卓原生项目
   ├─ docs/              # 规划与设计文档
   ├─ scripts/           # 基础运维脚本
   └─ infra/             # IaC（Terraform/Helm）
   ```
2. **初始化后端与前端项目**：
   - 后端（NestJS 示例）：
     ```bash
     pnpm dlx @nestjs/cli new backend
     cd backend && pnpm install && pnpm run start:dev
     ```
   - Web（Next.js 示例）：
     ```bash
     pnpm dlx create-next-app@latest web --typescript --app --eslint --tailwind
     ```
   - 安卓：使用 Android Studio 创建空 Compose 项目，包名如 `com.company.examcoach`。
3. **统一代码规范**：
   - 配置 ESLint、Prettier（前端/Node.js）、ktlint（安卓）、Checkstyle/Spotless（Java）。
   - 在仓库根目录添加 `.editorconfig` 与 `commitlint` 规则。
4. **CI/CD 雏形**：
   - 使用 GitHub Actions/云效流水线，配置以下工作流：
     - 后端单元测试 + Lint。
     - Web 构建与 Lint。
     - 安卓 Gradle Lint + 单元测试。
   - 引入 SonarQube 或 CodeQL 做静态扫描。

## 3. 后端服务开发

### 3.1 数据建模与数据库初始化
1. 设计核心实体：用户、学习计划、课程、题目、试卷、作答记录、错题本、支付订单、AI 批改结果。
2. PostgreSQL 示例建表脚本（节选）：
   ```sql
   CREATE TABLE users (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     phone VARCHAR(20) UNIQUE NOT NULL,
     password_hash TEXT,
     nickname VARCHAR(50),
     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
   );

   CREATE TABLE study_plans (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     user_id UUID REFERENCES users(id),
     exam_type VARCHAR(32) NOT NULL,
     start_date DATE NOT NULL,
     target_date DATE NOT NULL,
     progress JSONB DEFAULT '{}'::jsonb
   );
   ```
3. 使用 Prisma/TypeORM/Spring Data JPA 管理迁移：
   ```bash
   pnpm prisma migrate dev --name init
   ```

### 3.2 领域模块划分
- `auth`：手机号验证码登录、密码登录、第三方登录。
- `users`：个人信息、学习档案。
- `content`：题库、课程、词汇表管理。
- `practice`：练习任务、模考、错题本。
- `ai-feedback`：写作/口语批改、评分结果存储。
- `payment`：会员权益、购买课程、订单与发票。

### 3.3 API 设计与实现
1. 使用 OpenAPI/Swagger 先行定义接口：
   ```bash
   pnpm nest g resource exams --type=rest --crud
   ```
2. 核心接口示例：
   - `POST /auth/login`：手机号验证码登录。
   - `POST /plans`：创建学习计划。
   - `GET /plans/:id/progress`：查看进度。
   - `POST /practice/sessions`：开始模考或练习。
   - `POST /ai/essay-evaluations`：提交作文获得评分。
3. 编写服务层逻辑：整合题库、AI 服务，并维护 Redis 缓存（热门课程、排行榜）。
4. 接入支付：
   - 虚拟内容需遵循微信/支付宝平台规则。
   - 使用服务端签名，回调处理订单状态。
5. 安全与合规：
   - JWT 或 session 管理。
   - API 速率限制（NestJS Throttler/自建中间件）。
   - 敏感数据加密存储（手机号脱敏、密码 bcrypt）。

### 3.4 测试与监控
1. 单元测试：Jest（NestJS）或 JUnit（Spring）。关键模块覆盖率 ≥ 70%。
2. 集成测试：使用 Supertest 或 Postman/Newman 覆盖登录、学习计划、AI 批改流程。
3. 监控：Prometheus + Grafana、APM（SkyWalking/Jaeger）追踪调用链。
4. 日志：采集到 ELK/阿里云 SLS，配置隐私脱敏。

## 4. AI 能力接入步骤

1. **确定场景**：作文批改、口语评分、听力听写纠错、智能规划学习路径。
2. **模型选择**：在国内合规范围内，选用具备开放 API 的大模型或自建轻量模型。
3. **服务封装**：
   - 后端创建 `ai` 模块，定义统一接口 `AiProvider`。
   - 实现 `BaiduWenxinProvider`、`iFlytekSparkProvider` 等适配器。
   - 使用策略模式按场景路由：作文 -> 大模型，口语 -> 语音评分服务。
4. **提示词/模板管理**：存入数据库或配置中心，支持动态迭代与 A/B 实验。
5. **缓存与队列**：
   - 对高耗时批改任务使用消息队列（RabbitMQ/Kafka）异步处理。
   - 设置任务超时与重试机制。
6. **成本控制**：记录调用日志与费用，定期优化 prompt、权重策略。
7. **数据闭环**：教研团队人工抽检、标注，持续微调自有模型。

## 5. 安卓 App 开发流程

1. **项目初始化**：
   - Android Studio -> New Project -> Empty Compose Activity。
   - 配置模块结构：`app`（展示层）、`core`（网络、数据库、DI）、`feature-*`（按业务划分）。
2. **基础依赖**：
   - Retrofit + OkHttp + Kotlin Serialization（网络层）。
   - Hilt（依赖注入）、Room（离线缓存）、DataStore（偏好设置）。
   - Jetpack Compose + Navigation。
3. **核心页面**：
   - 登录注册页：手机号 + 验证码登录流程、隐私协议确认。
   - 首页 Dashboard：学习计划概览、AI 学习建议卡片。
   - 词汇/题库练习：支持离线、收藏、错题本。
   - 模考流程：倒计时、进度条、交卷后展示 AI 解析。
   - 写作/口语批改：支持录音上传、实时评语展示。
4. **状态管理**：
   - 使用 `ViewModel` + `StateFlow`。
   - 对网络层提供 `Repository`，结合 UseCase 拆分业务逻辑。
5. **测试与质量**：
   - 单元测试：JUnit + MockK；UI 测试：Compose UI Test。
   - 接入 Firebase Crashlytics（国内需走第三方，如 Bugly）。
6. **国内发布要求**：
   - 准备隐私政策弹窗、SDK 列表、第三方服务说明。
   - 打包渠道 APK，适配华为、小米等渠道的升级策略。

## 6. 网页端开发流程

1. **设计系统与组件库**：
   - 建立 `design-tokens.json`，约定品牌色、字体、间距。
   - 使用 Storybook 做组件开发与文档。
2. **页面路由规划**：
   - `/`：首页，介绍产品与考试资源。
   - `/dashboard`：学习概览，需要登录。
   - `/practice/*`：词汇、听力、阅读模块。
   - `/ai/essay`：作文批改页面。
   - `/admin`：后台管理（题库、课程、用户管理）。
3. **数据请求**：
   - 使用 `react-query` 或 `swr` 管理缓存。
   - 与后端统一鉴权（JWT + HttpOnly Cookie）。
4. **SSR 与 SEO**：
   - 使用 Next.js App Router，针对公开页面开启 SSR，便于搜索收录。
5. **国际化与可访问性**：
   - i18n（中文、英文），ARIA 标签，键盘导航支持。
6. **测试**：
   - 单元测试：Vitest/Testing Library。
   - 端到端测试：Playwright，覆盖登录、模考流程。

## 7. DevOps 与部署

1. **环境划分**：开发（dev）、测试（staging）、生产（prod）。
2. **容器化**：
   - 为后端与前端服务编写 Dockerfile，使用多阶段构建。
   - Docker Compose 或 Kubernetes 管理部署。
3. **数据库与缓存**：使用云数据库或自建，配置主从复制与自动备份。
4. **CI/CD 流程**：
   - 合并请求触发测试，全部通过后允许合并。
   - 主干分支打 Tag 触发部署（使用 Argo CD 或 Jenkins Pipeline）。
5. **监控与告警**：
   - API 性能：Prometheus + Grafana。
   - 前端监控：Sentry（需符合数据出境合规）。
   - 日志：ELK/阿里云日志服务，配置手机号等敏感信息脱敏。

## 8. 上线前准备

1. **安全与合规审查**：
   - 渗透测试、隐私合规评估、第三方 SDK 自查表。
   - 完成 ICP、教育类备案（如涉及在线教育需向教育部门报备）。
2. **内容审核**：题库与课程内容由教研团队审校，确保版权与准确性。
3. **灰度发布**：
   - 安卓：先通过内测分发平台（如蒲公英）邀请用户测试。
   - Web：使用 Feature Flag 控制新增功能，逐步放量。
4. **用户反馈渠道**：
   - App 内嵌意见反馈、客服系统（美洽、Udesk）。
   - 建立知识库/FAQ，整理常见问题。

## 9. 运营与持续迭代

1. **数据指标**：DAU、留存率、学习计划完成率、AI 批改使用次数、转化率。
2. **版本节奏**：每两周一个小版本，重要考试节点推出专项内容。
3. **A/B 测试**：对 AI 批改提示语、学习路径推荐进行实验。
4. **增长玩法**：排行榜、闯关赛、积分兑换商城，与高校/机构合作推广。
5. **用户成功团队**：安排督学老师或班主任，跟进高价值用户。

## 10. 后续扩展

- **iOS App**：在安卓与 Web 稳定后，复用业务逻辑与 API，使用 SwiftUI 实现。
- **B 端服务**：为学校/机构提供管理后台、班级数据报告。
- **多语言扩展**：后续支持出海市场或其他语种考试。

> 结合本文步骤与仓库内的规划文档，可按照模块化方式推进研发。建议在正式开发前完成详细的任务拆分与人力排期，保障需求、设计、开发、测试之间的协同。
