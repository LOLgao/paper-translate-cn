# Paper Translate

PDF 学术论文自动解析 + 中文翻译工具。

完整流程：PDF → MinerU 云端解析 → Markdown → DeepSeek 中文翻译

## 功能特点

- **MinerU 云端解析**：支持公式、表格、图片提取，生成结构化 Markdown
- **DeepSeek 翻译**：并发翻译 + 断点续传 + 翻译缓存，避免重复调用 API
- **智能分块**：按章节和段落自动分块，保护公式、���码、表格等特殊内容不被翻译
- **一键运行**：从 PDF 到中文翻译全自动完成

## 项目结构

```
paper_translate/
├── pipeline.py            # 主流程脚本
├── translate_md_fast.py   # Markdown 翻译模块
├── rebuild_markdown.py    # Markdown 重建模块（可选）
├── requirements.txt       # Python 依赖
├── .env                   # API 密钥配置（不上传）
├── .env.example           # 配置模板
├── papers/                # 放置待翻译的 PDF 文件
└── data/                  # 输出目录（解析结果 + 翻译）
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API 密钥

复制配置模板并填入你的密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```
DEEPSEEK_API_KEY=你的DeepSeek密钥
MINERU_API_TOKEN=你的MinerU令牌
```

- DeepSeek API Key：[https://platform.deepseek.com](https://platform.deepseek.com)
- MinerU Token：[https://mineru.net](https://mineru.net)

### 3. 放置 PDF

将 PDF 论文放入 `papers/` 目录。

### 4. 运行

```bash
# 完整流程：PDF → 解析 → 翻译
python pipeline.py paper.pdf

# 指定并发数
python pipeline.py paper.pdf --workers 8

# 跳过翻译，只做解析
python pipeline.py paper.pdf --skip-translate

# 跳过解析，只做翻译（已有解析结果时）
python pipeline.py paper.pdf --skip-mineru
```

输出结果在 `data/<论文名>/` 目录下，包含：

- `full.md` — MinerU 解析的原始 Markdown
- `cleaned.md` — 清洗后的 Markdown（如果有 rebuild 模块）
- `full_cn.md` / `cleaned_cn.md` — 中文翻译

### 单独使用翻译模块

```bash
python translate_md_fast.py input.md output_cn.md --workers 5
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | PDF 文件名（在 papers/ 下）或目录路径 | - |
| `--skip-mineru` | 跳过 MinerU 解析 | False |
| `--skip-translate` | 跳过翻译 | False |
| `--workers` | 翻译并发数 | 5 |
| `--poll-interval` | MinerU 轮询间隔（秒） | 30 |
| `--poll-timeout` | MinerU 轮询超时（秒） | 3600 |
| `-v` | 详细输出 | False |
