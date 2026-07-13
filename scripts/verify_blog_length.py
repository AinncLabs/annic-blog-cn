#!/usr/bin/env python3
"""Verify blog depth and endings without forcing every article into one template."""

from __future__ import annotations

import argparse
from collections import Counter
import re
import sys
from pathlib import Path
from typing import TextIO


MIN_PARAGRAPH_CHARS = 400
MIN_SENTENCES = 4
MAX_FAQ_SHARE = 0.15
VALID_CONTENT_TYPES = {"guide", "comparison", "analysis", "opinion"}
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


class Tee:
    """Write verifier output to the terminal and an optional audit report."""

    def __init__(self, *streams: TextIO) -> None:
        self.streams = streams

    def write(self, data: str) -> int:
        for stream in self.streams:
            stream.write(data)
        return len(data)

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()


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


def frontmatter_text(content: str) -> str:
    if not content.startswith("---"):
        return ""
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", content, flags=re.S)
    return match.group(1) if match else ""


def frontmatter_value(content: str, key: str) -> str:
    match = re.search(
        rf'(?m)^{re.escape(key)}:\s*["\']?(.+?)["\']?\s*$',
        frontmatter_text(content),
    )
    return match.group(1).strip() if match else ""


def frontmatter_faq_count(content: str) -> int:
    frontmatter = frontmatter_text(content)
    match = re.search(r"(?m)^faq:\s*$", frontmatter)
    if not match:
        return 0
    section = frontmatter[match.end() :]
    next_key = re.search(r"(?m)^[A-Za-z][A-Za-z0-9_-]*:\s*", section)
    if next_key:
        section = section[: next_key.start()]
    return len(re.findall(r"(?m)^\s*-\s+question:\s*", section))


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
        if char_count < MIN_PARAGRAPH_CHARS:
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


def final_block_type(content: str) -> str:
    """Return the final meaningful Markdown block type for ending validation."""
    lines = [line.strip() for line in strip_frontmatter(content).splitlines()]
    lines = [line for line in lines if line and not line.startswith("<!--")]
    if not lines:
        return "empty"
    last = lines[-1]
    if last.startswith(">"):
        return "quote"
    if re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)", last):
        return "list"
    if last.startswith("|"):
        return "table"
    if last.startswith("```"):
        return "code"
    if re.match(r"</(?:figure|table|div)>$", last):
        return "visual"
    if last.startswith("#"):
        return "heading"
    return "prose"


def structure_fingerprint(content: str) -> str:
    """Describe an article's block skeleton while ignoring its actual wording."""
    lines = strip_frontmatter(content).splitlines()
    tokens: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue

        if line.startswith("```"):
            tokens.append("代码")
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                index += 1
            index += 1
            continue

        if line.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines):
                quote_line = lines[index].strip()
                if quote_line.startswith(">"):
                    quote_lines.append(quote_line)
                    index += 1
                    continue
                if not quote_line:
                    index += 1
                    continue
                break
            tokens.append("TLDR" if "TL;DR" in " ".join(quote_lines) else "引用")
            continue

        h2_match = re.match(r"^##\s+(.+)$", line)
        if h2_match:
            heading = h2_match.group(1).strip()
            tokens.append("FAQ" if heading.upper() in FAQ_HEADINGS else "二级标题")
            index += 1
            continue
        if line.startswith("### "):
            tokens.append("三级标题")
            index += 1
            continue
        if line.startswith("#"):
            tokens.append("标题")
            index += 1
            continue

        if line.startswith("|"):
            tokens.append("表格")
            while index < len(lines) and lines[index].strip().startswith("|"):
                index += 1
            continue

        if re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)", line):
            tokens.append("清单")
            while index < len(lines):
                item = lines[index].strip()
                if re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)", item) or not item:
                    index += 1
                    continue
                break
            continue

        html_match = re.match(r"<(figure|table|div)\b", line)
        if html_match:
            tag = html_match.group(1)
            tokens.append("可视化")
            index += 1
            while index < len(lines) and f"</{tag}>" not in lines[index]:
                index += 1
            index += 1
            continue

        tokens.append("正文")
        index += 1
        while index < len(lines):
            next_line = lines[index].strip()
            if not next_line:
                break
            if re.match(
                r"^(?:>|#{1,6}\s|```|\||[-*+]\s+|\d+[.)]\s+|<(?:figure|table|div)\b)",
                next_line,
            ):
                break
            index += 1

    return " → ".join(tokens)


def publication_date(content: str) -> str:
    match = re.search(r'(?m)^pubDate:\s*["\']?([^"\'\s]+)', content)
    return match.group(1) if match else "0000-00-00"


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


