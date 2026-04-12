#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from html import unescape
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

TODAY = datetime(2026, 4, 12)
START_6M = TODAY - timedelta(days=183)
START_3M = TODAY - timedelta(days=90)
OUT_BASENAME = "牛客近6个月AI应用开发面经汇总"
SEARCH_QUERIES = [
    "AI应用开发", "AI应用开发 面经", "AI应用开发 一面", "AI应用开发 二面", "AI应用开发 实习",
    "AI应用平台开发", "AI应用平台开发 面经",
    "AI应用服务端开发", "AI应用服务端开发 面经",
    "AI应用后端开发", "AI应用后端开发 面经",
    "AI应用前端开发",
    "AI应用工程师", "AI应用工程师 面经",
    "AI技能应用开发",
    "AI Agent开发", "AI Agent开发 面经", "AI Agent 应用开发", "AI Agent研发",
    "Agent开发", "Agent开发 面经",
    "智能体开发", "智能体开发 面经", "智能体应用开发",
    "智能体与大模型应用工程", "智能体与大模型应用工程 面经",
    "大模型应用开发", "大模型应用开发 面经", "大模型应用开发 一面", "大模型应用开发 二面",
    "大模型应用工程", "大模型应用工程师", "大模型数据应用开发", "大模型数据应用开发 面经",
    "大模型开发", "大模型应用",
]
ROLE_KEYWORDS = [
    "ai应用开发", "ai应用平台开发", "ai应用服务端开发", "ai应用后端开发", "ai应用前端开发",
    "ai应用工程", "ai技能应用开发", "ai agent开发", "ai agent研发", "agent应用开发", "agent开发",
    "智能体开发", "智能体应用开发", "智能体与大模型应用工程", "大模型应用开发", "大模型应用工程",
    "大模型应用工程师", "大模型数据应用开发", "大模型开发", "ai应用", "agent岗", "agent研发",
]
INTERVIEW_POSITIVE = [
    "面经", "一面", "二面", "三面", "四面", "hr面", "终面", "凉经", "挂经", "过经", "oc", "offer",
    "面试问题", "面试记录", "面试分享", "面试", "答题思路",
]
INTERVIEW_NEGATIVE = [
    "求面经", "求助", "求指导", "要不要", "行么", "何去何从", "如何快速入门", "后端还是", "走传统",
    "该不该", "建议", "爆发", "路线", "offer，要接吗", "爆发，作为后端开发要不要", "何去何从", "现在走",
]
COMPANY_PATTERNS = [
    "阿里国际", "阿里云", "阿里灵犀互娱", "阿里淘天", "淘天", "蚂蚁", "腾讯", "字节", "剪映", "快手", "高德", "金山云",
    "蔚来", "小红书", "京东", "百度", "米哈游", "美团", "拼多多", "吉利科技", "第四范式", "OPPO", "XTransfer", "北汽", "某中厂", "某教育",
    "滴滴", "小厂", "T厂", "大厂", "教育", "阿里", "金山", "快手电商",
]

EXACT_TITLE_QUERIES = [
    "小红书 AI Agent开发 一面",
    "米哈游-AI Agent研发-暑期一面",
    "百度ai agent开发春招一面",
    "字节agent开发实习一面凉经",
    "快手AI Agent开发一面（已过）",
    "4.9-淘天agent-二面",
    "腾讯暑期实习 ai agent开发一面",
    "实习-快手电商-大模型数据应用开发一面",
    "字节暑期后端agent开发一面",
    "快手大模型应用开发算法岗三面面经",
    "拼多多大模型应用开发一面凉经",
    "腾讯 大模型应用开发 二面",
    "腾讯 大模型应用开发 一面",
    "大模型应用开发一面-美团面经",
    "OPPO大模型应用开发一面 攒人品",
    "字节 大模型应用开发 二面 日常实习",
    "字节大模型应用开发 日常实习一面",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.nowcoder.com/",
}


@dataclass
class Candidate:
    url: str
    source_type: str
    matched_queries: list[str]


