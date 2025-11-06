# 网页端架构设计

## 1. 技术选型
- **框架**：Next.js（React + SSR），便于 SEO 与首屏性能。
- **语言**：TypeScript。
- **样式**：Tailwind CSS 或 Ant Design + 自定义主题。
- **状态管理**：React Query（数据同步）+ Zustand（局部状态）。
- **图表**：ECharts 或 Recharts（学习数据可视化）。
- **构建与部署**：Vercel（海外）+ 国内云服务器（备案域名）/自建 Kubernetes。

## 2. 模块划分
1. **公共布局**：导航栏、侧边栏、底部、响应式适配。
2. **仪表盘**：学习概览、任务列表、最近练习。
3. **词汇中心**：词表、复习计划、闪卡、听写。
4. **阅读/听力练习**：支持文本、音频、字幕、答题互动。
5. **写作批改**：富文本编辑器、AI 反馈面板、历史版本。
6. **模考中心**：定时考试、题目切换、答题卡、提交报告。
7. **社区/运营**：资讯列表、直播、活动报名。
8. **账号与设置**：个人信息、目标考试、支付记录、隐私设置。

## 3. 与后端的交互
- 使用统一 API Client（封装 fetch/axios）。
- 通过 SSR 预取数据，CSR 进行交互更新。
- 使用 WebSocket/Server-Sent Events 同步实时通知、学习提醒。
- 支持文件上传（作文附件、音频）至对象存储，后端返回访问 URL。

## 4. 性能优化
- 页面按路由动态拆分；使用 Next.js `dynamic()` 实现懒加载。
- 利用 React Query 缓存与预取数据减少请求延迟。
- 图片优化：Next Image、OSS/CDN 加速。
- 使用 Edge Functions/Serverless 缓存热点页面。

## 5. 安全与合规
- CSRF 防护：SameSite Cookie + CSRF Token。
- XSS 防护：富文本严格过滤、Content Security Policy。
- 权限控制：前端路由守卫 + 后端鉴权。
- 访问日志与操作审计；登录异常监控。

## 6. 无障碍与国际化
- 支持键盘导航、语音阅读（ARIA 标签）。
- 多语言切换：i18next/next-intl；与移动端共享文案资源。
- 响应式布局：适配 1280px 以上桌面与平板设备。

## 7. 自动化与测试
- 组件测试：React Testing Library。
- 端到端测试：Playwright。
- Lint：ESLint + Stylelint + Prettier。
- CI/CD：GitHub Actions → 构建 → 单元测试 → 部署。

## 8. 运营组件
- 埋点：埋点 SDK（神策、GrowingIO），统计用户行为。
- A/B 测试：后端配置实验参数，前端读取。
- SEO：课程/资讯页自定义 meta 标签，生成 sitemap。
