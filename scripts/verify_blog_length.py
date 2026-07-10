#!/usr/bin/env python3
"""Verify Markdown blog depth, structure, density, and obvious manual-style prose."""

from __future__ import annotations

import argparse
from collections import Counter
import re
import sys
from pathlib import Path


MIN_CHARS = 400
MIN_SENTENCES = 4
CONCRETE_MARKERS = ("比如", "例如", "举个例子", "具体", "实际上")
FAQ_HEADINGS = ("FAQ", "常见问题")
ACTION_HEADING_MARKERS = (
    "行动建议",
    "行动清单",
    "检查清单",
    "调整建议",
    "下一步",
    "必须完成",
    "可以怎么做",
    "上线前",
    "发布前",
    "决定前",
)
GENERIC_ENDING_HEADINGS = ("结语", "总结", "写在最后", "最后", "最后的话")


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


def manual_tone_check(text: str) -> bool:
    """Flag paragraphs that stack three or more parallel classification phrases."""
    parallel_patterns = len(
        re.findall(r"第[一二三四五]\w{0,3}是|[A-Z]是[^，。]{2,10}，[A-Z]是", text)
    )
    return parallel_patterns >= 3


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
    """Extract prose paragraphs, excluding lists, tables, quotes, and the FAQ module."""
    content = strip_frontmatter(content)
    paragraphs: list[str] = []
    buffer: list[str] = []
    in_fence = False
    in_comment = False
    html_block: str | None = None
    in_faq = False

    def flush() -> None:
        if buffer:
            paragraph = plain_text(" ".join(buffer))
            if paragraph:
                paragraphs.append(paragraph)
            buffer.clear()

    for raw_line in content.splitlines():
        line = raw_line.strip()

        h2_match = re.match(r"^##\s+(.+)$", line)
        if h2_match:
            flush()
            in_faq = h2_match.group(1).strip().upper() in FAQ_HEADINGS
            continue
        if in_faq:
            continue

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
        if manual_tone_check(paragraph):
            issues.append("疑似说明书腔，平行罗列句式过多，需要改写成推理叙述")
        if issues:
            failures.append(
                {
                    "index": index,
                    "issues": issues,
                    "preview": paragraph[:50],
                }
            )
    return failures


def tldr_text(content: str) -> str:
    content = strip_frontmatter(content)
    lines: list[str] = []
    collecting = False
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if line.startswith(">"):
            collecting = True
            lines.append(re.sub(r"^>\s?", "", line))
        elif collecting:
            break
    return plain_text(" ".join(lines))


def action_list_count(content: str) -> int:
    content = strip_frontmatter(content)
    faq_match = re.search(r"(?mi)^##\s+(?:FAQ|常见问题)\s*$", content)
    if faq_match:
        content = content[: faq_match.start()]
    groups: list[int] = []
    current = 0
    for line in content.splitlines():
        if re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)", line.strip()):
            current += 1
        elif line.strip() and current:
            groups.append(current)
            current = 0
    if current:
        groups.append(current)
    valid_groups = [count for count in groups if 3 <= count <= 5]
    if valid_groups:
        return max(valid_groups)
    return max(groups, default=0)


def faq_entries(content: str) -> list[tuple[str, str]]:
    content = strip_frontmatter(content)
    match = re.search(r"(?mi)^##\s+(?:FAQ|常见问题)\s*$", content)
    if not match:
        return []
    section = content[match.end() :]
    entries: list[tuple[str, str]] = []
    question_matches = list(re.finditer(r"(?m)^###\s+(.+?)\s*$", section))
    for index, question_match in enumerate(question_matches):
        answer_start = question_match.end()
        answer_end = (
            question_matches[index + 1].start()
            if index + 1 < len(question_matches)
            else len(section)
        )
        answer_block = section[answer_start:answer_end].strip()
        answer = plain_text(answer_block.split("\n\n", 1)[0])
        entries.append((question_match.group(1).strip(), answer))
    return entries


