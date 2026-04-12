#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

BASE_JSON = Path('牛客近6个月AI应用开发面经汇总.json')
OUT_CLUSTER_MD = Path('牛客近6个月AI应用开发面经-知识点聚类.md')
OUT_BANK_MD = Path('牛客近6个月AI应用开发面经-高频题题库与答案框架.md')
OUT_COMPANY_MD = Path('牛客近6个月AI应用开发面经-公司维度对比分析.md')
OUT_ANALYSIS_JSON = Path('牛客近6个月AI应用开发面经-分析结果.json')

THEME_RULES = [
    ('项目介绍与项目拷打', ['自我介绍', '项目拷打', '项目亮点', '负责的部分', '介绍一个你做的这个项目', '介绍你写的这个项目', '重点讲架构和你负责的部分', '你的ai项目的亮点']),
    ('Agent架构与范式', ['agent', '智能体', 'workflow', 'react', 'fsm', 'dag', '状态机', '规划', '执行', '反思', '单agent', '多agent', '编排']),
    ('记忆与上下文管理', ['记忆', '跨会话', '长期记忆', '短期记忆', '上下文', '聊天历史', '三层记忆', '压缩', 'session', '多轮']),
    ('RAG与检索优化', ['rag', '检索', '召回', '重排序', 'rerank', 'chunk', 'hyde', '向量', 'milvus', 'hnsw', 'ivf', 'pq', 'embedding', '索引', 'ocr', 'pdf', '表格', '语义分块']),
    ('评测、幻觉与数据集', ['评估', '评测', '指标', '成功率', '数据集', '打分', '裁判员', '幻觉', 'ab测试', 'a/b', '实验', '闭环', '准确率', '效果']),
    ('框架、MCP与工具调用', ['langchain', 'langgraph', 'mcp', 'function calling', 'functioncall', 'skill', 'skills', 'tool', 'spring ai', 'ailibaba', 'checkpoint', 'harness', 'cli']),
    ('模型基础与推理机制', ['transformer', 'kv cache', 'temperature', 'top-p', 'top-k', 'attention', '微调', '强化学习', 'llm', '大模型', '采样', '用过哪些模型', '模型选择']),
    ('AI Coding与协作方式', ['ai coding', 'claude code', 'auto-coder', '写代码', '开发方式', '拆解任务', 'hook', '编程工具']),
    ('后端基础与工程化', ['redis', 'mysql', 'kafka', 'rabbitmq', '缓存', 'mq', 'jmeter', '本地部署', '配置管理', '热更新', '高并发', '单线程', 'jvm', 'dns', 'tcp', 'get', 'post', '线程', '进程', 'java', 'python', '垃圾回收', '内存泄漏', '引用']),
    ('业务场景设计', ['游戏', '电商', '导购', '客服', '安全', '医院', '漫剧', '设计一个', '业务', '角色状态']),
    ('前端与跨端工程', ['flutter', 'react native', 'widget', 'layout', 'paint', 'composite', '前端', '流式交互', 'ui']),
    ('算法与编码题', ['算法', '手撕', '链表', '丑数', '中位数', '字符串', '水杯', 'lru']),
    ('HR与流程信息', ['实习多久', '转正率', '到岗', '暑期', 'offer', 'hr面']),
]

