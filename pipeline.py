#!/usr/bin/env python3
"""
PDF 论文解析 + 翻译 自动化脚本

完整流程: PDF → MinerU 云端解析 → cleaned.md → 中文翻译

用法:
    # 从 PDF 开始完整流程
    python pipeline.py paper.pdf

    # 已有 MinerU 解析结果的目录（含 content_list.json）
    python pipeline.py /path/to/paper_dir/

    # 只翻译已有的 markdown
    python pipeline.py /path/to/paper_dir/ --skip-mineru

    # 指定并发数
    python pipeline.py paper.pdf --workers 8

    # 跳过翻译，只做解析
    python pipeline.py paper.pdf --skip-translate
"""

import os
import sys
import time
import hashlib
import zipfile
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import requests
except ImportError:
    print("请安装 requests: pip install requests")
    sys.exit(1)

# 确保能导入同目录下的模块（rebuild_markdown, translate_md_fast）
_SCRIPT_DIR = str(Path(__file__).resolve().parent)
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

# ---------------------------------------------------------------------------
# 日志
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("pipeline")

# ---------------------------------------------------------------------------
# MinerU 云端 API 配置
# ---------------------------------------------------------------------------
MINERU_API_TOKEN = os.getenv("MINERU_API_TOKEN", "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiIxNzMwMDI4MCIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTc3MTI0MDgxMiwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiIiwib3BlbklkIjpudWxsLCJ1dWlkIjoiOGIwNGM5OWUtODVmNi00ZTI2LThhY2MtNjA2ZTI5MDM4N2Y1IiwiZW1haWwiOiIiLCJleHAiOjE3NzkwMTY4MTJ9.sAPvgVC-MSoPWMpWRE15QjZCajJ5tFsy89FqAiqPBiQ5qktxV5DyjUKTF7tIBaYNEOOnPMloyKhg3Dty4BhQmA")  # ← 在这里填入你的 token，如: "eyJhbGciOiJIUzI1NiIs..."
MINERU_APPLY_URL = "https://mineru.net/api/v4/file-urls/batch"
MINERU_QUERY_URL = "https://mineru.net/api/v4/extract-results/batch"
MINERU_API_OPTIONS = {
    "model_version": "vlm",
    "enable_formula": True,
    "enable_table": True,
    "language": "ch",
}


def _mineru_headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MINERU_API_TOKEN}",
    }


def _generate_data_id(filename: str, max_bytes: int = 128) -> str:
    """生成符合 API 字节长度限制的 data_id。"""
    stem = Path(filename).stem
    original_id = f"pipeline/{stem}"
    if len(original_id.encode("utf-8")) <= max_bytes:
        return original_id
    file_hash = hashlib.md5(stem.encode("utf-8")).hexdigest()[:8]
    available = max_bytes - len("pipeline/".encode("utf-8")) - 9
    truncated = stem
    while len(truncated.encode("utf-8")) > available:
        truncated = truncated[:-1]
    return f"pipeline/{truncated}_{file_hash}"


def _download_file(url: str, dest: str) -> bool:
    """下载文件到本地。优先用 requests，SSL 失败时回退到系统 curl。"""
    import subprocess

    # 方式 1: requests
    try:
        resp = requests.get(url, timeout=300, stream=True)
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception:
        pass

    # 方式 2: 系统 curl（macOS 自带，使用系统 SSL，兼容性更好）
    logger.info("  requests 下载失败，使用 curl 重试...")
    try:
        result = subprocess.run(
            ["curl", "-fSL", "--retry", "3", "-o", dest, url],
            capture_output=True, text=True, timeout=300,
        )
        if result.returncode == 0 and os.path.exists(dest):
            return True
        logger.warning(f"  curl 失败: {result.stderr.strip()}")
    except Exception as e:
        logger.warning(f"  curl 调用失败: {e}")

    return False


# ---------------------------------------------------------------------------
# MinerU API 函数
# ---------------------------------------------------------------------------

def mineru_apply_upload_urls(files_info: List[Dict]) -> Tuple[str, List[str]]:
    """申请 MinerU 上传链接。返回 (batch_id, [upload_url, ...])。"""
    if not MINERU_API_TOKEN:
        raise RuntimeError(
            "未设置 MINERU_API_TOKEN 环境变量。\n"
            "请设置: export MINERU_API_TOKEN='your_token'\n"
            "获取地址: https://mineru.net"
        )
    data = {"files": files_info, **MINERU_API_OPTIONS}
    resp = requests.post(MINERU_APPLY_URL, headers=_mineru_headers(), json=data, timeout=60)
    resp.raise_for_status()
    result = resp.json()
    if result.get("code") != 0:
        raise RuntimeError(f"MinerU API error: {result.get('msg', 'unknown')}")
    return result["data"]["batch_id"], result["data"]["file_urls"]


