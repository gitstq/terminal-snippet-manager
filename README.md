# 🚀 Terminal Snippet Manager

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <b>English</b> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.zh-TW.md">繁體中文</a>
</p>

---

## 🎉 Introduction

**Terminal Snippet Manager** is a blazing fast, terminal-native code snippet manager designed for developers who live in the command line. It helps you store, organize, search, and execute code snippets without ever leaving your terminal.

### Why Terminal Snippet Manager?

As developers, we constantly reuse code patterns, commands, and configurations. Switching between browsers, GUI apps, and editors breaks our flow. Terminal Snippet Manager brings snippet management directly to where you work — the terminal — with a beautiful TUI interface powered by [Rich](https://github.com/Textualize/rich).

### ✨ Key Features

- ⚡ **Lightning Fast** — Written in Python with optimized fuzzy search
- 🔍 **Smart Search** — Fuzzy matching with relevance scoring
- 🏷️ **Tag System** — Organize snippets with custom tags
- 🎨 **Syntax Highlighting** — Beautiful code display for 15+ languages
- 📋 **Clipboard Integration** — Copy snippets with one command
- ▶️ **Execute Snippets** — Run bash/python snippets directly
- 🌐 **Auto Language Detection** — Automatically identifies programming languages
- 📤 **Import/Export** — JSON backup and restore functionality
- 🔒 **Local Storage** — Your snippets stay on your machine

---

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install terminal-snippet-manager

# Or install with pipx (recommended)
pipx install terminal-snippet-manager
```

### Basic Usage

```bash
# Add a new snippet
tsm add --title "Python Hello World" --code "print('Hello, World!')" --language python

# Search snippets
tsm search "hello"

# List all snippets
tsm list

# Show snippet with syntax highlighting
tsm show <snippet-id>

# Copy to clipboard
tsm copy <snippet-id>

# Execute a snippet (bash/python only)
tsm run <snippet-id>
```

---

## 📖 Detailed Usage Guide

### Adding Snippets

```bash
# Basic addition
tsm add --title "Docker PS" --code "docker ps -a" --language bash

# With description and tags
tsm add \
  --title "Python List Comprehension" \
  --code "squares = [x**2 for x in range(10)]" \
  --language python \
  --description "Create a list of squares" \
  --tags "python,list,comprehension"

# From file
tsm add --title "Config" --file ./config.yaml --language yaml

# From stdin
cat script.py | tsm add --title "My Script" --stdin

# Using editor
tsm add --title "Complex Code" --editor
```

### Searching Snippets

```bash
# Fuzzy search
tsm search "docker compose"

# Filter by language
tsm search "hello" --language python

# Filter by tags
tsm search "config" --tag docker --tag yaml

# List with filters
tsm list --language python --tag utility
```

### Managing Snippets

```bash
# Edit snippet
tsm edit <id> --title "New Title"
tsm edit <id> --editor

# Delete snippet
tsm delete <id>

# Show statistics
tsm stats

# List all languages
tsm languages

# List all tags
tsm tags
```

### Import/Export

```bash
# Export all snippets
tsm export ./my-snippets.json

# Import snippets
tsm import ./my-snippets.json

# Import with merge (default)
tsm import ./snippets.json --merge

# Import with replace
tsm import ./snippets.json --replace
```

---

## 💡 Design Philosophy

### Terminal-Native Experience

We believe the best tools are those that fit seamlessly into your existing workflow. Terminal Snippet Manager is designed for developers who spend most of their time in the terminal.

### Speed First

Every operation is optimized for speed:
- Sub-second fuzzy search across thousands of snippets
- Lazy loading with intelligent caching
- Minimal dependencies for fast startup

### Privacy by Design

Your code snippets are stored locally in `~/.terminal-snippet-manager/`. No cloud, no tracking, no data leaves your machine unless you explicitly export it.

---

## 📦 Supported Languages

Terminal Snippet Manager auto-detects the following languages:

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

## 🔧 Development

```bash
# Clone repository
git clone https://github.com/gitstq/terminal-snippet-manager.git
cd terminal-snippet-manager

# Install development dependencies
pip install -e ".[dev]"

# Run tests
make test

# Format code
make format

# Run linter
make lint
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and development process.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Click](https://click.palletsprojects.com/) — For the beautiful CLI framework
- [Rich](https://github.com/Textualize/rich) — For stunning terminal output
- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) — For fuzzy string matching

---

<p align="center">
  Made with ❤️ for terminal lovers
</p>
