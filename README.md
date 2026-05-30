<div align="center">

# 📄 DocParse-Pro

**A Powerful Document Parsing Tool with OCR, Table Extraction & Multi-Format Output**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)**

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Introduction

DocParse-Pro is a powerful, easy-to-use document parsing tool designed to extract text, tables, and metadata from PDF documents and images. Built with Python, it features intelligent OCR capabilities, multi-format output support, and a beautiful TUI interface.

**Key Highlights:**
- 🚀 **Fast & Efficient**: Optimized parsing engine for quick document processing
- 🔍 **Smart OCR**: Integrated Tesseract OCR for scanned documents
- 📊 **Table Extraction**: Automatically detect and extract tables
- 📤 **Multi-Format Output**: JSON, Markdown, CSV, and plain text
- ⚡ **Batch Processing**: Process entire directories of documents
- 🖥️ **Beautiful CLI**: Rich terminal interface with progress indicators

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📄 **PDF Parsing** | Extract text, tables, and metadata from PDF files |
| 🖼️ **Image OCR** | Recognize text from images and scanned documents |
| 📊 **Table Extraction** | Automatically detect and extract table structures |
| 📤 **Multi-Format Output** | Export to JSON, Markdown, CSV, or plain text |
| ⚡ **Batch Processing** | Process multiple files in one command |
| 🌐 **Multi-Language OCR** | Support for 100+ languages via Tesseract |

### 🚀 Quick Start

#### Requirements
- Python 3.10 or higher
- Tesseract OCR (optional, for OCR features)

#### Installation

```bash
# Install from PyPI
pip install docparse-pro

# Or install from source
git clone https://github.com/yourusername/DocParse-Pro.git
cd DocParse-Pro
pip install -e .
```

#### Install Tesseract (for OCR)

```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

#### Basic Usage

```bash
# Parse a PDF document
docparse parse document.pdf

# Parse with OCR enabled
docparse parse scanned.pdf --ocr --lang eng

# Output as JSON
docparse parse document.pdf --format json -o output.json

# Parse specific pages
docparse parse document.pdf --pages "1-5,10,15-20"

# Batch process a directory
docparse batch ./documents ./output --format markdown
```

### 📖 Detailed Usage Guide

#### Command Reference

**`docparse parse`** - Parse a single document

| Option | Description |
|--------|-------------|
| `-o, --output` | Output file path |
| `-f, --format` | Output format (json/text/markdown/csv) |
| `-p, --pages` | Pages to parse (e.g., "1-5,10,15-20") |
| `--ocr` | Enable OCR for scanned documents |
| `-l, --lang` | OCR language (default: eng) |
| `--tables` | Extract tables (default: True) |
| `-V, --verbose` | Verbose output |

**`docparse batch`** - Batch process documents

| Option | Description |
|--------|-------------|
| `-f, --format` | Output format |
| `--ocr` | Enable OCR |
| `-l, --lang` | OCR language |
| `-r, --recursive` | Process directories recursively |
| `-e, --extension` | File extensions to process |

**`docparse ocr`** - OCR configuration

| Option | Description |
|--------|-------------|
| `--check` | Check Tesseract installation |

#### Python API

```python
from docparse_pro import DocumentParser, OCREngine, OutputFormatter

# Parse a document
parser = DocumentParser()
content = parser.parse("document.pdf")

print(f"Text: {content.text[:200]}...")
print(f"Tables found: {len(content.tables)}")
print(f"Pages: {len(content.pages)}")

# Perform OCR
ocr = OCREngine(language="eng")
result = ocr.recognize("scanned_image.png")
print(f"Recognized text: {result.text}")

# Format output
formatter = OutputFormatter("markdown")
output = formatter.format(content)
print(output)
```

### 💡 Design Philosophy

DocParse-Pro was designed with the following principles:

1. **Simplicity First**: Easy to install and use, with sensible defaults
2. **Extensibility**: Modular architecture allows easy addition of new parsers and formatters
3. **Performance**: Optimized for speed without sacrificing accuracy
4. **Developer-Friendly**: Clean API, comprehensive documentation, type hints

### 📦 Packaging & Deployment

#### Build from Source

```bash
# Install build tools
pip install build

# Build package
python -m build

# The built packages will be in dist/
```

#### Docker Support

```dockerfile
FROM python:3.11-slim

# Install Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr

# Install DocParse-Pro
RUN pip install docparse-pro

