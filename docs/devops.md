# DevOps 与交付流程

## 1. 分支策略
- `main`: 稳定版本，用于生产部署。
- `develop`: 日常开发集成分支。
- 功能分支：`feature/<module-name>`；修复分支：`fix/<issue>`。
- 通过 Pull Request 提交代码，强制代码评审与自动化检查通过后合并。

## 2. 持续集成（CI）
- 使用 GitHub Actions 或 GitLab CI。
- 工作流：
  1. 安装依赖、缓存。
  2. 静态检查（ESLint、ktlint、detekt、Stylelint）。
  3. 单元测试（前端 `pnpm test`, 后端 `npm test`/`yarn test`, 安卓 `./gradlew test`）。
  4. 生成覆盖率报告并上传（Codecov）。
  5. 构建制品（Docker 镜像、APK、Web Bundle）。

## 3. 持续交付（CD）
- **后端**：构建 Docker 镜像，推送至镜像仓库 → 使用 Helm/Kustomize 部署到 Kubernetes。
- **安卓**：生成签名 APK/AAB，上传至各大应用市场；使用 Fastlane 自动化。
- **网页端**：自动部署至服务器/Vercel，国内部署需结合备案域名与 CDN。
- **iOS**：使用 Fastlane 上传 TestFlight，审批后上线 App Store。

## 4. 环境管理
- **本地**：使用 Docker Compose 搭建依赖服务（PostgreSQL、Redis、MinIO）。
- **测试环境**：持续集成后自动部署，供 QA 与灰度测试使用。
- **预发布**：与生产配置一致，进行发布前验证。
- **生产**：多可用区部署，负载均衡（SLB/Nginx Ingress）。

## 5. 可观测性
- **监控**：Prometheus 指标；Grafana 仪表盘展示请求量、延迟、错误率、资源使用。
- **日志**：ELK/EFK 收集服务日志，支持全文搜索。
- **链路追踪**：OpenTelemetry + Jaeger/Zipkin，定位性能瓶颈。
- **报警**：阈值触发短信/企业微信/飞书告警。

## 6. 安全治理
- 依赖安全扫描（Dependabot、Snyk）。
- 容器镜像安全扫描（Trivy）。
- 漏洞管理流程：发现 → 评估 → 修复 → 验证 → 复盘。
- 定期备份数据库与对象存储，演练灾备。

## 7. 质量保障
- 测试金字塔：单元测试 > 集成测试 > UI/E2E。
- 灰度发布与回滚机制：使用流量开关，快速切换旧版本。
- 性能测试：JMeter/Locust，关注高并发情况下的响应时间与资源消耗。
- 可观测性指标纳入 OKR，持续优化。

## 8. 运营与客服支撑
- 建立工单系统（如 Jira Service Management）。
- FAQ 与知识库；应用内反馈自动生成工单。
- 数据看板：日活、转化率、学习效果等核心指标实时展示。
