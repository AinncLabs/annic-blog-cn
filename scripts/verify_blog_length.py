#!/usr/bin/env python3
"""Keep Chinese blog posts concise, concrete, readable, and quotable."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


MIN_ARTICLE_CHARS = 500
MAX_ARTICLE_CHARS = 1200
MIN_PARAGRAPHS = 3
MIN_SENTENCES = 8
MAX_PARAGRAPH_CHARS = 320
MIN_QUOTE_CHARS = 12
MAX_QUOTE_CHARS = 90
CONCRETE_MARKERS = (
    "比如",
    "例如",
    "举个例子",
    "具体",
    "假设",
    "第一",
    "第二",
    "第三",
)


def sentence_split(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"[。！？!?]", text) if part.strip()]


def repetition_check(sentences: list[str]) -> list[tuple[int, int, float]]:
    """Flag sentence pairs that are likely saying the same thing twice."""
    suspicious_pairs: list[tuple[int, int, float]] = []
    for i, first in enumerate(sentences):
        for j in range(i + 1, len(sentences)):
            second = sentences[j]
            if len(first) < 18 or len(second) < 18:
                continue
            first_chars = set(first)
            second_chars = set(second)
            overlap = len(first_chars & second_chars) / max(
                len(first_chars), len(second_chars)
            )
            if overlap > 0.72:
                suspicious_pairs.append((i + 1, j + 1, round(overlap, 2)))
    return suspicious_pairs


def has_concrete_content(text: str) -> bool:
    return bool(re.search(r"\d", text)) or any(
        marker in text for marker in CONCRETE_MARKERS
    )


def strip_frontmatter(content: str) -> str:
    if not content.startswith("---"):
        return content
    match = re.match(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", content, flags=re.S)
    return content[match.end() :] if match else content


def plain_text(markdown: str) -> str:
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", markdown)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_article(content: str) -> tuple[list[str], list[str], list[str]]:
    """Return prose paragraphs, blockquotes, and all visible body chunks."""
    content = strip_frontmatter(content)
    paragraphs: list[str] = []
    quotes: list[str] = []
    visible_chunks: list[str] = []
    buffer: list[str] = []
    in_fence = False
    in_comment = False
    html_block: str | None = None

    def flush() -> None:
        if not buffer:
            return
        paragraph = plain_text(" ".join(buffer))
        if paragraph:
            paragraphs.append(paragraph)
            visible_chunks.append(paragraph)
        buffer.clear()

    for raw_line in content.splitlines():
        line = raw_line.strip()

        if line.startswith("```"):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if line.startswith("<!--"):
            flush()
            if "-->" not in line:
                in_comment = True
            continue

        if html_block:
            if re.search(rf"</{re.escape(html_block)}>\s*$", line):
                html_block = None
            continue
        html_match = re.match(r"<(figure|table|div|script|style)\b", line)
        if html_match:
            flush()
            tag = html_match.group(1)
            if not re.search(rf"</{tag}>\s*$", line):
                html_block = tag
            continue

        if not line:
            flush()
            continue
        if line.startswith("#") or re.match(r"^[-*_]{3,}$", line):
            flush()
            continue
        if line.startswith(">"):
            flush()
            quote = plain_text(line.lstrip("> "))
            if quote:
                quotes.append(quote)
                visible_chunks.append(quote)
            continue
        if line.startswith("|"):
            flush()
            if not re.match(r"^\|?\s*:?-{3,}", line):
                chunk = plain_text(line.replace("|", " "))
                if chunk:
                    visible_chunks.append(chunk)
            continue
        if re.match(r"^[-*+]\s+", line) or re.match(r"^\d+[.)]\s+", line):
            flush()
            chunk = plain_text(re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", line))
            if chunk:
                visible_chunks.append(chunk)
            continue

        buffer.append(line)

    flush()
    return paragraphs, quotes, visible_chunks


def check_article(filepath: Path) -> tuple[list[str], dict[str, int]]:
    paragraphs, quotes, visible_chunks = extract_article(
        filepath.read_text(encoding="utf-8")
    )
    article_text = " ".join(visible_chunks)
    compact_text = re.sub(r"\s+", "", article_text)
    sentences = sentence_split(article_text)
    issues: list[str] = []

    if len(compact_text) < MIN_ARTICLE_CHARS:
        issues.append(f"全文过短({len(compact_text)}字，至少{MIN_ARTICLE_CHARS}字)")
    if len(compact_text) > MAX_ARTICLE_CHARS:
        issues.append(f"全文过长({len(compact_text)}字，最多{MAX_ARTICLE_CHARS}字)")
    if len(paragraphs) < MIN_PARAGRAPHS:
        issues.append(f"正文段落不足({len(paragraphs)}段)")
    if len(sentences) < MIN_SENTENCES:
        issues.append(f"全文句数不足({len(sentences)}句)")

    long_paragraphs = [
        (index, len(re.sub(r"\s+", "", paragraph)))
        for index, paragraph in enumerate(paragraphs, start=1)
        if len(re.sub(r"\s+", "", paragraph)) > MAX_PARAGRAPH_CHARS
    ]
    if long_paragraphs:
        issues.append(f"段落过长{long_paragraphs}")

    valid_quotes = [
        quote
        for quote in quotes
        if MIN_QUOTE_CHARS <= len(re.sub(r"\s+", "", quote)) <= MAX_QUOTE_CHARS
    ]
    if not valid_quotes:
        issues.append(
            f"缺少{MIN_QUOTE_CHARS}–{MAX_QUOTE_CHARS}字的可转发核心金句"
        )

    duplicate_pairs = repetition_check(sentences)
    if duplicate_pairs:
        issues.append(f"疑似重复句{duplicate_pairs}")
    if not has_concrete_content(article_text):
        issues.append("缺少数字或具体例子")

    metrics = {
        "chars": len(compact_text),
        "paragraphs": len(paragraphs),
        "sentences": len(sentences),
        "quotes": len(valid_quotes),
    }
    return issues, metrics


def article_paths(targets: list[str]) -> list[Path]:
    paths: set[Path] = set()
    for target in targets:
        path = Path(target)
        if path.is_dir():
            paths.update(path.glob("*.md"))
        elif path.is_file():
            paths.add(path)
        else:
            raise FileNotFoundError(f"找不到文件或目录：{path}")
    return sorted(paths)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", nargs="+", help="Markdown article file or directory")
    args = parser.parse_args()

    try:
        paths = article_paths(args.targets)
    except FileNotFoundError as error:
        print(f"✗ {error}")
        return 2

    failed_articles = 0
    for path in paths:
        issues, metrics = check_article(path)
        summary = (
            f"{metrics['chars']}字，{metrics['paragraphs']}段，"
            f"{metrics['sentences']}句，{metrics['quotes']}条金句"
        )
        if not issues:
            print(f"✓ {path} 文章达标（{summary}）")
            continue
        failed_articles += 1
        print(f"✗ {path} 未达标（{summary}）：{', '.join(issues)}")

    print(
        f"汇总：检查 {len(paths)} 篇，"
        f"{len(paths) - failed_articles} 篇通过，{failed_articles} 篇未通过"
    )
    return 1 if failed_articles else 0


if __name__ == "__main__":
    sys.exit(main())
