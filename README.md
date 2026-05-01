# Code Review Bot v2.0

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
| 💬 评论触发 | 在 Issue 中 @code-review-bot 触发重新审核 |

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
│   └── code_review.py          # 核心审核脚本 v2.0
└── requirements.txt             # Python 依赖（可省略，workflow 自动安装）
```

### 触发审核

| 方式 | 触发条件 |
|------|----------|
| Issue 模板 | 选择「代码审核」模板，粘贴代码，提交 |
| PR 自动 | 创建/更新 Pull Request 自动审核 |
| 评论触发 | 在 Issue 中评论 `@code-review-bot` 重新审核 |

### 审核报告示例

```markdown
## 🔍 代码审核报告

**审核时间**: 2026-05-01 18:30:00
**代码来源**: 代码块 #1 (python)
**代码评分**: **78/100** 🟡 良好

### 📊 审核总览

| 检查项 | 结果 |
|--------|------|
| 🔴 严重问题 | 0 |
| 🟠 高危问题 | 1 |
| 🟡 中危问题 | 2 |
| 🟢 低危问题 | 1 |
| 🔑 敏感信息 | 0 |
| 🔒 安全扫描 (Bandit) | 1 |
| 📋 代码风格 (Ruff) | 3 |
| 🐛 Bug (Pylint) | 0 |
| 📏 代码行数 | 128 |
| 🔄 圈复杂度 | 8 |
| 💬 注释比例 | 12% |

<details><summary><b>⚠️ 恶意代码检测（点击展开详情）</b></summary>

#### 🟠 命令注入: subprocess shell=True
- **严重等级**: HIGH
- **出现次数**: 1 次
- **行号**: 18
- **修复建议**: 将 shell=True 改为 shell=False，避免 shell 注入

</details>

<details><summary><b>📝 评分扣分明细（点击展开）</b></summary>

| 扣分项 | 分值 |
|--------|------|
| 命令注入: subprocess shell=True | -15 |
| Bandit: 使用可能被滥用的函数 | -5 |
| Ruff: 3 个问题 | -0.6 |
| 圈复杂度过高 (8) | 0 |

| **最终得分** | **78/100** |

</details>

### 📝 审核结论

⚠️ **审核通过（有警告）** — 代码评分 **78/100**，建议修复后合并。
共发现 3 个高危/中危问题。

---
*此报告由 Code Review Bot v2.0 自动生成 | 审核标准参考 OWASP Top 10 + PEP 8*
```

## ⚙️ 配置

### 自定义审核阈值

编辑 `scripts/code_review.py` 中的常量：

```python
CORE_PASS = 70   # 通过分数阈值（默认 70）
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

**Made with ❤️ by Neko Ai Dev**