class NowcoderCollector:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def get(self, url: str) -> str:
        for attempt in range(3):
            try:
                resp = self.session.get(url, timeout=30)
                resp.raise_for_status()
                return resp.text
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(0.6 * (attempt + 1))
        raise RuntimeError("unreachable")

    def search_candidates(self) -> list[Candidate]:
        hit_map: dict[str, set[str]] = defaultdict(set)
        source_type: dict[str, str] = {}
        for query in list(dict.fromkeys(SEARCH_QUERIES + EXACT_TITLE_QUERIES)):
            html = self.get(f"https://www.nowcoder.com/search?query={quote(query)}&type=post")
            soup = BeautifulSoup(html, "lxml")
            for a in soup.find_all("a", href=True):
                href = a["href"].split("?")[0]
                if href.startswith("/"):
                    href = "https://www.nowcoder.com" + href
                if "/feed/main/detail/" in href:
                    hit_map[href].add(query)
                    source_type[href] = "feed"
                elif "/discuss/" in href:
                    hit_map[href].add(query)
                    source_type[href] = "discuss"
        items = [
            Candidate(url=url, source_type=source_type[url], matched_queries=sorted(hit_map[url]))
            for url in sorted(hit_map)
        ]
        return items

    def _extract_state(self, html: str) -> dict[str, Any]:
        marker = "window.__INITIAL_STATE__="
        start = html.find(marker)
        if start == -1:
            raise RuntimeError("window.__INITIAL_STATE__ not found")
        start += len(marker)
        end = html.find("};(function(){var s;", start)
        if end == -1:
            end = html.find("</script>", start)
            if end == -1:
                raise RuntimeError("script end not found")
            raw = html[start:end]
        else:
            raw = html[start : end + 1]
        return json.loads(raw)

    def _normalize_content(self, raw: str) -> str:
        if not raw:
            return ""
        if "<" in raw and ">" in raw:
            soup = BeautifulSoup(raw, "lxml")
            text = soup.get_text("\n", strip=True)
        else:
            text = raw
        text = unescape(text)
        text = text.replace("\xa0", " ")
        text = re.sub(r"\r", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _extract_questions(self, text: str) -> list[str]:
        if not text:
            return []
        normalized = text.replace("：", ":").replace("．", ".")
        normalized = re.sub(r"(?<!\n)(\d{1,2}[\.、])", r"\n\1", normalized)
        normalized = re.sub(r"(?<!\n)([（(]?[一二三四五六七八九十]+[）)])", r"\n\1", normalized)
        lines = []
        for raw_line in normalized.splitlines():
            line = re.sub(r"\s+", " ", raw_line).strip(" -•\t")
            if not line:
                continue
            is_questionish = (
                re.match(r"^\d{1,2}[\.、]", line)
                or re.match(r"^[（(]?[一二三四五六七八九十]+[）)]", line)
                or "?" in line or "？" in line
                or line.startswith("算法") or line.startswith("手撕") or line.startswith("场景题")
            )
            bad_numeric = re.fullmatch(r"[0-9.\-,:/ ]+", line or "") is not None
            bad_date_like = re.search(r"20\d{2}[.-]\d{1,2}[.-]\d{1,2}", line or "") is not None
            useful_text = re.search(r"[一-鿿A-Za-z]", line or "") is not None
            if is_questionish and len(line) <= 180 and useful_text and not bad_numeric and not bad_date_like:
                lines.append(line)
        dedup: list[str] = []
        seen: set[str] = set()
        for line in lines:
            key = re.sub(r"\W+", "", line)
            if key and key not in seen:
                seen.add(key)
                dedup.append(line)
        if len(dedup) < 3:
            fallback_stop = ("不知道", "感觉", "有大佬", "鼠鼠", "目前", "优点", "缺点", "现在是", "想问", "请问", "求问", "反问")
            for raw_line in text.splitlines():
                line = re.sub(r"\s+", " ", raw_line).strip(" -•\t")
                if not line:
                    continue
                if len(line) < 2 or len(line) > 80:
                    continue
                if any(line.startswith(prefix) for prefix in fallback_stop):
                    continue
                if re.fullmatch(r"[0-9.\-,:/ ]+", line):
                    continue
                if not re.search(r"[\u4e00-\u9fffA-Za-z]", line):
                    continue
                if line.count("，") + line.count(",") > 3:
                    continue
                key = re.sub(r"\W+", "", line)
                if key and key not in seen:
                    seen.add(key)
                    dedup.append(line)
        return dedup[:30]

    def _infer_company(self, title: str, text: str) -> str:
        merged = f"{title} {text[:300]}"
        for company in COMPANY_PATTERNS:
            if company in merged:
                if company == "剪映" and "字节" in merged:
                    return "字节/剪映"
                if company == "快手电商":
                    return "快手电商"
                return company
        m = re.match(r"^([^\s\-—_]+)", title)
        return m.group(1) if m else "未知"

    def _infer_role(self, title: str, text: str) -> str:
        merged = f"{title} {text[:500]}".lower()
        for role in ROLE_KEYWORDS:
            if role in merged:
                return role
        return "未明确"

    def _infer_round(self, title: str, text: str) -> str:
        merged = f"{title} {text[:200]}"
        for k in ["一面", "二面", "三面", "四面", "hr面", "终面"]:
            if k in merged:
                return k
        return "未明确"

    def _is_actual_interview(self, title: str, text: str) -> tuple[bool, str]:
        merged = f"{title}\n{text}".lower()
        title_l = title.lower()
        preview_l = text[:600].lower()
        broad_role_mark = any(k in title_l for k in ["ai应用", "agent", "智能体", "大模型"])
        role_hit = any(k in title_l or k in preview_l for k in ROLE_KEYWORDS)
        if not (broad_role_mark and role_hit):
            return False, "标题/正文前段缺少岗位关键词"
        if any(k in title_l for k in [s.lower() for s in INTERVIEW_NEGATIVE]):
            return False, "明显是求助/讨论帖"
        if any(k in title_l for k in ["常见题", "合集", "全攻略", "总结版", "路线", "汇总"]):
            return False, "明显是汇总/攻略帖"
        if title_l.startswith("求") and "面经" in title_l:
            return False, "求面经帖"
        title_or_preview = f"{title_l}\n{preview_l[:200]}"
        if not any(k in title_or_preview for k in [s.lower() for s in INTERVIEW_POSITIVE]):
            return False, "缺少面试特征词"
        return True, ""

    def fetch_detail(self, candidate: Candidate) -> dict[str, Any]:
        html = self.get(candidate.url)
        state = self._extract_state(html)
        content_data = state["prefetchData"]["2"]["ssrCommonData"]["contentData"]
        title = content_data.get("title", "")
        raw_content = content_data.get("content", "")
        text = self._normalize_content(raw_content)
        ts = content_data.get("createdAt") or content_data.get("createTime") or content_data.get("editTime")
        created_at = datetime.fromtimestamp(ts / 1000) if ts else None
        in_6m = bool(created_at and START_6M <= created_at <= TODAY + timedelta(days=1))
        in_3m = bool(created_at and START_3M <= created_at <= TODAY + timedelta(days=1))
        is_interview, exclude_reason = self._is_actual_interview(title, text)
        questions = self._extract_questions(text)
        title_has_interview = any(k in title.lower() for k in [s.lower() for s in INTERVIEW_POSITIVE])
        if is_interview and (not title_has_interview) and len(questions) < 3 and not re.search(r"(一面|二面|三面|hr面|终面|面试官)", text[:120], re.I):
            is_interview = False
            exclude_reason = "更像讨论/求助帖，非稳定面经"
        summary = "；".join(q[:50] for q in questions[:6]) if questions else re.sub(r"\s+", " ", text[:180])
        item = {
            "title": title,
            "url": candidate.url,
            "source_type": candidate.source_type,
            "matched_queries": candidate.matched_queries,
            "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S") if created_at else None,
            "created_date": created_at.strftime("%Y-%m-%d") if created_at else None,
            "within_last_6_months": in_6m,
            "within_last_3_months": in_3m,
            "company": self._infer_company(title, text),
            "role": self._infer_role(title, text),
            "round": self._infer_round(title, text),
            "is_actual_interview": is_interview,
            "exclude_reason": exclude_reason,
            "question_count": len(questions),
            "questions": questions,
            "summary": summary,
        }
        return item