ENTRYPOINT ["docparse"]
```

### 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

DocParse-Pro 是一款功能强大、易于使用的文档解析工具，专为从 PDF 文档和图像中提取文本、表格和元数据而设计。基于 Python 构建，具备智能 OCR 能力、多格式输出支持和美观的 TUI 界面。

**核心亮点：**
- 🚀 **快速高效**：优化的解析引擎，快速处理文档
- 🔍 **智能 OCR**：集成 Tesseract OCR，支持扫描文档
- 📊 **表格提取**：自动检测并提取表格结构
- 📤 **多格式输出**：支持 JSON、Markdown、CSV 和纯文本
- ⚡ **批量处理**：一键处理整个文档目录
- 🖥️ **美观界面**：Rich 终端界面，带进度指示器

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📄 **PDF 解析** | 从 PDF 文件中提取文本、表格和元数据 |
| 🖼️ **图像 OCR** | 识别图像和扫描文档中的文字 |
| 📊 **表格提取** | 自动检测并提取表格结构 |
| 📤 **多格式输出** | 导出为 JSON、Markdown、CSV 或纯文本 |
| ⚡ **批量处理** | 一条命令处理多个文件 |
| 🌐 **多语言 OCR** | 通过 Tesseract 支持 100+ 种语言 |

### 🚀 快速开始

#### 环境要求
- Python 3.10 或更高版本
- Tesseract OCR（可选，用于 OCR 功能）

#### 安装方式

```bash
# 从 PyPI 安装
pip install docparse-pro

# 或从源码安装
git clone https://github.com/yourusername/DocParse-Pro.git
cd DocParse-Pro
pip install -e .
```

#### 安装 Tesseract（用于 OCR）

```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# 从以下地址下载：https://github.com/UB-Mannheim/tesseract/wiki
```

#### 基本用法

```bash
# 解析 PDF 文档
docparse parse document.pdf

# 启用 OCR 解析扫描文档
docparse parse scanned.pdf --ocr --lang chi_sim

# 输出为 JSON 格式
docparse parse document.pdf --format json -o output.json

# 解析指定页面
docparse parse document.pdf --pages "1-5,10,15-20"

# 批量处理目录
docparse batch ./documents ./output --format markdown
```

### 📖 详细使用指南

#### 命令参考

**`docparse parse`** - 解析单个文档

| 选项 | 描述 |
|------|------|
| `-o, --output` | 输出文件路径 |
| `-f, --format` | 输出格式 (json/text/markdown/csv) |
| `-p, --pages` | 要解析的页面（如 "1-5,10,15-20"） |
| `--ocr` | 启用 OCR 处理扫描文档 |
| `-l, --lang` | OCR 语言（默认：eng） |
| `--tables` | 提取表格（默认：True） |
| `-V, --verbose` | 详细输出 |

**`docparse batch`** - 批量处理文档

| 选项 | 描述 |
|------|------|
| `-f, --format` | 输出格式 |
| `--ocr` | 启用 OCR |
| `-l, --lang` | OCR 语言 |
| `-r, --recursive` | 递归处理目录 |
| `-e, --extension` | 要处理的文件扩展名 |

**`docparse ocr`** - OCR 配置

| 选项 | 描述 |
|------|------|
| `--check` | 检查 Tesseract 安装状态 |

#### Python API

```python
from docparse_pro import DocumentParser, OCREngine, OutputFormatter

# 解析文档
parser = DocumentParser()
content = parser.parse("document.pdf")

print(f"文本内容: {content.text[:200]}...")
print(f"发现表格: {len(content.tables)} 个")
print(f"总页数: {len(content.pages)} 页")

# 执行 OCR
ocr = OCREngine(language="chi_sim")
result = ocr.recognize("scanned_image.png")
print(f"识别文本: {result.text}")

# 格式化输出
formatter = OutputFormatter("markdown")
output = formatter.format(content)
print(output)
```

### 💡 设计理念

DocParse-Pro 的设计遵循以下原则：

1. **简单至上**：易于安装和使用，提供合理的默认配置
2. **可扩展性**：模块化架构，便于添加新的解析器和格式化器
3. **高性能**：在保证准确性的同时优化处理速度
4. **开发者友好**：清晰的 API、完善的文档、完整的类型提示

### 📦 打包与部署

#### 从源码构建

```bash
# 安装构建工具
pip install build

# 构建包
python -m build

# 构建产物位于 dist/ 目录
```

#### Docker 支持

```dockerfile
FROM python:3.11-slim

# 安装 Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr

# 安装 DocParse-Pro
RUN pip install docparse-pro

