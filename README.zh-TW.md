# 🚀 Terminal Snippet Manager

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <b>繁體中文</b>
</p>

---

## 🎉 專案介紹

**Terminal Snippet Manager** 是一款極速的終端原生程式碼片段管理工具，專為在命令列中工作的開發者設計。它幫助你在不離開終端的情況下儲存、組織、搜尋和執行程式碼片段。

### 為什麼選擇 Terminal Snippet Manager？

作為開發者，我們經常重複使用程式碼模式、命令和設定。在瀏覽器、GUI 應用程式和編輯器之間切換會打斷我們的工作流程。Terminal Snippet Manager 將片段管理直接帶到你工作的地方——終端——並透過 [Rich](https://github.com/Textualize/rich) 提供精美的 TUI 介面。

### ✨ 核心特性

- ⚡ **極速體驗** — 使用 Python 編寫，最佳化的模糊搜尋
- 🔍 **智慧搜尋** — 帶相關性評分的模糊匹配
- 🏷️ **標籤系統** — 使用自訂標籤組織片段
- 🎨 **語法高亮** — 支援 15+ 種語言的精美程式碼顯示
- 📋 **剪貼簿整合** — 一鍵複製片段
- ▶️ **執行片段** — 直接執行 bash/python 片段
- 🌐 **自動語言偵測** — 自動識別程式語言
- 📤 **匯入/匯出** — JSON 備份和還原功能
- 🔒 **本地儲存** — 你的片段儲存在本地機器上

---

## 🚀 快速開始

### 安裝

```bash
# 從 PyPI 安裝
pip install terminal-snippet-manager

# 或使用 pipx 安裝（推薦）
pipx install terminal-snippet-manager
```

### 基本使用

```bash
# 新增片段
tsm add --title "Python Hello World" --code "print('Hello, World!')" --language python

# 搜尋片段
tsm search "hello"

# 列出所有片段
tsm list

# 顯示帶語法高亮的片段
tsm show <snippet-id>

# 複製到剪貼簿
tsm copy <snippet-id>

# 執行片段（僅支援 bash/python）
tsm run <snippet-id>
```

---

## 📖 詳細使用指南

### 新增片段

```bash
# 基礎新增
tsm add --title "Docker PS" --code "docker ps -a" --language bash

# 帶描述和標籤
tsm add \
  --title "Python 列表推導式" \
  --code "squares = [x**2 for x in range(10)]" \
  --language python \
  --description "建立平方數列表" \
  --tags "python,list,comprehension"

# 從檔案新增
tsm add --title "設定" --file ./config.yaml --language yaml

# 從標準輸入新增
cat script.py | tsm add --title "我的腳本" --stdin

# 使用編輯器
tsm add --title "複雜程式碼" --editor
```

### 搜尋片段

```bash
# 模糊搜尋
tsm search "docker compose"

# 按語言篩選
tsm search "hello" --language python

# 按標籤篩選
tsm search "config" --tag docker --tag yaml

# 帶篩選條件的列表
tsm list --language python --tag utility
```

### 管理片段

```bash
# 編輯片段
tsm edit <id> --title "新標題"
tsm edit <id> --editor

# 刪除片段
tsm delete <id>

# 顯示統計資訊
tsm stats

# 列出所有語言
tsm languages

# 列出所有標籤
tsm tags
```

### 匯入/匯出

```bash
# 匯出所有片段
tsm export ./my-snippets.json

# 匯入片段
tsm import ./my-snippets.json

# 合併匯入（預設）
tsm import ./snippets.json --merge

# 取代匯入
tsm import ./snippets.json --replace
```

---

## 💡 設計理念

### 終端原生體驗

我們相信最好的工具是那些能無縫融入現有工作流程的工具。Terminal Snippet Manager 專為在終端中花費大部分時間的開發者設計。

### 速度優先

每個操作都經過速度最佳化：
- 數千片段的亞秒級模糊搜尋
- 智慧快取的延遲載入
- 最小依賴，快速啟動

### 隱私設計

你的程式碼片段儲存在本地 `~/.terminal-snippet-manager/` 目錄中。無雲端、無追蹤，除非你主動匯出，否則資料不會離開你的機器。

---

## 📦 支援的語言

Terminal Snippet Manager 自動偵測以下語言：

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

## 🔧 開發

```bash
# 克隆倉庫
git clone https://github.com/gitstq/terminal-snippet-manager.git
cd terminal-snippet-manager

# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
make test

# 格式化程式碼
make format

# 執行程式碼檢查
make lint
```

---

## 🤝 貢獻指南

歡迎貢獻！請隨時提交 Pull Request。

1. Fork 本倉庫
2. 建立你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'feat: 新增某個 AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

請閱讀 [CONTRIBUTING.md](CONTRIBUTING.md) 了解我們的行為準則和開發流程。

---

## 📄 開源協議

本專案採用 MIT 協議 - 詳情請參閱 [LICENSE](LICENSE) 檔案。

---

## 🙏 致謝

- [Click](https://click.palletsprojects.com/) — 精美的 CLI 框架
- [Rich](https://github.com/Textualize/rich) — 驚豔的終端輸出
- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) — 模糊字串匹配

---

<p align="center">
  用 ❤️ 為終端愛好者打造
</p>
