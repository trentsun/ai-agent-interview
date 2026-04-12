#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from jinja2 import Template
import markdown
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path('.')
SITE_DIR = ROOT / 'site'
ASSETS_DIR = SITE_DIR / 'assets'

SUMMARY_JSON = ROOT / '牛客近6个月AI应用开发面经汇总.json'
ANALYSIS_JSON = ROOT / '牛客近6个月AI应用开发面经-分析结果.json'
REPORT_FILES = [
    ROOT / '牛客近6个月AI应用开发面经汇总.md',
    ROOT / '牛客近6个月AI应用开发面经-知识点聚类.md',
    ROOT / '牛客近6个月AI应用开发面经-高频题题库与答案框架.md',
    ROOT / '牛客近6个月AI应用开发面经-公司维度对比分析.md',
]
PDF_PATH = SITE_DIR / '牛客近6个月AI应用开发面经仪表盘.pdf'
INDEX_PATH = SITE_DIR / 'index.html'

STYLE = r'''
:root {
  --bg: #0b1020;
  --panel: #121a31;
  --panel-2: #0f1730;
  --text: #eaf0ff;
  --muted: #9fb0d8;
  --primary: #6ea8fe;
  --border: rgba(255,255,255,0.12);
  --chip: rgba(110,168,254,0.12);
  --table-stripe: rgba(255,255,255,0.03);
  --shadow: 0 12px 36px rgba(0,0,0,0.28);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: Inter, -apple-system, BlinkMacSystemFont, 'SF Pro SC', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  color: var(--text);
  background: radial-gradient(circle at top left, rgba(110,168,254,0.14), transparent 28%), radial-gradient(circle at top right, rgba(139,92,246,0.15), transparent 24%), var(--bg);
}
a { color: #9ec5fe; text-decoration: none; }
a:hover { text-decoration: underline; }
.page {
  max-width: 1640px;
  margin: 0 auto;
  padding: 20px;
}
.layout {
  display: grid;
  grid-template-columns: 290px minmax(0, 1fr);
  gap: 20px;
  align-items: start;
}
.sidebar, .hero, .side-panel, .card, .report, .toolbar {
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)), var(--panel);
  border: 1px solid var(--border);
  border-radius: 20px;
  box-shadow: var(--shadow);
}
.sidebar {
  position: sticky;
  top: 18px;
  padding: 18px;
  max-height: calc(100vh - 36px);
  overflow: auto;
}
.sidebar h2 {
  margin: 0 0 8px;
  font-size: 20px;
}
.sidebar p {
  margin: 0 0 14px;
  font-size: 13px;
  color: var(--muted);
  line-height: 1.6;
}
.sidebar-group { margin-bottom: 18px; }
.sidebar-group h3 {
  margin: 0 0 10px;
  font-size: 13px;
  color: #c9d8ff;
  text-transform: uppercase;
  letter-spacing: .08em;
}
.sidebar-tree {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.sidebar-tree a {
  display: block;
  padding: 9px 12px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.06);
  background: rgba(255,255,255,0.03);
  color: var(--text);
  font-size: 13px;
  line-height: 1.45;
}
.sidebar-tree a:hover {
  background: rgba(110,168,254,0.12);
  border-color: rgba(110,168,254,0.28);
  text-decoration: none;
}
.main { min-width: 0; }
.header {
  display: grid;
  grid-template-columns: 2.1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}
.hero { padding: 30px; }
.hero h1 { margin: 0 0 10px; font-size: 38px; line-height: 1.18; }
.hero p { color: var(--muted); margin: 0 0 14px; font-size: 15px; }
.side-panel { padding: 22px; }
.meta-list { margin: 0; padding-left: 18px; color: var(--muted); }
.meta-list li { margin: 8px 0; }
.stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin: 18px 0 22px;
}
.card { padding: 18px; }
.card .label { color: var(--muted); font-size: 13px; }
.card .value { font-size: 30px; font-weight: 800; margin-top: 8px; }
.card .hint { color: var(--muted); font-size: 12px; margin-top: 8px; }
.chips { display: flex; flex-wrap: wrap; gap: 10px; }
.chip {
  padding: 8px 12px;
  border-radius: 999px;
  background: var(--chip);
  border: 1px solid rgba(110,168,254,0.28);
  color: #d9e7ff;
  font-size: 13px;
}
.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  padding: 16px 18px;
  margin-bottom: 20px;
  position: sticky;
  top: 12px;
  z-index: 8;
  backdrop-filter: blur(10px);
}
.toolbar-title {
  font-size: 14px;
  color: var(--muted);
}
.actions { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
.search-input {
  min-width: 320px;
  background: var(--panel-2);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 10px 12px;
  outline: none;
}
.button {
  display: inline-block;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid rgba(110,168,254,0.35);
  background: linear-gradient(180deg, rgba(110,168,254,0.2), rgba(110,168,254,0.08));
  color: white;
  font-weight: 600;
}
.grid-2 {
  display: grid;
  grid-template-columns: 1.2fr 0.95fr;
  gap: 20px;
  margin-bottom: 20px;
}
.knowledge-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}
.knowledge-card {
  display: block;
  padding: 18px;
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(110,168,254,0.10), rgba(255,255,255,0.02));
  border: 1px solid rgba(110,168,254,0.18);
}
.knowledge-card h3 { margin: 0 0 8px; font-size: 18px; color: var(--text); }
.knowledge-card p { margin: 0 0 10px; color: var(--muted); font-size: 13px; line-height: 1.6; }
.knowledge-card ul { margin: 0; padding-left: 18px; color: #dde7ff; }
.section-title { margin: 0 0 12px; font-size: 24px; }
.table-wrap { overflow: auto; }
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
th, td {
  padding: 12px 10px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  text-align: left;
  vertical-align: top;
}
tr:nth-child(even) td { background: var(--table-stripe); }
.report {
  padding: 28px;
  margin-bottom: 20px;
}
.report h1:first-child, .report h2:first-child { margin-top: 0; }
.report h1, .report h2, .report h3, .report h4 { scroll-margin-top: 90px; }
.report p, .report li { line-height: 1.72; color: #dde7ff; }
.report ul, .report ol { padding-left: 22px; }
.report code {
  background: rgba(255,255,255,0.08);
  padding: 2px 6px;
  border-radius: 6px;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}
.report pre {
  overflow: auto;
  padding: 14px;
  border-radius: 14px;
  background: #0a1124;
  border: 1px solid rgba(255,255,255,0.08);
}
.report blockquote {
  margin: 16px 0;
  padding: 4px 16px;
  border-left: 4px solid var(--primary);
  background: rgba(110,168,254,0.08);
  border-radius: 0 12px 12px 0;
}
.report hr {
  border: none;
  border-top: 1px solid rgba(255,255,255,0.08);
  margin: 24px 0;
}
.footer {
  color: var(--muted);
  text-align: center;
  padding: 30px 0 10px;
  font-size: 13px;
}
@media (max-width: 1180px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar {
    position: static;
    max-height: none;
  }
  .header, .grid-2, .knowledge-grid { grid-template-columns: 1fr; }
}
@media (max-width: 820px) {
  .page { padding: 14px; }
  .stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .toolbar { position: static; }
  .actions { width: 100%; }
  .search-input { min-width: 0; width: 100%; }
}
@media print {
  body { background: white; color: #111; }
  .page { max-width: none; padding: 0; }
  .sidebar, .toolbar, .footer { display: none !important; }
  .layout { display: block; }
  .hero, .side-panel, .card, .report { box-shadow: none; background: white; border-color: #ddd; color: #111; }
  .hero p, .side-panel, .label, .hint, .meta-list, .footer { color: #444; }
  .report p, .report li, .report a, .hero h1, .section-title { color: #111; }
  a { color: #111; text-decoration: none; }
}
'''

