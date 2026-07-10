#!/usr/bin/env python3
"""Verify Markdown blog paragraph length, sentence count, and basic density."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


MIN_CHARS = 500
MIN_SENTENCES = 4
CONCRETE_MARKERS = ("比如", "例如", "举个例子", "具体", "实际上")


def sentence_split(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"[。！？!?]", text) if part.strip()]


def repetition_check(sentences: list[str]) -> list[tuple[int, int, float]]:
    """Flag sentence pairs with unusually high character-set overlap."""
    suspicious_pairs: list[tuple[int, int, float]] = []
    for i, first in enumerate(sentences):
        for j in range(i + 1, len(sentences)):
            second = sentences[j]
            first_chars = set(first)
            second_chars = set(second)
            if not first_chars or not second_chars:
                continue
            overlap = len(first_chars & second_chars) / max(
                len(first_chars), len(second_chars)
            )
            if overlap > 0.6 and len(first) > 8 and len(second) > 8:
                suspicious_pairs.append((i + 1, j + 1, round(overlap, 2)))
    return suspicious_pairs


def has_concrete_content(text: str) -> bool:
    has_number = bool(re.search(r"\d", text))
    has_percent = "%" in text or "％" in text
    has_marker = any(marker in text for marker in CONCRETE_MARKERS)
    return has_number or has_percent or has_marker


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


def extract_body_paragraphs(content: str) -> list[str]:
    """Extract prose paragraphs while excluding Markdown structure and HTML blocks."""
    content = strip_frontmatter(content)
    paragraphs: list[str] = []
    buffer: list[str] = []
    in_fence = False
    in_comment = False
    html_block: str | None = None

    def flush() -> None:
        if buffer:
            paragraph = plain_text(" ".join(buffer))
            if paragraph:
                paragraphs.append(paragraph)
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

        is_structure = (
            not line
            or line.startswith("#")
            or line.startswith("|")
            or re.match(r"^[-*+]\s+", line) is not None
            or re.match(r"^\d+[.)]\s+", line) is not None
            or line.startswith(">")
            or re.match(r"^[-*_]{3,}$", line) is not None
        )
        if is_structure:
            flush()
            continue

        buffer.append(line)

    flush()
    return paragraphs


def check_article(filepath: Path) -> list[dict[str, object]]:
    content = filepath.read_text(encoding="utf-8")
    failures: list[dict[str, object]] = []
    for index, paragraph in enumerate(extract_body_paragraphs(content), start=1):
        char_count = len(paragraph)
        sentences = sentence_split(paragraph)
        issues: list[str] = []
        if char_count < MIN_CHARS:
            issues.append(f"字数不足({char_count}字)")
        if len(sentences) < MIN_SENTENCES:
            issues.append(f"句数不足({len(sentences)}句)")
        duplicate_pairs = repetition_check(sentences)
        if duplicate_pairs:
            issues.append(f"疑似重复句{duplicate_pairs}")
        if not has_concrete_content(paragraph):
            issues.append("缺少具体数字/例子/场景词，疑似空话")
        if issues:
            failures.append(
                {
                    "index": index,
                    "issues": issues,
                    "preview": paragraph[:50],
                }
            )
    return failures


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
        failures = check_article(path)
        if not failures:
            print(f"✓ {path} 全部正文段落达标")
            continue
        failed_articles += 1
        print(f"✗ {path} 有 {len(failures)} 段不达标：")
        for failure in failures:
            issues = ", ".join(failure["issues"])
            print(
                f"  正文段落{failure['index']}: {issues} — "
                f"「{failure['preview']}...」"
            )

    print(f"汇总：检查 {len(paths)} 篇，{len(paths) - failed_articles} 篇通过，{failed_articles} 篇未通过")
    return 1 if failed_articles else 0


if __name__ == "__main__":
    sys.exit(main())