def mineru_upload_file(file_path: str, upload_url: str) -> bool:
    """PUT 上传单个文件。"""
    try:
        with open(file_path, "rb") as f:
            resp = requests.put(upload_url, data=f, timeout=300)
            return resp.status_code == 200
    except Exception as e:
        logger.warning(f"上传失败 {file_path}: {e}")
        return False


def mineru_query_batch(batch_id: str) -> Dict:
    """查询批次解析结果。"""
    url = f"{MINERU_QUERY_URL}/{batch_id}"
    resp = requests.get(url, headers=_mineru_headers(), timeout=30)
    resp.raise_for_status()
    result = resp.json()
    if result.get("code") != 0:
        raise RuntimeError(f"MinerU query error: {result.get('msg')}")
    return result["data"]


def mineru_download_and_extract(zip_url: str, dest_dir: str) -> bool:
    """下载 ZIP 并解压，将 full.md / content_list.json 放到 dest_dir。"""
    zip_path = os.path.join(dest_dir, "mineru_result.zip")
    os.makedirs(dest_dir, exist_ok=True)

    # 下载（3次重试）
    for attempt in range(3):
        if _download_file(zip_url, zip_path):
            logger.info(f"  下载成功: {os.path.getsize(zip_path)} bytes")
            break
        logger.warning(f"  下载重试 ({attempt + 1}/3)...")
        if attempt < 2:
            time.sleep(3)
    else:
        logger.error("  下载失败（3次重试均失败）")
        return False

    # 解压
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(dest_dir)
    except Exception as e:
        logger.error(f"  解压失败: {e}")
        return False

    # 查找 full.md 并移动到 dest_dir 根级别
    dest_fullmd = os.path.join(dest_dir, "full.md")
    if not os.path.exists(dest_fullmd):
        for root, _dirs, files in os.walk(dest_dir):
            for fname in files:
                if fname == "full.md":
                    src = os.path.join(root, fname)
                    if src != dest_fullmd:
                        os.rename(src, dest_fullmd)
                    break
            if os.path.exists(dest_fullmd):
                break

    # 搬运 content_list*.json 和 images/ 到 dest_dir 根级别
    for root, _dirs, files in os.walk(dest_dir):
        for fname in files:
            if fname.endswith("_content_list.json") or fname.endswith("content_list_v2.json"):
                src = os.path.join(root, fname)
                dest_cl = os.path.join(dest_dir, fname)
                if src != dest_cl:
                    try:
                        os.rename(src, dest_cl)
                    except OSError:
                        pass

    # 搬运 images 目录
    dest_images = os.path.join(dest_dir, "images")
    if not os.path.exists(dest_images):
        for root, dirs, _files in os.walk(dest_dir):
            if "images" in dirs and root != dest_dir:
                src_images = os.path.join(root, "images")
                try:
                    os.rename(src_images, dest_images)
                except OSError:
                    pass
                break

    # 清理 zip
    try:
        os.remove(zip_path)
    except OSError:
        pass

    return os.path.exists(dest_fullmd)


# ---------------------------------------------------------------------------
# Phase 1: MinerU 解析
# ---------------------------------------------------------------------------