TOPIC_RULES = [
    ('项目介绍/项目拷打', ['自我介绍', '项目拷打', '项目亮点', '介绍你写的这个项目', '介绍一个你做的这个项目', '负责的部分', '你的ai项目的亮点']),
    ('Agent 与 workflow/单多 Agent 选型', ['workflow', '单agent', '多agent', 'agent 和传统', '智能体开发范式', '什么时候采用单agent', '为什么要做多 agent']),
    ('记忆系统设计', ['记忆', '跨会话', '长期记忆', '短期记忆', '上下文压缩', '三层记忆', '聊天历史']),
    ('RAG 系统设计', ['为什么要用 rag', 'rag 知识库', 'rag 的流程', 'rag 系统', 'rag 可以怎么分类', 'agentic rag', 'rag 项目']),
    ('检索/召回/重排/向量索引优化', ['召回', '重排', 'chunk', 'hyde', '向量', 'milvus', 'hnsw', 'ivf', 'pq', 'embedding', '索引', 'ocr', 'pdf', '表格', '语义分块']),
    ('RAG/Agent 评测与幻觉治理', ['评估', '评测', '指标', '成功率', '准确率', '幻觉', '闭环', 'ab测试', 'a/b', '实验', '数据集', '打分']),
    ('LangChain / LangGraph / 编排框架选型', ['langchain', 'langgraph', 'checkpoint', 'dag', '状态机', '编排']),
    ('MCP / Function Calling / Skills / Tool Calling', ['mcp', 'function calling', 'skill', 'skills', 'tool', 'cli']),
    ('意图识别与 Query 理解', ['意图识别', '意图判断', 'query']),
    ('AI Coding / Claude Code 实践', ['ai coding', 'claude code', 'auto-coder', 'hook', '写代码', '编程工具']),
    ('场景设计题（游戏/电商/安全/客服）', ['游戏', '电商', '导购', '客服', '安全', '医院', '漫剧', '设计一个']),
    ('后端基础：Redis/缓存/MQ/高并发', ['redis', '缓存', 'rabbitmq', 'kafka', '高并发', '单线程', 'jmeter']),
    ('模型基础：Transformer/KV Cache/Temperature', ['transformer', 'kv cache', 'temperature', 'attention', '微调', '强化学习']),
    ('算法题/手撕题', ['算法', '手撕', '链表', '丑数', '中位数', '字符串', '水杯', 'lru']),
]