def has_structured_aid(content: str) -> bool:
    body = strip_frontmatter(content)
    has_table = re.search(r"(?m)^\|\s*:?-{3,}", body) is not None
    has_code = re.search(r"(?m)^```", body) is not None
    has_visual = re.search(r"(?m)^<(?:figure|table)\b", body) is not None
    has_action_list = action_list_count(body) >= 3
    return has_table or has_code or has_visual or has_action_list


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
    content_type = frontmatter_value(content, "contentType")
    if content_type not in VALID_CONTENT_TYPES:
        issues.append("frontmatter 缺少有效 contentType；必须是 guide、comparison、analysis 或 opinion")

    tldr = tldr_text(content)
    if "TL;DR" not in tldr:
        issues.append("缺少放在正文开头的 TL;DR 引用块")
    else:
        tldr_sentences = sentence_split(tldr.replace("TL;DR", ""))
        if not 2 <= len(tldr_sentences) <= 4:
            issues.append(f"TL;DR 应为2-4句(当前{len(tldr_sentences)}句)")

    entries = faq_entries(content)
    has_markdown_faq = re.search(r"(?mi)^##\s+(?:FAQ|常见问题)\s*$", strip_frontmatter(content)) is not None
    frontmatter_faq_items = frontmatter_faq_count(content)
    has_faq = has_markdown_faq or frontmatter_faq_items > 0
    faq_intent = frontmatter_value(content, "faqIntent")
    if has_faq and len(faq_intent) < 12:
        issues.append("FAQ 缺少 faqIntent 保留理由；只有真实搜索问题或关键边界补充才允许保留")
    if faq_intent and not has_faq:
        issues.append("存在 faqIntent 但文章没有 FAQ，请删除失效的保留理由")
    if has_markdown_faq:
        if len(entries) < 2:
            issues.append(f"已有 FAQ 但不足2个真实问句(当前{len(entries)}个)")
        for index, (question, answer) in enumerate(entries, start=1):
            if not question.endswith(("？", "?")):
                issues.append(f"FAQ问题{index}不是问句")
            answer_length = len(answer)
            if not 30 <= answer_length <= 60:
                issues.append(f"FAQ回答{index}应为30-60字(当前{answer_length}字)")
    if frontmatter_faq_items and frontmatter_faq_items < 2:
        issues.append(f"frontmatter FAQ 不足2个真实问句(当前{frontmatter_faq_items}个)")

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

    body_paragraphs = extract_body_paragraphs(content)
    if not body_paragraphs:
        issues.append("文章缺少完整正文论述")

    if re.search(r"(?m)^## 核心判断与执行背景$", strip_frontmatter(content)):
        issues.append("仍在使用通用标题“核心判断与执行背景”，需要改成本文专属标题")
    if re.search(r"(?m)^### 对照表、清单与执行参考$", strip_frontmatter(content)):
        issues.append("仍在使用通用模块标题，需要说明这张表或清单具体解决什么问题")
    boilerplate_phrases = (
        "真正需要改变的不是再加一条规则",
        "工具只有在减少重复确认、保留操作记录并帮助团队判断下一步时",
        "可以马上做的三个调整",
        "判断一个功能有没有用，看它能不能减少下一次沟通",
        "下一批任务前要留下三类结论",
    )
    for phrase in boilerplate_phrases:
        if phrase in content:
            issues.append(f"仍含批量模板句“{phrase}”，需要改成本文独有的判断")

    ending_type = final_block_type(content)
    if ending_type != "prose":
        issues.append(
            f"文章最后一个内容块是{ending_type}，需要用自然段完成真正收尾"
        )

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
    parser.add_argument("--report", help="Also save the raw verifier output to this file")
    args = parser.parse_args()

    try:
        paths = article_paths(args.targets)
    except FileNotFoundError as error:
        print(f"✗ {error}")
        return 2

    original_stdout = sys.stdout
    report_handle: TextIO | None = None
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_handle = report_path.open("w", encoding="utf-8")
        sys.stdout = Tee(original_stdout, report_handle)

    failed_articles = 0
    final_heading_counts: Counter[str] = Counter()
    fingerprint_counts: Counter[str] = Counter()
    dated_fingerprints: list[tuple[str, Path, str]] = []
    faq_article_paths: list[Path] = []
    for path in paths:
        content = path.read_text(encoding="utf-8")
        if faq_entries(content) or frontmatter_faq_count(content):
            faq_article_paths.append(path)
        fingerprint = structure_fingerprint(content)
        fingerprint_counts[fingerprint] += 1
        dated_fingerprints.append((publication_date(content), path, fingerprint))
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

    overused_structures = {
        fingerprint: count
        for fingerprint, count in fingerprint_counts.items()
        if count >= 7
    }
    if overused_structures:
        print("✗ 同一文章骨架使用过多，结构已经覆盖了内容差异：")
        for fingerprint, count in sorted(
            overused_structures.items(), key=lambda item: (-item[1], item[0])
        ):
            print(f"  {count} 篇使用：{fingerprint}")

    consecutive_templates: list[tuple[list[Path], str]] = []
    dated_fingerprints.sort(key=lambda item: (item[0], item[1].name), reverse=True)
    for start in range(len(dated_fingerprints) - 4):
        window = dated_fingerprints[start : start + 5]
        if len({item[2] for item in window}) == 1:
            consecutive_templates.append(([item[1] for item in window], window[0][2]))
    if consecutive_templates:
        print("✗ 按发布日期相邻的5篇文章使用同一骨架：")
        for window, fingerprint in consecutive_templates:
            print(f"  {', '.join(path.name for path in window)}")
            print(f"  骨架：{fingerprint}")

    faq_limit = max(2, int(len(paths) * MAX_FAQ_SHARE))
    faq_overuse = len(faq_article_paths) > faq_limit
    if faq_overuse:
        print(
            f"✗ FAQ 使用过多：{len(faq_article_paths)}/{len(paths)} 篇，"
            f"当前上限为 {faq_limit} 篇（{MAX_FAQ_SHARE:.0%}）"
        )
        print("  FAQ 只能用于真实搜索意图或正文难以自然展开的关键边界，不能作为文章默认模块。")

    print(f"汇总：检查 {len(paths)} 篇，{len(paths) - failed_articles} 篇通过，{failed_articles} 篇未通过")
    exit_code = 1 if failed_articles or repeated_endings or overused_structures or consecutive_templates or faq_overuse else 0
    if report_handle:
        sys.stdout.flush()
        sys.stdout = original_stdout
        report_handle.close()
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
