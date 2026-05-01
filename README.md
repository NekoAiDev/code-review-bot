# Code Review Bot v2.1

一个基于 GitHub Actions 的自动化代码审核机器人，能够检测安全问题、合规问题、敏感信息泄露和潜在 Bug，并给出 0-100 分的综合评分。

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 🔍 多源审核 | 支持 Issue 代码块 + PR diff 变更文件 |
| 🔒 恶意代码检测 | 检测命令注入、代码执行、反序列化、路径遍历等，含 CRITICAL/HIGH/MEDIUM/LOW 严重等级 |
| 🔑 敏感信息检测 | 检测硬编码密码、API Key、GitHub Token、AWS Key、私钥等 |
| 🔒 Bandit 安全扫描 | 专业 Python 安全漏洞扫描 |
| 📋 Ruff 代码风格 | PEP 8 合规性检查 |
| 🐛 Pylint Bug 检测 | 潜在 Bug 和逻辑错误检测 |
| 📊 代码复杂度分析 | 圈复杂度、代码行数、注释比例 |
| 📝 0-100 评分系统 | 自动评分 + 等级徽章（优秀/良好/需改进/不合格）|
| 🏷 自动标签 | 根据评分自动打标签（score-excellent/good/needs-work/poor）|
| 📂 可折叠报告 | 详细问题可折叠，报告清晰易读 |
| 💬 评论指令 | 支持多条指令：重新审核、请求人工、审核通过/拒绝 |
| 📧 管理员邮件通知 | 每次代码提交和审核完成后自动邮件通知管理员 |

## 📊 评分标准

| 分数 | 等级 | 徽章 | 说明 |
|------|------|------|------|
| 90-100 | 优秀 | 🟢 | 代码质量优秀，几乎无问题 |
| 70-89 | 良好 | 🟡 | 代码质量良好，少量警告 |
| 50-69 | 需改进 | 🟠 | 存在中高危问题，建议修复后合并 |
| 0-49 | 不合格 | 🔴 | 存在严重问题，必须修复 |

**扣分规则：**
- CRITICAL 问题：-25 分/个
- HIGH 问题：-15 分/个
- MEDIUM 问题：-8 分/个
- LOW 问题：-3 分/个
- 敏感信息泄露：-15 分/个
- Bandit 问题：-3~-15 分/个（按严重等级）
- Ruff 问题：-0.2 分/个（上限 -10 分）
- Pylint Error：-3 分/个
- 圈复杂度 >20：-5 分
- 代码行数 >500：-3 分
- 注释比例 <5%：-3 分

## 🚀 使用方法

### 安装到仓库

将 `code-review-bot` 的文件复制到你的仓库：

```
your-repo/
├── .github/
│   └── workflows/
│       └── code-review.yml       # 审核工作流
├── scripts/
│   └── code_review.py          # 核心审核脚本 v2.1
└── requirements.txt             # Python 依赖（可省略，workflow 自动安装）
```

### 配置 Secrets

在仓库 Settings → Secrets and variables → Actions 中添加：

| Secret 名称 | 说明 | 必需 |
|-------------|------|------|
| `MAIL_PASSWORD` | QQ 邮箱 SMTP 授权码（非 QQ 密码） | ✅ |

### 触发审核

| 方式 | 触发条件 |
|------|----------|
| Issue 模板 | 选择「提交代码」模板，粘贴代码，提交 |
| PR 自动 | 创建/更新 Pull Request 自动审核 |
| 评论触发 | 在 Issue 中评论 `@code-review-bot review` 重新审核 |

## 💬 指令系统

### 普通用户指令

| 指令 | 说明 |
|------|------|
| `@code-review-bot review` | 重新触发自动审核 |
| `@code-review-bot human` | 请求管理员人工审核 |

### 管理员指令

| 指令 | 说明 |
|------|------|
| `@code-review-bot approve` | 标记审核通过，自动回复并打 `approved` 标签 |
| `@code-review-bot reject [原因]` | 标记审核不通过，自动回复原因并打 `rejected` 标签 |

### 人工审核流程

```
用户提交代码 → 自动审核 → 评论审核报告
                        ↓
            用户评论 @code-review-bot human → 邮件通知管理员
                        ↓
            管理员在 Issue 查看代码和报告
                        ↓
            管理员评论 @code-review-bot approve → ✅ 审核通过
            或
            管理员评论 @code-review-bot reject 代码有XX问题 → ❌ 审核不通过
```

## 📧 管理员邮件通知

管理员邮箱：**3815099625@qq.com**

邮件通知场景：
1. **新代码提交** — 用户创建代码审核 Issue 时，立即通知管理员
2. **审核报告** — 自动审核完成后，发送完整审核报告（附件 md + 邮件摘要）
3. **人工审核请求** — 用户请求人工审核时，邮件通知管理员前往处理

邮件标题统一以 `[Admin管理员]` 开头，方便识别。

## 🏷 自动标签

| 标签 | 触发条件 |
|------|----------|
| `review` | 提交代码 Issue |
| `bug` / `triage` | Bug 反馈 Issue |
| `enhancement` | 功能建议 Issue |
| `review-passed` | 自动审核通过 |
| `review-warning` | 自动审核通过但有警告 |
| `review-failed` | 自动审核未通过 |
| `human-review` | 用户请求人工审核 |
| `approved` | 管理员审核通过 |
| `rejected` | 管理员审核不通过 |
| `score-excellent` | 评分 ≥ 90 |
| `score-good` | 评分 ≥ 70 |
| `score-needs-work` | 评分 ≥ 50 |
| `score-poor` | 评分 < 50 |

## ⚙️ 配置

### 自定义审核阈值

编辑 `scripts/code_review.py` 中的常量：

```python
SCORE_PASS = 70   # 通过分数阈值（默认 70）
SCORE_WARN = 50   # 警告分数阈值（默认 50）
```

### 自定义恶意代码规则

在 `scripts/code_review.py` 中的 `MALICIOUS_PATTERNS` 列表添加新规则：

```python
(r"你的正则模式", "描述", "HIGH", "修复建议"),
```

### 自定义敏感信息规则

在 `SECRET_PATTERNS` 列表添加新规则：

```python
(r"你的正则模式", "描述"),
```

### 自定义管理员邮箱

编辑 `.github/workflows/code-review.yml` 中的 `env`：

```yaml
env:
  ADMIN_EMAIL: "your-admin@qq.com"
```

## 🛠 支持的编程语言

| 语言 | 安全检测 | 风格检查 | Bug 检测 |
|------|----------|----------|----------|
| Python | ✅ Bandit + 模式匹配 | ✅ Ruff | ✅ Pylint |
| JavaScript | ✅ 模式匹配 | ⏳ 计划中 | ⏳ 计划中 |
| Java | ✅ 模式匹配 | ⏳ 计划中 | ⏳ 计划中 |
| Go | ✅ 模式匹配 | ⏳ 计划中 | ⏳ 计划中 |

## 📝 开发

### 本地测试

```bash
pip install ruff pylint bandit

# 设置事件文件路径（模拟 GitHub Actions）
export GITHUB_EVENT_PATH=/path/to/event.json
export EVENT_NAME=issues   # 或 pull_request
export GITHUB_TOKEN=xxx  # 可选

python scripts/code_review.py
```

### 贡献

欢迎提交 Issue 和 PR！请使用对应的 Issue 模板。

## 📄 许可证

MIT License

## 🙏 致谢

本项目的设计灵感来自于 [AstrBot](https://github.com/Soulter/AstrBot) 插件审核机器人。

---

**Made with ❤️ by Neko Ai**