ANSWER_FRAMEWORKS = {
    '项目介绍/项目拷打': [
        '先给业务背景：用户是谁、核心痛点是什么、为什么值得用 AI/Agent 做。',
        '再讲系统方案：输入 -> 处理链路 -> 模型/检索/工具 -> 输出。',
        '明确你自己的 ownership：你主导了哪几块，做了什么关键决策。',
        '量化结果：准确率、成功率、响应时延、成本、人工替代率。',
        '最后补一段复盘：踩过什么坑、怎么权衡、如果重做会怎么改。',
    ],
    'Agent 与 workflow/单多 Agent 选型': [
        '先下定义：workflow 是预定义流程，Agent 是基于上下文动态决策。',
        '再讲适用场景：稳定高频任务用 workflow；开放复杂任务才考虑 Agent。',
        '单 Agent 适合轻量任务，多 Agent 适合角色分工明显、工具复杂、需要并行/反思的场景。',
        '补充风险：多 Agent 会带来状态同步、成本、时延、调试难度。',
        '结尾给出选型原则：先 workflow，必要时再逐步 Agent 化。',
    ],
    '记忆系统设计': [
        '分层回答：短期记忆、长期记忆、用户画像/外部知识。',
        '说明写入时机：并不是“全量记忆”，而是事件触发/摘要压缩/显著性提取。',
        '说明存储介质：会话缓存、数据库/向量库、文件或 KV。',
        '说明召回策略：按用户、会话、任务阶段、时间窗口过滤。',
        '补充治理：过期淘汰、冲突解决、并发一致性、隐私隔离。',
    ],
    'RAG 系统设计': [
        '先回答为什么要用 RAG：补齐私域知识、降低幻觉、提升可控性。',
        '再讲链路：文档接入 -> 清洗切块 -> 索引 -> 召回 -> 重排 -> 生成。',
        '讲清关键设计：chunk 粒度、元数据、混合检索、引用回传。',
        '补充失败兜底：低置信度拒答、回退模板、人工介入。',
        '最后讲如何评估：检索命中率、答案正确率、业务指标。',
    ],
    '检索/召回/重排/向量索引优化': [
        '先拆问题：召回质量、排序质量、检索延迟、索引成本。',
        '回答常见优化：BM25 + 向量混检、query rewrite、HyDE、rerank。',
        '索引层说明：HNSW 适合高召回低延迟，IVF/PQ 更偏大规模压缩。',
        '针对 PDF/OCR/表格，强调结构化抽取和版面信息保留。',
        '结尾说评估方式：Recall@K、MRR、NDCG、端到端正确率。',
    ],
    'RAG/Agent 评测与幻觉治理': [
        '先分离检索评测和生成评测，不把问题混成一个指标。',
        '检索看 Recall@K / MRR / NDCG；生成看正确率、引用一致性、任务成功率。',
        '数据集来源要说清：真实日志、人工构造、失败样本回流。',
        '幻觉治理从三层答：输入约束、检索增强、输出校验/拒答。',
        '最好补线上监控：抽样复核、回流闭环、AB 实验。',
    ],
    'LangChain / LangGraph / 编排框架选型': [
        '先说定位：LangChain 偏快速搭链路，LangGraph 偏复杂状态机编排。',
        '如果有分支、循环、重试、人工介入、checkpoint，LangGraph 更合适。',
        '如果只是简单工具串联，LangChain 更轻更快。',
        '选型时讲维度：开发效率、可观测性、状态管理、扩展性、维护成本。',
        '最后结合自己项目说“为什么这次这么选”。',
    ],
    'MCP / Function Calling / Skills / Tool Calling': [
        '先逐一定义概念，不要混着说。',
        'Function Calling/Tool Calling 是模型触发工具；Skill 更像能力封装；MCP 更像工具/上下文接入协议。',
        '说明它们如何协同：模型规划 -> 选择工具/skill -> 调用执行 -> 回填结果。',
        '补充工程问题：权限、超时、幂等、失败重试、可观测性。',
        '最后说实际价值：降低接入成本，提高复用和治理能力。',
    ],
    '意图识别与 Query 理解': [
        '先说明方法：规则、小模型分类、大模型判断、混合路由。',
        '再说输入特征：用户 query、上下文、历史行为、业务元数据。',
        '重点讲评估：准确率、召回率、混淆类目、线上误判样本。',
        '强调兜底：低置信度回退到澄清问句或保守策略。',
        '如果业务复杂，要补“多意图/歧义 query 如何处理”。',
    ],
    'AI Coding / Claude Code 实践': [
        '先说你怎么用：需求澄清、方案草拟、代码生成、测试补齐、文档整理。',
        '强调边界：AI 适合提效，不直接代替关键设计和最终验收。',
        '保证质量的办法：任务拆小、明确约束、提供上下文、单测/人工 review。',
        '补充失败场景：需求模糊、跨文件重构、隐式约束多时容易跑偏。',
        '最后说你自己的最佳实践和收益。',
    ],
    '场景设计题（游戏/电商/安全/客服）': [
        '先画业务目标：用户是谁，核心任务是什么，成功指标是什么。',
        '再拆系统：意图识别、检索/知识库、工具调用、状态管理、输出策略。',
        '说明为什么需要 Agent/多 Agent，以及每个角色负责什么。',
        '补稳定性与安全：权限、审计、拒答、异常兜底。',
        '最后补评测与上线：离线集、灰度、AB、人工复核。',
    ],
    '后端基础：Redis/缓存/MQ/高并发': [
        '先回到业务问题：为什么引入缓存/MQ，而不是只背定义。',
        'Redis 重点答数据结构、单线程高性能原因、持久化/集群/一致性。',
        'MQ 重点答解耦、削峰、异步，以及顺序性、幂等、丢消息治理。',
        '缓存题要讲失效策略、穿透击穿雪崩、冷热数据。',
        '最好结合自己项目里实际怎么用。',
    ],
    '模型基础：Transformer/KV Cache/Temperature': [
        'Transformer 至少讲清 self-attention、前馈层、位置编码、残差归一化。',
        'KV Cache 要说明它缓存什么、为什么能加速 decode、代价是什么。',
        'Temperature/Top-p/Top-k 回答采样多样性与稳定性的权衡。',
        '如果问微调/强化学习，先分清 SFT、偏好优化、在线强化。',
        '强调“懂概念 + 懂工程影响”，不要只背术语。',
    ],
    '算法题/手撕题': [
        '先确认题意和输入输出边界。',
        '说思路时先给复杂度，再落到数据结构选择。',
        '编码时注意鲁棒性、边界条件、变量命名。',
        '写完主动做样例验证。',
        '如果时间不够，先给可行解再优化。',
    ],
}