ENTRYPOINT ["docparse"]
```

### 🤝 贡献指南

欢迎参与贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 📄 开源协议

本项目采用 MIT 协议开源 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 🇹🇼 繁體中文

### 🎉 專案介紹

DocParse-Pro 是一款功能強大、易於使用的文件解析工具，專為從 PDF 文件和影像中提取文字、表格和元資料而設計。基於 Python 構建，具備智慧 OCR 能力、多格式輸出支援和美觀的 TUI 介面。

**核心亮點：**
- 🚀 **快速高效**：最佳化的解析引擎，快速處理文件
- 🔍 **智慧 OCR**：整合 Tesseract OCR，支援掃描文件
- 📊 **表格提取**：自動偵測並提取表格結構
- 📤 **多格式輸出**：支援 JSON、Markdown、CSV 和純文字
- ⚡ **批次處理**：一鍵處理整個文件目錄
- 🖥️ **美觀介面**：Rich 終端介面，帶進度指示器

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📄 **PDF 解析** | 從 PDF 檔案中提取文字、表格和元資料 |
| 🖼️ **影像 OCR** | 辨識影像和掃描文件中的文字 |
| 📊 **表格提取** | 自動偵測並提取表格結構 |
| 📤 **多格式輸出** | 匯出為 JSON、Markdown、CSV 或純文字 |
| ⚡ **批次處理** | 一條指令處理多個檔案 |
| 🌐 **多語言 OCR** | 透過 Tesseract 支援 100+ 種語言 |

### 🚀 快速開始

#### 環境需求
- Python 3.10 或更高版本
- Tesseract OCR（選用，用於 OCR 功能）

#### 安裝方式

```bash
# 從 PyPI 安裝
pip install docparse-pro

# 或從原始碼安裝
git clone https://github.com/yourusername/DocParse-Pro.git
cd DocParse-Pro
pip install -e .
```

#### 安裝 Tesseract（用於 OCR）

```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# 從以下網址下載：https://github.com/UB-Mannheim/tesseract/wiki
```

#### 基本用法

```bash
# 解析 PDF 文件
docparse parse document.pdf

# 啟用 OCR 解析掃描文件
docparse parse scanned.pdf --ocr --lang chi_tra

# 輸出為 JSON 格式
docparse parse document.pdf --format json -o output.json

# 解析指定頁面
docparse parse document.pdf --pages "1-5,10,15-20"

# 批次處理目錄
docparse batch ./documents ./output --format markdown
```

### 📖 詳細使用指南

#### 指令參考

**`docparse parse`** - 解析單一文件

| 選項 | 描述 |
|------|------|
| `-o, --output` | 輸出檔案路徑 |
| `-f, --format` | 輸出格式 (json/text/markdown/csv) |
| `-p, --pages` | 要解析的頁面（如 "1-5,10,15-20"） |
| `--ocr` | 啟用 OCR 處理掃描文件 |
| `-l, --lang` | OCR 語言（預設：eng） |
| `--tables` | 提取表格（預設：True） |
| `-V, --verbose` | 詳細輸出 |

**`docparse batch`** - 批次處理文件

| 選項 | 描述 |
|------|------|
| `-f, --format` | 輸出格式 |
| `--ocr` | 啟用 OCR |
| `-l, --lang` | OCR 語言 |
| `-r, --recursive` | 遞迴處理目錄 |
| `-e, --extension` | 要處理的檔案副檔名 |

**`docparse ocr`** - OCR 設定

| 選項 | 描述 |
|------|------|
| `--check` | 檢查 Tesseract 安裝狀態 |

#### Python API

```python
from docparse_pro import DocumentParser, OCREngine, OutputFormatter

# 解析文件
parser = DocumentParser()
content = parser.parse("document.pdf")

print(f"文字內容: {content.text[:200]}...")
print(f"發現表格: {len(content.tables)} 個")
print(f"總頁數: {len(content.pages)} 頁")

# 執行 OCR
ocr = OCREngine(language="chi_tra")
result = ocr.recognize("scanned_image.png")
print(f"辨識文字: {result.text}")

# 格式化輸出
formatter = OutputFormatter("markdown")
output = formatter.format(content)
print(output)
```

### 💡 設計理念

DocParse-Pro 的設計遵循以下原則：

1. **簡單至上**：易於安裝和使用，提供合理的預設設定
2. **可擴展性**：模組化架構，便於新增新的解析器和格式化器
3. **高效能**：在保證準確性的同時最佳化處理速度
4. **開發者友善**：清晰的 API、完善的文件、完整的類型提示

### 📦 打包與部署

#### 從原始碼建構

```bash
# 安裝建構工具
pip install build

# 建構套件
python -m build

# 建構產物位於 dist/ 目錄
```

#### Docker 支援

```dockerfile
FROM python:3.11-slim

# 安裝 Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr

# 安裝 DocParse-Pro
RUN pip install docparse-pro

ENTRYPOINT ["docparse"]
```

### 🤝 貢獻指南

歡迎參與貢獻！請查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解詳情。

### 📄 開源授權

本專案採用 MIT 授權條款開源 - 詳見 [LICENSE](LICENSE) 檔案。

---

<div align="center">

**Made with ❤️ by DocParse-Pro Team**

**[⬆ Back to Top](#docparse-pro)**

</div>