def build_markdown(all_items: list[dict[str, Any]], kept_items: list[dict[str, Any]]) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    company_counter = Counter(item["company"] for item in kept_items)
    month_counter = Counter(item["created_date"][:7] for item in kept_items if item.get("created_date"))
    lines = [
        f"# {OUT_BASENAME}",
        "",
        f"- 生成时间：{generated_at}",
        f"- 统计窗口：{START_6M.strftime('%Y-%m-%d')} ～ {TODAY.strftime('%Y-%m-%d')}",
        f"- 搜索关键词数：{len(list(dict.fromkeys(SEARCH_QUERIES + EXACT_TITLE_QUERIES)))}",
        f"- 牛客搜索候选帖数（去重后）：{len(all_items)}",
        f"- 过滤后实际面经帖数：{len(kept_items)}",
        f"- 最近3个月面经帖数：{sum(1 for x in kept_items if x['within_last_3_months'])}",
        "",
        "> 说明：这里的“全量”指基于牛客站内搜索 + 多组岗位关键词扩展后，当前可检索到并落在近6个月窗口内的相关面经帖去重结果。",
        "",
        "## 搜索关键词",
        "",
        "- " + "、".join(list(dict.fromkeys(SEARCH_QUERIES + EXACT_TITLE_QUERIES))),
        "",
        "## 公司分布",
        "",
    ]
    for company, count in company_counter.most_common():
        lines.append(f"- {company}: {count}")
    lines += ["", "## 月份分布", ""]
    for month, count in sorted(month_counter.items(), reverse=True):
        lines.append(f"- {month}: {count}")
    lines += ["", "## 总表", "", "| 日期 | 公司 | 岗位归类 | 轮次 | 标题 | 链接 | 提取题目数 |", "|---|---|---|---|---|---|---:|"]
    for item in kept_items:
        lines.append(
            f"| {item['created_date']} | {item['company']} | {item['role']} | {item['round']} | {item['title'].replace('|','/')} | [原帖]({item['url']}) | {item['question_count']} |"
        )
    lines += ["", "## 逐条整理", ""]
    for item in kept_items:
        lines += [
            f"### {item['created_date']}｜{item['title']}",
            "",
            f"- 公司：{item['company']}",
            f"- 岗位归类：{item['role']}",
            f"- 轮次：{item['round']}",
            f"- 来源：{item['url']}",
            f"- 命中搜索词：{'、'.join(item['matched_queries'])}",
            f"- 提炼摘要：{item['summary']}",
            "- 提取到的面试题/考点：",
        ]
        if item["questions"]:
            for q in item["questions"]:
                lines.append(f"  - {q}")
        else:
            lines.append("  - （未稳定提取出题目，建议回原帖查看）")
        lines.append("")
    lines += ["## 排除项", ""]
    excluded = [x for x in all_items if not x["is_actual_interview"] or not x["within_last_6_months"]]
    for item in excluded:
        reason = item["exclude_reason"] or ("超出时间窗口" if not item["within_last_6_months"] else "其他")
        lines.append(f"- {item['created_date']}｜{item['title']}｜{reason}｜{item['url']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    collector = NowcoderCollector()
    candidates = collector.search_candidates()
    all_items: list[dict[str, Any]] = []
    for idx, candidate in enumerate(candidates, start=1):
        try:
            item = collector.fetch_detail(candidate)
            all_items.append(item)
        except Exception as exc:
            all_items.append(
                {
                    "title": candidate.url.rsplit("/", 1)[-1],
                    "url": candidate.url,
                    "source_type": candidate.source_type,
                    "matched_queries": candidate.matched_queries,
                    "created_at": None,
                    "created_date": None,
                    "within_last_6_months": False,
                    "within_last_3_months": False,
                    "company": "未知",
                    "role": "未明确",
                    "round": "未明确",
                    "is_actual_interview": False,
                    "exclude_reason": f"抓取失败: {exc}",
                    "question_count": 0,
                    "questions": [],
                    "summary": "",
                }
            )
        time.sleep(0.12)
    kept_items = [
        x for x in all_items
        if x["within_last_6_months"] and x["is_actual_interview"]
    ]
    kept_items.sort(key=lambda x: (x["created_at"] or "", x["title"]), reverse=True)
    all_items.sort(key=lambda x: (x["created_at"] or "", x["title"]), reverse=True)

    base = Path(OUT_BASENAME)
    base_json = base.with_suffix(".json")
    base_md = base.with_suffix(".md")
    base_json.write_text(json.dumps({
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "window": {"start_6m": START_6M.strftime("%Y-%m-%d"), "start_3m": START_3M.strftime("%Y-%m-%d"), "today": TODAY.strftime("%Y-%m-%d")},
        "queries": SEARCH_QUERIES,
        "all_items": all_items,
        "kept_items": kept_items,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    base_md.write_text(build_markdown(all_items, kept_items), encoding="utf-8")

    print(f"candidates={len(candidates)}")
    print(f"kept={len(kept_items)}")
    print(f"json={base_json}")
    print(f"md={base_md}")


if __name__ == "__main__":
    main()