SCRIPT = r'''
(function () {
  const input = document.getElementById('search-input');
  const rows = Array.from(document.querySelectorAll('[data-search-row]'));
  if (!input) return;
  input.addEventListener('input', () => {
    const kw = input.value.trim().toLowerCase();
    rows.forEach((row) => {
      const text = (row.getAttribute('data-search-row') || '').toLowerCase();
      row.style.display = !kw || text.includes(kw) ? '' : 'none';
    });
  });
})();
'''

TEMPLATE = Template(r'''
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{{ title }}</title>
  <meta name="description" content="AI应用开发面经看板：汇总、知识点聚类、高频题题库、公司维度对比分析。" />
  <link rel="stylesheet" href="assets/styles.css" />
</head>
<body>
  <div class="page">
    <div class="layout">
      <aside class="sidebar">
        <h2>目录</h2>
        <p>左侧目录树固定，右侧内容区尽量铺满。你可以一直通过这里跳转，不用在长页面里来回滚动。</p>

        <div class="sidebar-group">
          <h3>核心导航</h3>
          <div class="sidebar-tree">
            <a href="#overview">总览</a>
            <a href="#knowledge-nav">知识点导航卡片</a>
            <a href="#themes">高频题型</a>
          </div>
        </div>

        <div class="sidebar-group">
          <h3>知识点目录</h3>
          <div class="sidebar-tree">
            {% for item in knowledge_nav %}
            <a href="#{{ item.anchor }}">{{ item.name }}</a>
            {% endfor %}
          </div>
        </div>

        <div class="sidebar-group">
          <h3>分析报告</h3>
          <div class="sidebar-tree">
            {% for section in sections %}
            <a href="#{{ section.anchor }}">{{ section.short_title }}</a>
            {% endfor %}
          </div>
        </div>

        <div class="sidebar-group">
          <h3>附录</h3>
          <div class="sidebar-tree">
            <a href="#latest">最新面经列表</a>
          </div>
        </div>
      </aside>

      <main class="main">
        <div class="header">
          <section class="hero">
            <h1>{{ title }}</h1>
            <p>{{ subtitle }}</p>
            <div class="stats">
              <div class="card"><div class="label">面经样本数</div><div class="value">{{ stats.interview_count }}</div><div class="hint">近 6 个月筛选后的有效面经</div></div>
              <div class="card"><div class="label">提取题目数</div><div class="value">{{ stats.question_count }}</div><div class="hint">来自全部面经的问题/考点</div></div>
              <div class="card"><div class="label">覆盖公司数</div><div class="value">{{ stats.company_count }}</div><div class="hint">字节 / 腾讯 / 淘天 / 快手 等</div></div>
              <div class="card"><div class="label">最后构建时间</div><div class="value" style="font-size:18px;line-height:1.45">{{ stats.generated_at }}</div><div class="hint">刷新命令：./refresh_interview_site.sh</div></div>
            </div>
            <div class="chips">
              {% for company, count in top_companies %}
              <span class="chip">{{ company }} · {{ count }}</span>
              {% endfor %}
            </div>
          </section>
          <aside class="side-panel">
            <h3 style="margin-top:0">使用方式</h3>
            <ul class="meta-list">
              <li>本地直接打开：<code>site/index.html</code></li>
              <li>本地启动服务：<code>./serve_interview_site.sh</code></li>
              <li>公网临时分享：<code>./public_interview_site.sh</code></li>
              <li>更新面经并重建网页：<code>./refresh_interview_site.sh</code></li>
              <li>PDF 导出：<code>{{ pdf_name }}</code></li>
            </ul>
            <h3>浏览建议</h3>
            <p style="color:var(--muted)">先看右侧总览和知识点导航，再从左侧目录树进入具体知识点。面经原始条目放在最下方附录区。</p>
          </aside>
        </div>

        <div class="toolbar">
          <div class="toolbar-title">左侧目录树负责导航；右上角保留搜索和 PDF 下载。</div>
          <div class="actions">
            <input id="search-input" class="search-input" placeholder="筛选附录中的面经：公司 / 岗位 / 标题" />
            <a class="button" href="{{ pdf_name }}">下载 PDF</a>
          </div>
        </div>

        <div id="overview" class="grid-2">
          <section class="report">
            <h2 class="section-title">高频知识点 Top 10</h2>
            <div class="table-wrap">
              <table>
                <thead><tr><th>知识点</th><th>题目数</th><th>涉及公司数</th><th>涉及面经数</th></tr></thead>
                <tbody>
                  {% for row in top_themes %}
                  <tr><td>{{ row.name }}</td><td>{{ row.question_count }}</td><td>{{ row.company_count }}</td><td>{{ row.post_count }}</td></tr>
                  {% endfor %}
                </tbody>
              </table>
            </div>
          </section>
          <section class="report" id="themes">
            <h2 class="section-title">高频题型 Top 10</h2>
            <div class="table-wrap">
              <table>
                <thead><tr><th>题型</th><th>命中题数</th><th>涉及公司数</th><th>涉及面经数</th></tr></thead>
                <tbody>
                  {% for row in top_topics %}
                  <tr><td>{{ row.name }}</td><td>{{ row.question_count }}</td><td>{{ row.company_count }}</td><td>{{ row.post_count }}</td></tr>
                  {% endfor %}
                </tbody>
              </table>
            </div>
          </section>
        </div>

        <section class="report" id="knowledge-nav">
          <h2 class="section-title">知识点快速导航</h2>
          <p style="color:var(--muted);margin-top:0">优先把高频知识点放在最前面。可以点击下面卡片进入，也可以直接点左侧目录树。</p>
          <div class="knowledge-grid">
            {% for item in knowledge_nav %}
            <a class="knowledge-card" href="#{{ item.anchor }}">
              <h3>{{ item.name }}</h3>
              <p>题目数 {{ item.question_count }} · 涉及公司 {{ item.company_count }} · 涉及面经 {{ item.post_count }}</p>
              <ul>
                {% for q in item.sample_questions %}
                <li>{{ q }}</li>
                {% endfor %}
              </ul>
            </a>
            {% endfor %}
          </div>
        </section>

        {% for item in knowledge_nav %}
        <section class="report" id="{{ item.anchor }}">
          <h2 class="section-title">{{ item.name }}</h2>
          <p style="color:var(--muted)">题目数 {{ item.question_count }} · 涉及公司 {{ item.company_count }} · 涉及面经 {{ item.post_count }}</p>
          <div class="chips" style="margin-bottom:14px">
            {% for company in item.companies[:12] %}
            <span class="chip">{{ company }}</span>
            {% endfor %}
          </div>
          <h3>代表题目</h3>
          <ul>
            {% for q in item.top_questions %}
            <li>{{ q[0] }} <span style="color:var(--muted)">（{{ q[1] }} 次）</span></li>
            {% endfor %}
          </ul>
        </section>
        {% endfor %}

        {% for section in sections %}
        <section class="report" id="{{ section.anchor }}">
          {{ section.html | safe }}
        </section>
        {% endfor %}

        <section class="report" id="latest">
          <h2 class="section-title">附录：最新面经列表</h2>
          <p style="color:var(--muted);margin-top:0">具体面经条目放在附录区，优先级低于前面的知识点导航、聚类和题库。</p>
          <div class="table-wrap">
            <table>
              <thead>
                <tr><th>日期</th><th>公司</th><th>岗位</th><th>轮次</th><th>标题</th><th>原帖</th></tr>
              </thead>
              <tbody>
                {% for item in latest_items %}
                <tr data-search-row="{{ item.created_date }} {{ item.company }} {{ item.role }} {{ item.round }} {{ item.title }}">
                  <td>{{ item.created_date }}</td>
                  <td>{{ item.company }}</td>
                  <td>{{ item.role }}</td>
                  <td>{{ item.round }}</td>
                  <td>{{ item.title }}</td>
                  <td><a href="{{ item.url }}" target="_blank" rel="noreferrer">查看原帖</a></td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>
        </section>

        <div class="footer">
          由本地脚本自动生成。更新流程：抓取牛客面经 → 分析聚类 → 生成网页/PDF。
        </div>
      </main>
    </div>
  </div>
  <script src="assets/app.js"></script>
</body>
</html>
''')


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=['extra', 'tables', 'fenced_code', 'toc', 'sane_lists', 'nl2br'],
        output_format='html5',
    )


