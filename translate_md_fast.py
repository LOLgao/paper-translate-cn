#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 快速翻译脚本 - 使用 DeepSeek API
优化版本：并发翻译 + 批量处理 + 断点续传
"""

import re
import os
import json
import hashlib
from openai import OpenAI
from typing import List, Tuple, Dict
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# 性能配置
MAX_WORKERS = 5  # 并发翻译数量（建议 3-10）
BATCH_SIZE = 2000  # 每批次最大字符数（越大效率越高，但单次调用时间越长）
MAX_RETRIES = 3  # 失败重试次数
RETRY_DELAY = 2  # 重试延迟（秒）

# 初始化客户端
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL
)


class FastMarkdownTranslator:
    def __init__(self, api_key: str = None, max_workers: int = MAX_WORKERS):
        """初始化快速翻译器"""
        if api_key:
            self.client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)
        else:
            self.client = client

        self.max_workers = max_workers
        self.cache_dir = Path(".translation_cache")
        self.cache_dir.mkdir(exist_ok=True)

        # 正则表达式模式
        self.patterns = {
            'math_block': r'\$\$[\s\S]*?\$\$',
            'math_inline': r'\$[^\$\n]+?\$',
            'code_block': r'```[\s\S]*?```',
            'image': r'!\[.*?\]\(.*?\)',
            'table': r'<table>[\s\S]*?</table>',
            'reference': r'\([\w\s]+et al\.,?\s*\d{4}[a-z]?\)',
            'heading': r'^#{1,6}\s+',
            'link': r'\[([^\]]+)\]\(([^\)]+)\)',
        }

    def get_cache_key(self, text: str) -> str:
        """生成缓存键"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def save_to_cache(self, key: str, translation: str):
        """保存到缓存"""
        cache_file = self.cache_dir / f"{key}.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({'translation': translation}, f, ensure_ascii=False)

    def load_from_cache(self, key: str) -> str:
        """从缓存加载"""
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('translation')
        return None

    def protect_special_content(self, text: str) -> Tuple[str, dict]:
        """保护特殊内容"""
        protected = {}
        counter = 0
        result = text

        protect_order = [
            'code_block',
            'math_block',
            'table',
            'image',
            'math_inline',
        ]

        for pattern_name in protect_order:
            pattern = self.patterns[pattern_name]
            matches = list(re.finditer(pattern, result))

            for match in reversed(matches):  # 从后往前替换，避免位置偏移
                placeholder = f"___PROTECTED_{counter}___"
                protected[placeholder] = match.group(0)
                result = result[:match.start()] + placeholder + result[match.end():]
                counter += 1

        return result, protected

    def restore_protected_content(self, text: str, protected: dict) -> str:
        """恢复受保护的内容"""
        result = text
        for placeholder, original in protected.items():
            result = result.replace(placeholder, original)
        return result

    def get_actual_length(self, text: str, protected_map: dict) -> int:
        """
        计算文本的实际长度（包括被保护内容的原始长度）
        用于正确估算翻译块的大小
        """
        actual_length = len(text)

        # 找出文本中的所有占位符
        placeholders = re.findall(r'___PROTECTED_\d+___', text)

        for placeholder in placeholders:
            if placeholder in protected_map:
                # 减去占位符长度，加上原始内容长度
                actual_length = actual_length - len(placeholder) + len(protected_map[placeholder])

        return actual_length

    def should_translate(self, text: str) -> bool:
        """判断文本是否需要翻译"""
        if re.match(r'^___PROTECTED_\d+___$', text.strip()):
            return False
        if re.match(r'^[\d\s\$\-\+\*\/\(\)\[\]\{\}\.,:;]+$', text.strip()):
            return False
        if re.search(r'[a-zA-Z]{2,}', text):
            return True
        return False

    def translate_text_with_retry(self, text: str, retries: int = MAX_RETRIES) -> str:
        """带重试机制的翻译"""
        if not self.should_translate(text):
            return text

        # 检查缓存
        cache_key = self.get_cache_key(text)
        cached = self.load_from_cache(cache_key)
        if cached:
            return cached

        # 构建提示词
        prompt = f"""请将以下英文学术文本翻译成中文。要求：
1. 保持学术性和专业性
2. 不要翻译占位符（如 ___PROTECTED_xxx___）
3. 保持原有的格式、换行和标点符号
4. 只返回翻译结果，不要添加任何解释

文本：
{text}"""

        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个专业的学术论文翻译助手。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=8000
                )

                translation = response.choices[0].message.content.strip()

                # 保存到缓存
                self.save_to_cache(cache_key, translation)

                return translation

            except Exception as e:
                if attempt < retries - 1:
                    print(f"  ⚠️  翻译失败，{RETRY_DELAY}秒后重试 ({attempt + 1}/{retries}): {str(e)[:50]}")
                    time.sleep(RETRY_DELAY)
                else:
                    print(f"  ❌ 翻译失败，返回原文: {str(e)[:50]}")
                    return text

    def split_into_chunks(self, text: str) -> List[Tuple[str, dict]]:
        """
        智能分块：按章节和段落分块
        返回: [(文本块, 保护内容映射), ...]
        """
        # 先保护特殊内容
        protected_text, protected_map = self.protect_special_content(text)

        # 按标题分割（章节级别）
        sections = re.split(r'(^#{1,3}\s+.+$)', protected_text, flags=re.MULTILINE)

        chunks = []
        current_chunk = ""

        for i, section in enumerate(sections):
            if not section.strip():
                continue

            # 如果是标题或添加后超过批次大小，创建新块
            is_heading = re.match(r'^#{1,3}\s+', section)

            # 关键修复：使用实际长度计算，而不是占位符长度
            current_actual_length = self.get_actual_length(current_chunk, protected_map)
            section_actual_length = self.get_actual_length(section, protected_map)
            would_exceed = current_actual_length + section_actual_length > BATCH_SIZE

            if current_chunk and (is_heading or would_exceed):
                # 保存当前块
                chunks.append(current_chunk.strip())
                current_chunk = section + "\n\n"
            else:
                current_chunk += section + "\n\n"

        # 添加最后一块
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # 为每个块分配对应的保护内容
        result = []
        for chunk_text in chunks:
            chunk_protected = {}
            for placeholder, original in protected_map.items():
                if placeholder in chunk_text:
                    chunk_protected[placeholder] = original
            result.append((chunk_text, chunk_protected))

        return result, protected_map

    def translate_chunk(self, chunk_data: Tuple[int, str, dict]) -> Tuple[int, str]:
        """翻译单个块（用于并发）"""
        index, text, protected_map = chunk_data

        # 计算实际长度（包括被保护内容）
        actual_length = self.get_actual_length(text, protected_map)

        print(f"  🔄 正在翻译块 {index + 1}... (占位符长度: {len(text)} 字符, 实际长度: {actual_length} 字符)")
        translation = self.translate_text_with_retry(text)
        print(f"  ✅ 完成块 {index + 1}")
        return index, translation

    def translate_file(self, input_path: str, output_path: str = None):
        """快速翻译文件（并发版本）"""
        if output_path is None:
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_cn{ext}"

        print(f"📖 正在读取文件: {input_path}")
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"📊 文件大小: {len(content)} 字符")
        print(f"🔧 正在分块处理...")

        chunks, protected_map = self.split_into_chunks(content)
        print(f"📦 共分为 {len(chunks)} 个块")
        print(f"⚡ 并发数: {self.max_workers}")
        print()

        # 准备翻译任务（包含 protected_map 用于计算实际长度）
        chunk_texts = [(i, chunk[0], chunk[1]) for i, chunk in enumerate(chunks)]

        # 使用线程池并发翻译
        print("🚀 开始并发翻译...")
        start_time = time.time()

        translated_chunks = [None] * len(chunks)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.translate_chunk, chunk_data)
                      for chunk_data in chunk_texts]

            # 收集结果
            for future in futures:
                index, translation = future.result()
                translated_chunks[index] = translation

        elapsed_time = time.time() - start_time
        print()
        print(f"⏱️  翻译耗时: {elapsed_time:.1f} 秒")
        print(f"📈 平均速度: {len(content) / elapsed_time:.0f} 字符/秒")
        print()

        # 组合翻译结果
        print("🔄 正在组合结果...")
        translated_content = "\n\n".join(translated_chunks)

        # 恢复保护的内容
        print("🔓 正在恢复特殊内容...")
        final_content = self.restore_protected_content(translated_content, protected_map)

        print(f"💾 正在保存到: {output_path}")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print()
        print(f"✅ 翻译完成！")
        print(f"📄 输出文件: {output_path}")
        print(f"📊 缓存目录: {self.cache_dir}")

    def clear_cache(self):
        """清理缓存"""
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(exist_ok=True)
            print("🗑️  缓存已清理")


def main():
    """主函数"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='快速翻译 Markdown 文件')
    parser.add_argument('input', nargs='?', default='full.md', help='输入文件路径')
    parser.add_argument('output', nargs='?', help='输出文件路径（可选）')
    parser.add_argument('--workers', type=int, default=MAX_WORKERS,
                       help=f'并发数量（默认: {MAX_WORKERS}）')
    parser.add_argument('--clear-cache', action='store_true',
                       help='清理翻译缓存')

    args = parser.parse_args()

    # 创建翻译器
    translator = FastMarkdownTranslator(max_workers=args.workers)

    # 清理缓存
    if args.clear_cache:
        translator.clear_cache()
        return

    # 执行翻译
    print("=" * 60)
    print("  快速 Markdown 翻译工具 - DeepSeek API")
    print("=" * 60)
    print()

    translator.translate_file(args.input, args.output)

    print()
    print("💡 提示：")
    print("  - 翻译结果已缓存，重新运行可以复用已翻译的内容")
    print("  - 使用 --clear-cache 参数可以清理缓存")
    print("  - 使用 --workers N 可以调整并发数量")


if __name__ == "__main__":
    main()