def run_mineru(
    pdf_path: str,
    paper_dir: str,
    poll_interval: int = 30,
    poll_timeout: int = 3600,
) -> bool:
    """
    PDF → MinerU 云端解析 → 下载结果。

    返回 True 成功, False 失败。
    """
    pdf_name = os.path.basename(pdf_path)
    data_id = _generate_data_id(pdf_name)

    logger.info(f"[MinerU] 开始解析: {pdf_name}")
    logger.info(f"  data_id = {data_id}")

    # 1. 申请上传链接
    try:
        files_info = [{"name": pdf_name, "data_id": data_id}]
        batch_id, upload_urls = mineru_apply_upload_urls(files_info)
        logger.info(f"  batch_id = {batch_id}")
    except Exception as e:
        logger.error(f"  申请上传链接失败: {e}")
        return False

    # 2. 上传文件
    if not mineru_upload_file(pdf_path, upload_urls[0]):
        logger.error(f"  上传失败: {pdf_name}")
        return False
    logger.info("  上传成功")

    # 3. 轮询等待
    logger.info(f"  等待解析（轮询间隔 {poll_interval}s，超时 {poll_timeout}s）...")
    start = time.time()

    while (time.time() - start) < poll_timeout:
        time.sleep(poll_interval)
        elapsed_min = (time.time() - start) / 60

        try:
            result_data = mineru_query_batch(batch_id)
        except Exception as e:
            logger.warning(f"  查询失败: {e}（重试中）")
            continue

        file_results = result_data.get("extract_result", [])
        if not file_results:
            logger.info(f"  等待中... ({elapsed_min:.1f}min)")
            continue

        fr = file_results[0]
        state = fr.get("state", "unknown")
        logger.info(f"  状态: {state} ({elapsed_min:.1f}min)")

        if state == "done":
            zip_url = fr.get("full_zip_url")
            if not zip_url:
                logger.error("  解析完成但未获取到下载链接")
                return False

            os.makedirs(paper_dir, exist_ok=True)
            ok = mineru_download_and_extract(zip_url, paper_dir)
            if ok:
                logger.info(f"  MinerU 解析成功 → {paper_dir}")
            else:
                logger.error("  下载/解压失败")
            return ok

        elif state == "failed":
            logger.error("  MinerU 解析失败")
            return False

    logger.error(f"  MinerU 超时（{poll_timeout}s）")
    return False


# ---------------------------------------------------------------------------
# Phase 2: rebuild cleaned.md
# ---------------------------------------------------------------------------

def run_rebuild(paper_dir: str) -> bool:
    """从 content_list.json 生成 cleaned.md。失败时跳过，直接使用 full.md。"""
    d = Path(paper_dir)

    # 检查是否有 content_list.json
    has_content_list = bool(list(d.glob("*content_list*.json")))
    if not has_content_list:
        logger.info("  无 content_list.json，跳过 rebuild（将直接使用 full.md）")
        return True

    try:
        from rebuild_markdown import process_paper
    except ImportError:
        logger.warning("  rebuild_markdown 模块不可用，跳过（将直接使用 full.md）")
        return True

    logger.info("[Rebuild] 生成 cleaned.md ...")
    try:
        ok = process_paper(d, enable_vl=False)
        if ok:
            logger.info("  cleaned.md 生成成功")
        else:
            logger.warning("  cleaned.md 生成失败（将回退到 full.md）")
        return True
    except Exception as e:
        logger.warning(f"  生成 cleaned.md 异常: {e}（将回退到 full.md）")
        return True


# ---------------------------------------------------------------------------
# Phase 3: 翻译
# ---------------------------------------------------------------------------

def run_translate(paper_dir: str, workers: int = 5) -> bool:
    """翻译 cleaned.md (或 full.md) 为中文。"""
    from translate_md_fast import FastMarkdownTranslator

    d = Path(paper_dir)

    # 优先使用 cleaned.md，回退 full.md
    input_file = None
    for name in ("cleaned.md", "full.md"):
        candidate = d / name
        if candidate.exists():
            input_file = str(candidate)
            break

    if input_file is None:
        logger.error("  未找到可翻译的 Markdown 文件（cleaned.md 或 full.md）")
        return False

    # 输出到 translate/ 子目录
    translate_dir = d 
    translate_dir.mkdir(exist_ok=True)
    basename = Path(input_file).stem
    output_file = str(translate_dir / f"{basename}_cn.md")

    logger.info(f"[翻译] {Path(input_file).name} → {Path(output_file).name}")
    logger.info(f"  并发数: {workers}")

    try:
        translator = FastMarkdownTranslator(max_workers=workers)
        translator.translate_file(input_file, output_file)
        logger.info(f"  翻译完成 → {output_file}")
        return True
    except Exception as e:
        logger.error(f"  翻译失败: {e}")
        return False


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def resolve_input(paper_path: str) -> Tuple[str, Optional[str]]:
    """
    解析输入路径，返回 (paper_dir, pdf_path_or_None)。

    - PDF 文件 → paper_dir 为同级目录下 "<stem>-<hash>" 子目录
    - 目录 → 直接作为 paper_dir
    - .md 文件 → paper_dir 为所在目录
    """
    p = Path(paper_path).resolve()

    if p.is_file() and p.suffix.lower() == ".pdf":
        # 用文件名生成 paper_dir
        paper_dir = str(p.parent / p.stem)
        return paper_dir, str(p)

    elif p.is_dir():
        return str(p), None

    elif p.is_file() and p.suffix.lower() == ".md":
        return str(p.parent), None

    else:
        raise FileNotFoundError(f"路径不存在: {paper_path}")


