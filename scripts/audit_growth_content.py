#!/usr/bin/env python3
"""Deterministic SEO/GEO checks and automatic growth-mode evaluation.

The audit intentionally scores only observable repository evidence. External
metrics stay unavailable unless growth-data/metrics.json supplies them.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "src/content/blog"
METRICS_PATH = ROOT / "growth-data/metrics.json"


def frontmatter_and_body(text: str) -> tuple[str, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", text, flags=re.S)
    if not match:
        return "", text
    return match.group(1), text[match.end() :]


def scalar(frontmatter: str, key: str) -> str:
    match = re.search(
        rf"(?m)^{re.escape(key)}:\s*[\"']?(.+?)[\"']?\s*$", frontmatter
    )
    return match.group(1).strip() if match else ""


def list_count(frontmatter: str, key: str, item_key: str) -> int:
    start = re.search(rf"(?m)^{re.escape(key)}:\s*$", frontmatter)
    if not start:
        return 0
    section = frontmatter[start.end() :]
    next_key = re.search(r"(?m)^[A-Za-z][A-Za-z0-9_-]*:\s*", section)
    if next_key:
        section = section[: next_key.start()]
    return len(re.findall(rf"(?m)^\s*-\s+{re.escape(item_key)}:\s*", section))


def inline_list(frontmatter: str, key: str) -> list[str]:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*\[(.*?)\]\s*$", frontmatter)
    if not match:
        return []
    return [item.strip().strip("\"'") for item in match.group(1).split(",") if item.strip()]


def add_check(
    checks: list[dict[str, Any]], name: str, points: int, passed: bool, evidence: str
) -> None:
    checks.append(
        {
            "check": name,
            "points": points if passed else 0,
            "possible": points,
            "passed": passed,
            "evidence": evidence,
        }
    )


def audit_article(path: Path, all_titles: dict[str, int]) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = frontmatter_and_body(text)
    title = scalar(frontmatter, "title")
    description = scalar(frontmatter, "description")
    author = scalar(frontmatter, "author")
    pub_date = scalar(frontmatter, "pubDate")
    updated_date = scalar(frontmatter, "updatedDate")
    slug = path.stem
    h2_count = len(re.findall(r"(?m)^##\s+", body))
    body_h1_count = len(re.findall(r"(?m)^#\s+", body))
    internal_links = len(re.findall(r"\]\(/blog(?:/|\))", body))
    external_links = len(re.findall(r"\]\(https://", body))
    tags = inline_list(frontmatter, "tags")
    faq_count = list_count(frontmatter, "faq", "question")
    body_chars = len(re.sub(r"\s+", "", body))
    tables = len(re.findall(r"(?m)^\|\s*:?-{3,}", body))
    numbers = len(re.findall(r"\d", body))

    seo: list[dict[str, Any]] = []
    add_check(seo, "unique title", 10, bool(title) and all_titles.get(title, 0) == 1, title)
    add_check(seo, "meta description", 10, 45 <= len(description) <= 180, f"{len(description)} chars")
    add_check(seo, "clean slug", 5, bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug)), slug)
    add_check(seo, "single rendered H1 contract", 10, body_h1_count == 0, f"body H1={body_h1_count}; layout H1=1")
    add_check(seo, "heading coverage", 10, h2_count >= 4, f"H2={h2_count}")
    add_check(seo, "substantive body", 10, body_chars >= 1200, f"non-space chars={body_chars}")
    primary_topic_aligned = bool(tags) and tags[0].lower() in title.lower() and tags[0].lower() in body.lower()
    add_check(seo, "primary topic alignment", 10, primary_topic_aligned, tags[0] if tags else "missing")
    add_check(seo, "internal links", 10, internal_links >= 2, str(internal_links))
    add_check(seo, "external references", 10, external_links >= 2, str(external_links))
    add_check(seo, "author and dates", 10, bool(author and pub_date and updated_date), f"author={bool(author)}, dates={bool(pub_date and updated_date)}")
    site_contract = all(
        (
            (ROOT / "public/robots.txt").exists(),
            (ROOT / "public/llms.txt").exists(),
            "BlogPosting" in (ROOT / "src/layouts/BlogPost.astro").read_text(encoding="utf-8"),
            "canonical" in (ROOT / "src/components/BaseHead.astro").read_text(encoding="utf-8"),
        )
    )
    add_check(seo, "canonical/schema/robots contract", 5, site_contract, "site templates and public files")

    geo: list[dict[str, Any]] = []
    first_section = body[:1500]
    add_check(geo, "answer-first summary", 15, "先给答案" in first_section, "answer heading in opening section")
    core_parts = all(marker in body for marker in ("Definition:", "Why:", "Example:"))
    add_check(geo, "core answer block", 15, core_parts, "Definition/Why/Example")
    add_check(geo, "entity definition", 10, "核心实体" in body, "visible entity relationship paragraph")
    add_check(geo, "FAQ coverage", 15, faq_count >= 2 and bool(scalar(frontmatter, "faqIntent")), f"FAQ={faq_count}")
    add_check(geo, "key facts and data points", 10, tables >= 1 and numbers >= 3, f"tables={tables}, numeric chars={numbers}")
    add_check(geo, "expert explanation", 10, "## 专家解释" in body, "visible attributed analysis")
    add_check(geo, "citable references", 10, external_links >= 2, str(external_links))
    add_check(geo, "trust and freshness", 5, bool(author and updated_date), f"author={author}, updated={updated_date}")
    schema_contract = "FAQPage" in (ROOT / "src/layouts/BlogPost.astro").read_text(encoding="utf-8")
    add_check(geo, "visible FAQ schema contract", 5, faq_count >= 2 and schema_contract, "frontmatter FAQ + layout schema")
    robots = (ROOT / "public/robots.txt").read_text(encoding="utf-8")
    machine_access = "Allow: /" in robots and (ROOT / "public/llms.txt").exists()
    add_check(geo, "AI access and llms.txt", 5, machine_access, "robots allow + llms.txt")

    return {
        "slug": slug,
        "title": title,
        "seo_score": sum(check["points"] for check in seo),
        "geo_score": sum(check["points"] for check in geo),
        "seo_checks": seo,
        "geo_checks": geo,
    }


def load_metrics() -> dict[str, Any]:
    if not METRICS_PATH.exists():
        return {}
    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))


def evaluate_mode(today: date) -> dict[str, Any]:
    posts = sorted(BLOG_DIR.glob("*.md"))
    dates: list[date] = []
    for path in posts:
        frontmatter, _ = frontmatter_and_body(path.read_text(encoding="utf-8"))
        value = scalar(frontmatter, "pubDate")
        try:
            dates.append(datetime.strptime(value[:10], "%Y-%m-%d").date())
        except (ValueError, TypeError):
            continue
    launch_date = min(dates) if dates else None
    site_age_days = (today - launch_date).days if launch_date else None
    metrics = load_metrics()

    expansion_checks = {
        "blog_count_below_300": len(posts) < 300,
        "site_age_below_90_days": site_age_days is None or site_age_days < 90,
        "gsc_keywords_below_500_or_unavailable": metrics.get("gsc_valid_keywords") is None
        or metrics.get("gsc_valid_keywords", 0) < 500,
        "ai_citations_insufficient_or_unavailable": metrics.get("ai_citations") is None
        or metrics.get("ai_citations", 0) < 1,
        "topic_clusters_incomplete_or_unavailable": metrics.get("topic_clusters_complete")
        is not True,
    }
    maintenance_checks = {
        "blog_count_at_least_300": len(posts) >= 300,
        "keyword_coverage_stable": metrics.get("keyword_coverage_stable") is True,
        "monthly_organic_traffic_growing": metrics.get("monthly_organic_traffic_growing")
        is True,
        "verified_ai_citations": metrics.get("ai_citations", 0) >= 1,
        "index_rate_above_80_percent": metrics.get("index_rate", 0) > 0.8,
    }
    mode = "Maintenance" if all(maintenance_checks.values()) else "Expansion"
    return {
        "mode": mode,
        "blog_count": len(posts),
        "launch_date": launch_date.isoformat() if launch_date else None,
        "site_age_days": site_age_days,
        "metrics_source": str(METRICS_PATH) if METRICS_PATH.exists() else "unavailable",
        "expansion_checks": expansion_checks,
        "maintenance_checks": maintenance_checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", help="Article files to score")
    parser.add_argument("--date", default=date.today().isoformat(), help="Evaluation date")
    parser.add_argument("--json", action="store_true", help="Print JSON")
    args = parser.parse_args()

    try:
        audit_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    except ValueError:
        print("--date must use YYYY-MM-DD", file=sys.stderr)
        return 2

    all_titles: dict[str, int] = {}
    for path in BLOG_DIR.glob("*.md"):
        frontmatter, _ = frontmatter_and_body(path.read_text(encoding="utf-8"))
        title = scalar(frontmatter, "title")
        all_titles[title] = all_titles.get(title, 0) + 1

    targets = [Path(item) for item in args.paths]
    results = [audit_article(path, all_titles) for path in targets]
    report = {"mode_evaluation": evaluate_mode(audit_date), "articles": results}
    report["average_seo_score"] = (
        round(sum(item["seo_score"] for item in results) / len(results), 1)
        if results
        else None
    )
    report["average_geo_score"] = (
        round(sum(item["geo_score"] for item in results) / len(results), 1)
        if results
        else None
    )

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        mode = report["mode_evaluation"]
        print(
            f"Mode: {mode['mode']} | Blogs: {mode['blog_count']} | "
            f"Site age: {mode['site_age_days']} days | Metrics: {mode['metrics_source']}"
        )
        for item in results:
            status = "PASS" if item["seo_score"] >= 80 and item["geo_score"] >= 80 else "FAIL"
            print(
                f"{status} {item['slug']}: SEO {item['seo_score']}/100, "
                f"GEO {item['geo_score']}/100"
            )
        if results:
            print(
                f"Average: SEO {report['average_seo_score']}, "
                f"GEO {report['average_geo_score']}"
            )

    failed = any(item["seo_score"] < 80 or item["geo_score"] < 80 for item in results)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