COMPANY_STYLE_HINTS = {
    '字节': '项目细节会深挖到记忆、评测、数据集、并发隔离，常伴随模型基础或算法题。',
    '腾讯': '偏应用架构与工程实现，常问记忆、Skill/MCP、状态机、LangChain/LangGraph。',
    '淘天': '偏 Agent 范式、记忆设计、RAG 优化和业务场景落地，也会问实验与成本。',
    '阿里国际': '除了 AI 应用本身，还会穿插 Python/计网/操作系统等通用基础。',
    '阿里云': '偏场景系统设计和高风险场景治理，重视 RAG 评测与幻觉控制。',
    '阿里灵犀互娱': '强业务场景题，尤其游戏客服/游戏助手/多 Agent 设计。',
    '快手': 'AI 应用 + 后端八股混合考，Redis/MQ/框架选型比重高。',
    '小红书': 'Agent / RAG / 向量索引问得系统，喜欢考概念边界与检索细节。',
    '京东': '重 workflow、RAG、意图识别和电商业务场景，兼顾缓存与压测。',
    '蚂蚁': '偏 RAG 细节、重排、幻觉、采样参数和项目追问。',
    '高德': '偏跨端工程与 AI Coding 协作方式，也会问 Agent skill 拆分。',
    '蔚来': '更偏服务端基础 + AI 应用结合。',
    '百度': '偏 Agent 项目深挖，关注规划、记忆、工具调用和评测。',
    '米哈游': '偏游戏场景下的 Agent 设计、状态定义与记忆管理。',
}


def norm_q(q: str) -> str:
    q = re.sub(r'^\s*\d+[.、]\s*', '', q)
    q = re.sub(r'^\s*[（(]?[一二三四五六七八九十]+[）)]\s*', '', q)
    return re.sub(r'\s+', ' ', q).strip(' ：:;；，,。')


LOW_VALUE_PATTERNS = ['没后续', '攒人品', '反问', '具体部门业务', '有啥了解吗', '有啥了解', '要是到', '能来实习', '能实习多久']


def is_low_value(q: str) -> bool:
    return any(p in q for p in LOW_VALUE_PATTERNS)


def assign_theme(q: str) -> str:
    lower = q.lower()
    best_theme = '其他'
    best_score = 0
    for theme, kws in THEME_RULES:
        score = sum(1 for kw in kws if kw.lower() in lower)
        if score > best_score:
            best_score = score
            best_theme = theme
    return best_theme


def matched_topics(q: str) -> list[str]:
    lower = q.lower()
    hits = []
    for topic, kws in TOPIC_RULES:
        if any(kw.lower() in lower for kw in kws):
            hits.append(topic)
    return hits


def md_link(text: str, url: str) -> str:
    return f'[{text}]({url})'


def top_n(counter: Counter, n: int) -> list[tuple[str, int]]:
    return counter.most_common(n)