def short_title(path: Path) -> str:
    name = path.stem
    name = name.replace('牛客近6个月AI应用开发面经-', '')
    if name == '牛客近6个月AI应用开发面经汇总':
        return '总汇总'
    return name


def anchor_from_path(path: Path) -> str:
    name = path.stem
    safe = ''.join(ch if ch.isascii() and ch.isalnum() else '-' for ch in name.lower())
    while '--' in safe:
        safe = safe.replace('--', '-')
    return safe.strip('-') or 'section'


def register_fonts() -> str:
    font_name = 'STSong-Light'
    try:
        pdfmetrics.registerFont(UnicodeCIDFont(font_name))
    except Exception:
        font_name = 'Helvetica'
    return font_name


def build_pdf(report_paths: list[Path], pdf_path: Path, stats: dict, top_companies: list[tuple[str, int]]) -> None:
    font_name = register_fonts()
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleCN', parent=styles['Title'], fontName=font_name, fontSize=24, leading=30, alignment=TA_CENTER, spaceAfter=14)
    h1_style = ParagraphStyle('H1CN', parent=styles['Heading1'], fontName=font_name, fontSize=18, leading=24, spaceBefore=10, spaceAfter=8)
    h2_style = ParagraphStyle('H2CN', parent=styles['Heading2'], fontName=font_name, fontSize=15, leading=20, spaceBefore=8, spaceAfter=6)
    h3_style = ParagraphStyle('H3CN', parent=styles['Heading3'], fontName=font_name, fontSize=13, leading=18, spaceBefore=6, spaceAfter=4)
    body_style = ParagraphStyle('BodyCN', parent=styles['BodyText'], fontName=font_name, fontSize=10.5, leading=15)
    code_style = ParagraphStyle('CodeCN', parent=body_style, fontName=font_name, fontSize=9.5, leading=13, leftIndent=12)
    small_style = ParagraphStyle('SmallCN', parent=body_style, fontName=font_name, fontSize=9.5, leading=13, textColor='#555555')

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=15 * mm, bottomMargin=15 * mm)
    story = []
    story.append(Paragraph('AI 应用开发面经仪表盘', title_style))
    story.append(Paragraph('牛客近 6 个月 AI 应用开发 / Agent / 大模型应用相关面经整理', small_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f'面经样本数：{stats["interview_count"]}　｜　提取题目数：{stats["question_count"]}　｜　覆盖公司数：{stats["company_count"]}', body_style))
    story.append(Paragraph(f'构建时间：{stats["generated_at"]}', body_style))
    story.append(Paragraph('Top 公司：' + '、'.join(f'{name}({count})' for name, count in top_companies[:10]), body_style))
    story.append(PageBreak())

    for idx, path in enumerate(report_paths):
        text = path.read_text(encoding='utf-8')
        for raw in text.splitlines():
            line = raw.rstrip()
            if not line.strip():
                story.append(Spacer(1, 4))
                continue
            escaped = escape(line)
            if line.startswith('# '):
                story.append(Paragraph(escape(line[2:].strip()), h1_style))
            elif line.startswith('## '):
                story.append(Paragraph(escape(line[3:].strip()), h2_style))
            elif line.startswith('### '):
                story.append(Paragraph(escape(line[4:].strip()), h3_style))
            elif line.startswith('|'):
                story.append(Paragraph(escaped.replace(' ', '&nbsp;'), code_style))
            elif re.match(r'^\s*[-*]\s+', line):
                content = re.sub(r'^\s*[-*]\s+', '• ', line)
                story.append(Paragraph(escape(content), body_style))
            elif re.match(r'^\s*\d+[.、]\s*', line):
                story.append(Paragraph(escape(line), body_style))
            elif line.startswith('> '):
                story.append(Paragraph(escape('引用：' + line[2:]), small_style))
            else:
                story.append(Paragraph(escaped, body_style))
        if idx != len(report_paths) - 1:
            story.append(PageBreak())

    doc.build(story)


