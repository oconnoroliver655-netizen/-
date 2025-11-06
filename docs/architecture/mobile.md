# 移动端架构设计

## 1. 安卓端技术方案
- **语言**：Kotlin（必要时兼容 Java）。
- **架构模式**：MVVM + Clean Architecture。
- **主要框架**：Jetpack Compose（UI）、ViewModel、LiveData/StateFlow、Room、WorkManager、Hilt。
- **网络层**：Retrofit + OkHttp + Kotlin Serialization/ Moshi。
- **本地存储**：Room 数据库（缓存词汇、题库片段）、DataStore（配置）、EncryptedSharedPreferences（敏感数据）。
- **多媒体**：ExoPlayer 播放音视频；语音识别 SDK（科大讯飞/阿里云）。
- **AI 功能对接**：通过后端 API 获取批改结果；口语测评可本地集成语音 SDK。
- **测试**：Unit Test + Instrumentation Test + UI Test（Espresso/Compose Test）。

### 1.1 模块划分
1. `app`: 依赖注入、导航、全局配置。
2. `feature-*`: 按功能拆分模块（词汇、听力、写作、模考、社区等）。
3. `core-ui`: 公用组件、主题、样式。
4. `core-data`: Repository、数据源、网络与数据库实现。
5. `core-model`: 数据模型定义。
6. `core-common`: 工具类、日志、错误处理。

### 1.2 功能规划
- 欢迎/引导页 → 登录 → 选择目标考试。
- 首页展示学习进度、今日任务。
- 词汇学习：卡片切换、发音、复习日历。
- 听力模块：音频播放、字幕同步、语音识别比对。
- 口语模块：录音、评分、反馈建议。
- 写作批改：上传作文 → AI 返回修改建议。
- 模考中心：选择考试 → 计时 → 提交 → 报告。
- 社区运营：资讯、直播入口、积分商城。
- 设置：账号、隐私、设备管理、意见反馈。

### 1.3 上架要求
- 填写《个人信息保护政策》《用户协议》、敏感权限说明。
- 接入国内应用商店 SDK（华为、小米等）实现更新检查与支付适配。
- 通过三方安全检测（如腾讯安全、阿里聚安全）。

## 2. iOS 端预研
- **语言**：Swift。
- **框架**：SwiftUI + Combine（或 UIKit + MVVM-C）。
- **本地存储**：Core Data、UserDefaults、Keychain。
- **网络层**：URLSession + Combine、第三方（Alamofire）。
- **语音能力**：Speech Framework + 后端评分。
- **上架合规**：遵循苹果隐私标签、IAP 支付、TestFlight 测试。

## 3. 跨端设计
- 统一设计语言（色彩、字体、组件），提供 Design System。
- 使用 Figma 建立 UI 组件库；导出给安卓 Compose 与 SwiftUI。
- 多端数据同步：通过后端 API + WebSocket 实时更新（例如学习进度）。
- 用户体验一致性：统一导航结构与术语，同时遵循各平台交互规范。

## 4. 离线能力
- 支持离线下载词汇、音频、练习题；恢复网络后同步结果。
- 离线期间提供本地化批改提示（基础规则），上线后交给云端 AI。
- 断点续传、后台下载、空间管理提示。

## 5. 性能与质量保障
- 启动优化：按需初始化、延迟加载、使用 App Startup。
- 图片资源优化：Glide/Coil（安卓）、SDWebImage（iOS）。
- ANR/Crash 监控：Firebase Crashlytics、腾讯 Bugly。
- 指标采集：帧率、启动时长、网络耗时，上报到埋点系统。
- 自动化流水线：Gradle + GitHub Actions/Jenkins 编译、单元测试、静态检查（ktlint、detekt）。

## 6. 国际化与无障碍
- 采用资源文件管理多语言，初期支持简体中文 + 英文。
- 支持字体大小调节、深色模式、语音朗读。
- 在 iOS 使用 Dynamic Type，在安卓使用 Compose 提供可访问性描述。
