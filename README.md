# Code Review Bot

一个基于 GitHub Actions 的自动化代码审核机器人，能够检测代码中的安全问题、合规问题和潜在 Bug。

## ✨ 功能特性

- **📝 Issue 模板** — 用户创建 Issue 时自动弹出选项引导（提交代码审核 / Bug 反馈 / 功能建议）
- **🔒 安全检测** — 使用 Bandit 扫描 Python 代码中的安全漏洞
- **📋 合规检查** — 使用 Ruff 检查代码风格和规范性
- **🐛 Bug 检测** — 使用 Pylint 检测潜在 Bug 和逻辑错误
- **⚠️ 恶意代码识别** — 自动识别危险函数调用（eval、exec、os.system 等）
- **🏷 自动标签** — 根据模板类型自动打标签（review / bug / enhancement）
- **📊 审核结果标签** — 审核通过自动打 `review-passed`，未通过打 `review-failed`
- **📝 自动报告** — 自动生成审核报告并评论到 Issue/PR

## 🚀 使用方法

### 1. 安装到仓库

将本项目文件复制到你的仓库中：

```
your-repo/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── code-review.yml       # 代码审核模板
│   │   ├── bug-report.yml        # Bug 反馈模板
│   │   ├── feature-request.yml   # 功能建议模板
│   │   └── config.yml            # 模板配置
│   └── workflows/
│       └── code-review.yml       # 审核工作流
├── scripts/
│   └── code_review.py            # 核心审核脚本
└── requirements.txt              # Python 依赖
```

### 2. 用户使用流程

用户点击 **New Issue** 时会看到三个选项：

| 模板 | 用途 | 自动标签 |
|------|------|----------|
| 📝 代码审核 | 提交代码进行自动审核 | `review` |
| 🐛 Bug 反馈 | 报告审核机器人本身的问题 | `bug` |
| 💡 功能建议 | 为审核机器人提出新功能 | `enhancement` |

用户选择 **📝 代码审核** 后：

1. 填写编程语言
2. 粘贴代码
3. 确认不包含敏感信息
4. 提交 Issue
5. 审核机器人自动运行，几分钟内评论审核报告

### 3. 查看审核报告

机器人会自动在 Issue/PR 下评论审核报告，包含：

- ✅ 通过项
- ⚠️ 警告项
- ❌ 未通过项
- 📝 修复建议

同时自动添加审核结果标签：
- `review-passed` — 审核通过
- `review-failed` — 审核未通过

## 📊 审核报告示例

```markdown
## 🔍 代码审核报告

**审核时间**: 2026-05-01 18:05:00
**审核机器人**: Code Review Bot v1.0.0

### 🔒 安全检查
**⚠️ 发现潜在危险操作:**
- ❌ 危险函数: os.system

**Bandit 安全扫描:**
- ⚠️ 使用可能被滥用的函数 (行 18)

### 📋 合规检查
**Ruff 代码风格检查:**
- ⚠️ 3 个警告

### 🐛 Bug 检测
**⚠️ 2 个警告:**
- 未使用的变量 (行 5)
- 未处理的异常 (行 42)

### 📝 审核总结
⚠️ **审核通过（有警告）** - 发现少量问题，建议修复后合并。

---
*此报告由 Code Review Bot 自动生成*
```

## ⚙️ 配置

### 自定义 Issue 模板

编辑 `.github/ISSUE_TEMPLATE/` 下的模板文件，修改表单字段：

```yaml
# .github/ISSUE_TEMPLATE/code-review.yml
- type: dropdown
  id: language
  attributes:
    label: 编程语言
    options:
      - Python
      - JavaScript
      - TypeScript
      # 添加更多语言...
```

### 自定义审核规则

在 `scripts/code_review.py` 中，可以调整检查工具的参数：

```python
# 调整 Bandit 检查级别
result = subprocess.run(
    ["bandit", "-f", "json", "-ll", "-r", code_path],  # -ll 只显示中高级别问题
    ...
)
```

## 🛠 支持的编程语言

- **Python** (主要支持)
  - 安全检测: Bandit
  - 代码风格: Ruff
  - Bug 检测: Pylint

未来计划支持：
- JavaScript/TypeScript
- Java
- Go

## 📝 开发

### 本地测试

```bash
# 安装依赖
pip install ruff pylint bandit safety

# 运行审核脚本
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