def h2_sections(content: str) -> list[tuple[str, str]]:
    content = strip_frontmatter(content)
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", content))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        sections.append((match.group(1).strip(), content[match.end() : end]))
    return sections


def check_structure(content: str) -> list[str]:
    issues: list[str] = []
    tldr = tldr_text(content)
    if not tldr or "TL;DR" not in tldr:
        issues.append("缺少 TL;DR 引用块")
    else:
        tldr_sentences = sentence_split(tldr.replace("TL;DR", ""))
        if not 2 <= len(tldr_sentences) <= 4:
            issues.append(f"TL;DR 应为2-4句(当前{len(tldr_sentences)}句)")

    entries = faq_entries(content)
    has_faq = re.search(r"(?mi)^##\s+(?:FAQ|常见问题)\s*$", strip_frontmatter(content)) is not None
    if has_faq:
        if len(entries) < 2:
            issues.append(f"已有 FAQ 但不足2个真实问句(当前{len(entries)}个)")
        for index, (question, answer) in enumerate(entries, start=1):
            if not question.endswith(("？", "?")):
                issues.append(f"FAQ问题{index}不是问句")
            answer_length = len(answer)
            if not 30 <= answer_length <= 60:
                issues.append(f"FAQ回答{index}应为30-60字(当前{answer_length}字)")

    for heading, section in h2_sections(content):
        if heading.upper() in FAQ_HEADINGS:
            continue
        if action_list_count(section) >= 3 and not extract_body_paragraphs(section):
            continue
        if any(marker in heading for marker in ACTION_HEADING_MARKERS) and action_list_count(section) >= 3:
            continue
        paragraphs = extract_body_paragraphs(section)
        if not paragraphs:
            issues.append(f"二级标题“{heading}”下缺少展开论述")

    sections = h2_sections(content)
    if sections:
        final_heading, final_section = sections[-1]
        if final_heading.upper() in FAQ_HEADINGS or any(
            marker in final_heading for marker in ACTION_HEADING_MARKERS
        ):
            issues.append("文章不能以 FAQ 或行动清单匆匆结束，需要补一个回扣核心观点的自然收尾")
        if final_heading.strip() in GENERIC_ENDING_HEADINGS:
            issues.append(f"结尾标题“{final_heading}”过于模板化，需要改成与本文观点直接相关的标题")
        if not extract_body_paragraphs(final_section):
            issues.append("最后一个二级标题下需要有完整的收尾论述")
    return issues


def article_paths(targets: list[str]) -> list[Path]:
    paths: set[Path] = set()
    for target in targets:
        path = Path(target)
        if path.is_dir():
            paths.update(path.rglob("*.md"))
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
    final_heading_counts: Counter[str] = Counter()
    for path in paths:
        content = path.read_text(encoding="utf-8")
        sections = h2_sections(content)
        if sections:
            final_heading_counts[sections[-1][0]] += 1
        failures = check_article(path)
        structure_issues = check_structure(content)
        if not failures and not structure_issues:
            print(f"✓ {path} 全部正文段落达标")
            continue
        failed_articles += 1
        print(
            f"✗ {path} 有 {len(failures)} 段不达标、"
            f"{len(structure_issues)} 项结构问题："
        )
        for failure in failures:
            issues = ", ".join(failure["issues"])
            print(
                f"  正文段落{failure['index']}: {issues} — "
                f"「{failure['preview']}...」"
            )
        for issue in structure_issues:
            print(f"  结构: {issue}")

    repeated_endings = {
        heading: count for heading, count in final_heading_counts.items() if count >= 4
    }
    if repeated_endings:
        print("✗ 全库结尾标题重复过多，疑似再次套用统一收尾模板：")
        for heading, count in sorted(repeated_endings.items(), key=lambda item: (-item[1], item[0])):
            print(f"  {count} 篇使用“{heading}”")

    print(f"汇总：检查 {len(paths)} 篇，{len(paths) - failed_articles} 篇通过，{failed_articles} 篇未通过")
    return 1 if failed_articles or repeated_endings else 0


if __name__ == "__main__":
    sys.exit(main())