def main():
    parser = argparse.ArgumentParser(
        description="PDF 论文解析 + 翻译 自动化脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 完整流程: PDF → MinerU 解析 → cleaned.md → 翻译
  python pipeline.py paper.pdf

  # 已有解析结果的目录，只做 rebuild + 翻译
  python pipeline.py /path/to/paper_dir/

  # 跳过 MinerU，只翻译
  python pipeline.py /path/to/paper_dir/ --skip-mineru

  # 跳过翻译，只做解析
  python pipeline.py paper.pdf --skip-translate

  # 调整翻译并发数
  python pipeline.py paper.pdf --workers 8
        """,
    )

    parser.add_argument("input", help="PDF 文件路径、论文目录或 Markdown 文件路径")
    parser.add_argument("--skip-mineru", action="store_true", help="跳过 MinerU 解析")
    parser.add_argument("--skip-translate", action="store_true", help="跳过翻译")
    parser.add_argument("--workers", type=int, default=5, help="翻译并发数（默认: 5）")
    parser.add_argument("--poll-interval", type=int, default=30, help="MinerU 轮询间隔秒数（默认: 30）")
    parser.add_argument("--poll-timeout", type=int, default=3600, help="MinerU 轮询超时秒数（默认: 3600）")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    start_time = time.time()

    logger.info("=" * 60)
    logger.info("  PDF 论文解析 + 翻译 Pipeline")
    logger.info("=" * 60)

    # ── 解析输入 ──
    try:
        paper_dir, pdf_path = resolve_input(args.input)
        paper_dir = str('./data/' + paper_dir)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    logger.info(f"  论文目录 : {paper_dir}")
    logger.info(f"  PDF 文件 : {pdf_path or '(无)'}")
    logger.info("=" * 60)

    # ── Phase 1: MinerU 解析 ──
    if pdf_path and not args.skip_mineru:
        # 检查是否已有解析结果
        d = Path(paper_dir)
        has_md = (d / "cleaned.md").exists() or (d / "full.md").exists()
        if has_md:
            logger.info("\n[Phase 1] 已有 Markdown，跳过 MinerU")
        else:
            logger.info("\n[Phase 1] PDF → MinerU 解析")
            ok = run_mineru(
                pdf_path, paper_dir,
                poll_interval=args.poll_interval,
                poll_timeout=args.poll_timeout,
            )
            if not ok:
                logger.error("MinerU 解析失败，退出")
                return 1
    else:
        logger.info("\n[Phase 1] 跳过 MinerU")

    # ── Phase 2: rebuild cleaned.md ──
    logger.info("\n[Phase 2] 重建 cleaned.md")
    d = Path(paper_dir)
    if not (d / "cleaned.md").exists():
        run_rebuild(paper_dir)
    else:
        logger.info("  cleaned.md 已存在，跳过")

    # ── Phase 3: 翻译 ──
    if not args.skip_translate:
        logger.info("\n[Phase 3] Markdown → 中文翻译")
        ok = run_translate(paper_dir, workers=args.workers)
        if not ok:
            logger.error("翻译失败")
            return 1
    else:
        logger.info("\n[Phase 3] 跳过翻译")

    # ── 汇总 ──
    elapsed = time.time() - start_time
    mins, secs = divmod(int(elapsed), 60)

    logger.info(f"\n{'=' * 60}")
    logger.info("  Pipeline 完成")
    logger.info(f"{'=' * 60}")
    logger.info(f"  论文目录   : {paper_dir}")
    logger.info(f"  耗时       : {mins}m {secs}s")

    # 列出输出文件
    d = Path(paper_dir)
    outputs = []
    for name in ("full.md", "cleaned.md", "figure_map.json"):
        if (d / name).exists():
            outputs.append(name)
    translate_dir = d / "translate"
    if translate_dir.exists():
        for f in translate_dir.iterdir():
            outputs.append(f"translate/{f.name}")
    logger.info(f"  输出文件   : {', '.join(outputs)}")
    logger.info("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