def main() -> None:
    SITE_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)

    summary = json.loads(SUMMARY_JSON.read_text())
    analysis = json.loads(ANALYSIS_JSON.read_text())
    kept_items = summary['kept_items']
    question_count = sum(item['question_count'] for item in kept_items)
    company_counter = Counter(item['company'] for item in kept_items)
    generated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sections = []
    for idx, path in enumerate(REPORT_FILES, start=1):
        sections.append({
            'anchor': f'report-{idx}',
            'short_title': short_title(path),
            'html': md_to_html(path.read_text(encoding='utf-8')),
        })

    top_themes = [
        {'name': name, 'question_count': info['question_count'], 'company_count': len(info['companies']), 'post_count': info['post_count']}
        for name, info in list(analysis['theme_summary'].items())[:10]
    ]
    top_topics = [
        {'name': name, 'question_count': info['question_count'], 'company_count': len(info['companies']), 'post_count': info['post_count']}
        for name, info in list(analysis['topic_summary'].items())[:10]
    ]
    knowledge_nav = []
    for idx, (name, info) in enumerate(list(analysis['theme_summary'].items())[:10], start=1):
        if name == '其他':
            continue
        knowledge_nav.append({
            'name': name,
            'anchor': f'knowledge-{idx}',
            'question_count': info['question_count'],
            'company_count': len(info['companies']),
            'post_count': info['post_count'],
            'companies': info['companies'],
            'sample_questions': [q for q, _ in info['top_questions'][:3]],
            'top_questions': info['top_questions'][:8],
        })
    stats = {
        'interview_count': len(kept_items),
        'question_count': question_count,
        'company_count': len(company_counter),
        'generated_at': generated_at,
    }

    html = TEMPLATE.render(
        title='AI 应用开发面经仪表盘',
        subtitle='把牛客近 6 个月的 AI 应用开发 / Agent / 大模型应用相关面经，整理成可长期更新的本地网页。',
        stats=stats,
        top_companies=company_counter.most_common(10),
        top_themes=top_themes,
        top_topics=top_topics,
        latest_items=sorted(kept_items, key=lambda x: (x.get('created_date') or '', x['title']), reverse=True),
        knowledge_nav=knowledge_nav,
        sections=sections,
        pdf_name=PDF_PATH.name,
    )

    (ASSETS_DIR / 'styles.css').write_text(STYLE, encoding='utf-8')
    (ASSETS_DIR / 'app.js').write_text(SCRIPT, encoding='utf-8')
    INDEX_PATH.write_text(html, encoding='utf-8')
    build_pdf(REPORT_FILES, PDF_PATH, stats, company_counter.most_common(10))

    print(f'index={INDEX_PATH}')
    print(f'pdf={PDF_PATH}')


if __name__ == '__main__':
    main()