def main() -> None:
    data = json.loads(BASE_JSON.read_text())
    items = data['kept_items']

    theme_questions = defaultdict(list)
    theme_companies = defaultdict(set)
    theme_posts = defaultdict(set)
    topic_questions = defaultdict(list)
    topic_companies = defaultdict(set)
    topic_posts = defaultdict(set)
    company_posts = defaultdict(list)
    company_theme_counter = defaultdict(Counter)
    company_topic_counter = defaultdict(Counter)

    for item in items:
        company_posts[item['company']].append(item)
        seen_theme_in_post = set()
        seen_topic_in_post = set()
        for raw_q in item['questions']:
            q = norm_q(raw_q)
            if not q or is_low_value(q):
                continue
            theme = assign_theme(q)
            theme_questions[theme].append({'q': q, 'company': item['company'], 'title': item['title'], 'url': item['url']})
            theme_companies[theme].add(item['company'])
            theme_posts[theme].add(item['title'])
            if theme not in seen_theme_in_post:
                company_theme_counter[item['company']][theme] += 1
                seen_theme_in_post.add(theme)
            for topic in matched_topics(q):
                topic_questions[topic].append({'q': q, 'company': item['company'], 'title': item['title'], 'url': item['url']})
                topic_companies[topic].add(item['company'])
                topic_posts[topic].add(item['title'])
                if topic not in seen_topic_in_post:
                    company_topic_counter[item['company']][topic] += 1
                    seen_topic_in_post.add(topic)

    # cluster markdown
    cluster_lines = [
        '# 牛客近6个月AI应用开发面经：知识点聚类',
        '',
        f'- 面经样本数：{len(items)}',
        f'- 提取题目数：{sum(len(item["questions"]) for item in items)}',
        '',
        '## 聚类总览',
        '',
        '| 知识点 | 题目数 | 涉及公司数 | 涉及面经数 |',
        '|---|---:|---:|---:|',
    ]
    theme_rank = sorted(theme_questions.keys(), key=lambda t: (t == '其他', -len(theme_questions[t])) if t == '其他' else (False, -len(theme_questions[t])))
    for theme in theme_rank:
        cluster_lines.append(f'| {theme} | {len(theme_questions[theme])} | {len(theme_companies[theme])} | {len(theme_posts[theme])} |')
    cluster_lines += ['', '## 逐类展开', '']
    for theme in theme_rank:
        cluster_lines += [f'### {theme}', '']
        cluster_lines.append(f'- 题目数：{len(theme_questions[theme])}')
        cluster_lines.append(f'- 覆盖公司：{"、".join(sorted(theme_companies[theme]))}')
        rep_counter = Counter(x['q'] for x in theme_questions[theme])
        cluster_lines.append('- 代表题目：')
        for q, count in rep_counter.most_common(8):
            companies = sorted({x['company'] for x in theme_questions[theme] if x['q'] == q})
            cluster_lines.append(f'  - ({count}) {q} —— {"、".join(companies)}')
        cluster_lines.append('')

    # topic / answer bank markdown
    bank_lines = [
        '# 牛客近6个月AI应用开发面经：高频题题库与答案框架',
        '',
        f'- 面经样本数：{len(items)}',
        f'- 高频主题数：{len(topic_questions)}',
        '',
        '## 高频题总览',
        '',
        '| 高频题主题 | 命中题数 | 涉及公司数 | 涉及面经数 |',
        '|---|---:|---:|---:|',
    ]
    topic_rank = sorted(topic_questions.keys(), key=lambda t: len(topic_questions[t]), reverse=True)
    for topic in topic_rank:
        bank_lines.append(f'| {topic} | {len(topic_questions[topic])} | {len(topic_companies[topic])} | {len(topic_posts[topic])} |')
    bank_lines += ['', '## 题库与答案框架', '']
    for topic in topic_rank:
        rep_counter = Counter(x['q'] for x in topic_questions[topic])
        bank_lines += [f'### {topic}', '']
        bank_lines.append(f'- 命中题数：{len(topic_questions[topic])}')
        bank_lines.append(f'- 涉及公司：{"、".join(sorted(topic_companies[topic]))}')
        bank_lines.append('- 高频问法：')
        for q, count in rep_counter.most_common(6):
            bank_lines.append(f'  - ({count}) {q}')
        framework = ANSWER_FRAMEWORKS.get(topic)
        if framework:
            bank_lines.append('- 答案框架：')
            for step in framework:
                bank_lines.append(f'  1. {step}' if step == framework[0] else f'  - {step}')
        bank_lines.append('')

    # company analysis markdown
    company_lines = [
        '# 牛客近6个月AI应用开发面经：公司维度对比分析',
        '',
        f'- 统计公司数：{len(company_posts)}',
        '',
        '## 公司总览',
        '',
        '| 公司 | 面经数 | 高频知识点 | 风格提示 |',
        '|---|---:|---|---|',
    ]
    company_rank = sorted(company_posts.keys(), key=lambda c: len(company_posts[c]), reverse=True)
    for company in company_rank:
        filtered_themes = [(t,cnt) for t,cnt in company_theme_counter[company].most_common() if t != '其他'] or company_theme_counter[company].most_common(3)
        top_themes = '、'.join(t for t, _ in filtered_themes[:3])
        style = COMPANY_STYLE_HINTS.get(company, '以具体项目深挖为主，建议按该公司的高频知识点准备。')
        company_lines.append(f'| {company} | {len(company_posts[company])} | {top_themes} | {style} |')
    company_lines += ['', '## 逐公司分析', '']
    for company in company_rank:
        company_lines += [f'### {company}', '']
        company_lines.append(f'- 面经数：{len(company_posts[company])}')
        company_lines.append(f'- 风格画像：{COMPANY_STYLE_HINTS.get(company, "以具体项目深挖为主，建议按该公司的高频知识点准备。")}')
        company_lines.append('- 高频知识点：')
        filtered_theme_details = [(t,cnt) for t,cnt in company_theme_counter[company].most_common() if t != '其他'] or company_theme_counter[company].most_common(6)
        for theme, count in filtered_theme_details[:6]:
            company_lines.append(f'  - {theme}: {count}')
        company_lines.append('- 高频题型：')
        for topic, count in company_topic_counter[company].most_common(6):
            company_lines.append(f'  - {topic}: {count}')
        company_lines.append('- 相关面经：')
        for item in sorted(company_posts[company], key=lambda x: x['created_date'], reverse=True):
            company_lines.append(f'  - {item["created_date"]}｜{md_link(item["title"], item["url"])}')
        company_lines.append('')

    OUT_CLUSTER_MD.write_text('\n'.join(cluster_lines) + '\n', encoding='utf-8')
    OUT_BANK_MD.write_text('\n'.join(bank_lines) + '\n', encoding='utf-8')
    OUT_COMPANY_MD.write_text('\n'.join(company_lines) + '\n', encoding='utf-8')
    OUT_ANALYSIS_JSON.write_text(json.dumps({
        'theme_summary': {
            theme: {
                'question_count': len(theme_questions[theme]),
                'companies': sorted(theme_companies[theme]),
                'post_count': len(theme_posts[theme]),
                'top_questions': Counter(x['q'] for x in theme_questions[theme]).most_common(10),
            }
            for theme in theme_rank
        },
        'topic_summary': {
            topic: {
                'question_count': len(topic_questions[topic]),
                'companies': sorted(topic_companies[topic]),
                'post_count': len(topic_posts[topic]),
                'top_questions': Counter(x['q'] for x in topic_questions[topic]).most_common(10),
            }
            for topic in topic_rank
        },
        'company_summary': {
            company: {
                'post_count': len(company_posts[company]),
                'top_themes': company_theme_counter[company].most_common(10),
                'top_topics': company_topic_counter[company].most_common(10),
                'titles': [item['title'] for item in sorted(company_posts[company], key=lambda x: x['created_date'], reverse=True)],
            }
            for company in company_rank
        }
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('cluster', OUT_CLUSTER_MD)
    print('bank', OUT_BANK_MD)
    print('company', OUT_COMPANY_MD)
    print('analysis', OUT_ANALYSIS_JSON)


if __name__ == '__main__':
    main()
