# 🚀 Terminal Snippet Manager

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <a href="README.md">English</a> | <b>简体中文</b> | <a href="README.zh-TW.md">繁體中文</a>
</p>

---

## 🎉 项目介绍

**Terminal Snippet Manager** 是一款极速的终端原生代码片段管理工具，专为在命令行中工作的开发者设计。它帮助你在不离开终端的情况下存储、组织、搜索和执行代码片段。

### 为什么选择 Terminal Snippet Manager？

作为开发者，我们经常重复使用代码模式、命令和配置。在浏览器、GUI应用和编辑器之间切换会打断我们的工作流。Terminal Snippet Manager 将片段管理直接带到你工作的地方——终端——并通过 [Rich](https://github.com/Textualize/rich) 提供精美的 TUI 界面。

### ✨ 核心特性

- ⚡ **极速体验** — 使用 Python 编写，优化的模糊搜索
- 🔍 **智能搜索** — 带相关性评分的模糊匹配
- 🏷️ **标签系统** — 使用自定义标签组织片段
- 🎨 **语法高亮** — 支持 15+ 种语言的精美代码显示
- 📋 **剪贴板集成** — 一键复制片段
- ▶️ **执行片段** — 直接运行 bash/python 片段
- 🌐 **自动语言检测** — 自动识别编程语言
- 📤 **导入/导出** — JSON 备份和恢复功能
- 🔒 **本地存储** — 你的片段保存在本地机器上

---

## 🚀 快速开始

### 安装

```bash
# 从 PyPI 安装
pip install terminal-snippet-manager

# 或使用 pipx 安装（推荐）
pipx install terminal-snippet-manager
```

### 基本使用

```bash
# 添加新片段
tsm add --title "Python Hello World" --code "print('Hello, World!')" --language python

# 搜索片段
tsm search "hello"

# 列出所有片段
tsm list

# 显示带语法高亮的片段
tsm show <snippet-id>

# 复制到剪贴板
tsm copy <snippet-id>

# 执行片段（仅支持 bash/python）
tsm run <snippet-id>
```

---

## 📖 详细使用指南

### 添加片段

```bash
# 基础添加
tsm add --title "Docker PS" --code "docker ps -a" --language bash

# 带描述和标签
tsm add \
  --title "Python 列表推导式" \
  --code "squares = [x**2 for x in range(10)]" \
  --language python \
  --description "创建平方数列表" \
  --tags "python,list,comprehension"

# 从文件添加
tsm add --title "配置" --file ./config.yaml --language yaml

# 从标准输入添加
cat script.py | tsm add --title "我的脚本" --stdin

# 使用编辑器
tsm add --title "复杂代码" --editor
```

### 搜索片段

```bash
# 模糊搜索
tsm search "docker compose"

# 按语言过滤
tsm search "hello" --language python

# 按标签过滤
tsm search "config" --tag docker --tag yaml

# 带过滤条件的列表
tsm list --language python --tag utility
```

### 管理片段

```bash
# 编辑片段
tsm edit <id> --title "新标题"
tsm edit <id> --editor

# 删除片段
tsm delete <id>

# 显示统计信息
tsm stats

# 列出所有语言
tsm languages

# 列出所有标签
tsm tags
```

### 导入/导出

```bash
# 导出所有片段
tsm export ./my-snippets.json

# 导入片段
tsm import ./my-snippets.json

# 合并导入（默认）
tsm import ./snippets.json --merge

# 替换导入
tsm import ./snippets.json --replace
```

---

## 💡 设计理念

### 终端原生体验

我们相信最好的工具是那些能无缝融入现有工作流的工具。Terminal Snippet Manager 专为在终端中花费大部分时间的开发者设计。

### 速度优先

每个操作都经过速度优化：
- 数千片段的亚秒级模糊搜索
- 智能缓存的懒加载
- 最小依赖，快速启动

### 隐私设计

你的代码片段存储在本地 `~/.terminal-snippet-manager/` 目录中。无云端、无追踪，除非你主动导出，否则数据不会离开你的机器。

---

## 📦 支持的语言

Terminal Snippet Manager 自动检测以下语言：

- **Python** (.py)
- **JavaScript/TypeScript** (.js, .ts)
- **Bash/Shell** (.sh, .bash)
- **Go** (.go)
- **Rust** (.rs)
- **Java** (.java)
- **C/C++** (.c, .cpp, .h)
- **Ruby** (.rb)
- **PHP** (.php)
- **SQL** (.sql)
- **HTML/CSS** (.html, .css)
- **JSON/YAML** (.json, .yaml, .yml)

---

## 🔧 开发

```bash
# 克隆仓库
git clone https://github.com/gitstq/terminal-snippet-manager.git
cd terminal-snippet-manager

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
make test

# 格式化代码
make format

# 运行代码检查
make lint
```

---

## 🤝 贡献指南

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'feat: 添加某个 AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解我们的行为准则和开发流程。

---

## 📄 开源协议

本项目采用 MIT 协议 - 详情请参阅 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- [Click](https://click.palletsprojects.com/) — 精美的 CLI 框架
- [Rich](https://github.com/Textualize/rich) — 惊艳的终端输出
- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) — 模糊字符串匹配

---

<p align="center">
  用 ❤️ 为终端爱好者打造
</p>
