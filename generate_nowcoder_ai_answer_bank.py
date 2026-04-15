#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ANALYSIS_JSON = Path('牛客近6个月AI应用开发面经-分析结果.json')
OUT_MD = Path('牛客近6个月AI应用开发面经-逐题优秀答案稿.md')
OUT_JSON = Path('牛客近6个月AI应用开发面经-逐题优秀答案稿.json')


TOPIC_ORDER = [
    '项目介绍/项目拷打',
    'Agent 与 workflow/单多 Agent 选型',
    '记忆系统设计',
    'RAG 系统设计',
    '检索/召回/重排/向量索引优化',
    'RAG/Agent 评测与幻觉治理',
    'LangChain / LangGraph / 编排框架选型',
    'MCP / Function Calling / Skills / Tool Calling',
    '意图识别与 Query 理解',
    'AI Coding / Claude Code 实践',
    '场景设计题（游戏/电商/安全/客服）',
    '后端基础：Redis/缓存/MQ/高并发',
    '模型基础：Transformer/KV Cache/Temperature',
    '算法题/手撕题',
]


STYLE_GUIDE = [
    '先给结论，不先绕概念背景。',
    '定义、适用边界、工程取舍三件事同时讲清。',
    '尽量带指标、代价、失败场景和兜底策略。',
    '项目题不编造经历；没有做过的部分明确说“当时没做到，但我会这样补”。',
    '面试表达优先“我的判断 -> 为什么 -> 怎么落地 -> 怎么验证”。',
]


def qkey(text: str) -> str:
    text = re.sub(r'^\(\d+\)\s*', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def add_entry(groups: dict[str, list[dict]], topic: str, question: str, count: int) -> None:
    question = qkey(question)
    if not question:
        return
    if not any(item['question'] == question for item in groups[topic]):
        groups[topic].append({'question': question, 'count': count})


def topic_from_question(question: str, fallback_topic: str) -> str:
    q = question.lower()
    mapping = [
        ('项目介绍/项目拷打', ['自我介绍', '项目拷打', '介绍你', '介绍一个你做的这个项目', '亮点', '负责的部分']),
        ('记忆系统设计', ['记忆', '聊天历史', '长期记忆', '短期记忆', '压缩']),
        ('RAG 系统设计', ['agentic rag', 'rag 知识库', 'rag 可以怎么分类', '为什么要用 rag', 'rag 的流程', 'rag 系统']),
        ('检索/召回/重排/向量索引优化', ['召回', '重排', 'hyde', 'ivf', 'pq', '向量', '索引', 'chunk', 'ocr', 'pdf']),
        ('RAG/Agent 评测与幻觉治理', ['评估', '评测', '幻觉', '闭环', 'ab 测试', 'a/b', '成功率', '准确率', '数据集']),
        ('LangChain / LangGraph / 编排框架选型', ['langchain', 'langgraph', 'spring ai', 'ailibaba', 'dag', 'checkpoint']),
        ('MCP / Function Calling / Skills / Tool Calling', ['mcp', 'function calling', 'skill', 'skills', 'tool calling', 'cli']),
        ('意图识别与 Query 理解', ['意图识别', '意图判断', 'query']),
        ('AI Coding / Claude Code 实践', ['claude code', 'ai coding', 'hook', 'auto-coder', '写代码']),
        ('场景设计题（游戏/电商/安全/客服）', ['游戏', '电商', '导购', '客服', '安全', '医院', '漫剧', '设计智能体']),
        ('后端基础：Redis/缓存/MQ/高并发', ['redis', '缓存', 'rabbitmq', 'kafka', 'jmeter', '高并发', 'mysql']),
        ('模型基础：Transformer/KV Cache/Temperature', ['transformer', 'attention', 'kv cache', 'temperature', 'top-p', 'top-k']),
        ('算法题/手撕题', ['算法', '手撕', '链表', '中位数', '字符串', 'lru']),
        ('Agent 与 workflow/单多 Agent 选型', ['workflow', '单agent', '多agent', 'react', 'fsm', '状态机', '范式', 'agent ']),
    ]
    for topic, kws in mapping:
        if any(kw in q for kw in kws):
            return topic
    return fallback_topic


def bullets(*items: str) -> list[str]:
    return [item for item in items if item]


def answer_project(question: str) -> tuple[list[str], list[str], list[str]]:
    if '自我介绍' in question:
        answer = bullets(
            '我会用“背景-项目-能力-匹配度”四段式来答，控制在 1 到 2 分钟。',
            '例如：我主要做过 AI 应用开发和全栈/后端工程，最近一段经历聚焦在 Agent、RAG、工具调用和工程落地。我比较强的点不是只会调模型，而是能把检索、记忆、工具、评测和后端服务串成一个可上线系统。',
            '项目里我通常负责核心链路设计和工程落地，比如知识库接入、检索优化、工具调用协议、状态管理、评测闭环，以及线上问题排查和性能优化。',
            '我现在投这个岗位，是因为它既要求 AI 应用理解，也要求工程实现，我过去的经历比较匹配，而且我更擅长把不稳定的 demo 做成可维护、可评估、可迭代的产品能力。',
        )
        plus = bullets('最后一句要强行收束到“我为什么适合这个岗位”。', '别把经历按时间流水账罗列，要围绕岗位能力讲。')
        avoid = bullets('不要一上来讲兴趣爱好。', '不要说自己“主要靠大模型写代码”，会显得 ownership 不足。')
        return answer, plus, avoid
    answer = bullets(
        '先讲业务目标和用户痛点，再讲架构链路，最后讲你自己的 ownership 和结果。',
        '优秀候选人的答法不是“我做了一个 Agent”，而是“我为了解决什么问题，为什么选这个方案，这个方案具体怎么工作”。',
        '项目链路建议按“输入 -> 预处理 -> 检索/记忆/工具 -> 规划执行 -> 输出校验 -> 监控评测”来讲。',
        '一定补指标，例如成功率、延迟、人工替代率、命中率、成本变化；如果没有现成指标，就坦诚说当时没有系统化监控，但我现在会补这几类指标。',
        '最后一定复盘一个 trade-off，例如为什么没上多 Agent、为什么先做混合检索、为什么记忆不做全量写入。',
    )
    plus = bullets('如果面试官追问，先守住业务目标和技术决策依据。', '项目题最加分的是“知道自己没做好的地方以及如何补”。')
    avoid = bullets('不要把所有技术名词堆一遍。', '不要只讲功能，不讲你负责什么。')
    return answer, plus, avoid


def answer_agent(question: str) -> tuple[list[str], list[str], list[str]]:
    q = question.lower()
    if '多 agent' in q or '多agent' in q or '单agent' in q:
        answer = bullets(
            '我的判断是：默认先用 workflow 或单 Agent，只有在角色分工明显、工具复杂、需要并行或反思时，才引入多 Agent。',
            '单 Agent 的优势是实现简单、上下文集中、成本和时延可控；多 Agent 的优势是职责清晰、可并行、便于隔离不同策略，但代价是状态同步、调度复杂度、失败链路都会上升。',
            '如果任务本质是固定流程，比如检索、摘要、生成、审核几步相对稳定，我更倾向 workflow；如果需要动态规划、多轮纠错、角色协作，才会考虑 Agent 化。',
            '所以选型标准不是“是否更酷”，而是看任务开放度、可预测性、失败成本和维护成本。',
        )
    elif 'workflow' in q:
        answer = bullets(
            'workflow 和 Agent 的核心区别在于：workflow 是预定义路径，Agent 是基于上下文动态选择下一步动作。',
            '我通常先问两个问题：任务步骤能不能提前穷举？失败后允许不允许探索？如果能穷举且稳定，就优先 workflow。',
            '很多线上场景其实不需要“强自主”，因为可预测、可审计、低成本比灵活性更重要。',
            '只有当任务存在不确定路径、工具组合多、需要反思或多轮规划时，Agent 才真正有价值。',
        )
    else:
        answer = bullets(
            '优秀答法要把 Agent 拆成规划、执行、观察、反思、状态管理五层，而不是只说“模型会自己调用工具”。',
            '我会强调 Agent 只是控制逻辑，真正决定稳定性的还是工具边界、状态管理、异常处理和评测闭环。',
            '如果是线上系统，我更关注“是否可回放、可审计、可中断、可恢复”，这比 demo 跑通更重要。',
        )
    plus = bullets('补一句“我默认从简单方案起步”，会显得工程判断成熟。', '如果做过状态机或 DAG，补一个真实例子最加分。')
    avoid = bullets('不要把 ReAct 当成所有 Agent 的同义词。', '不要说“多 Agent 一定更强”。')
    return answer, plus, avoid


def answer_memory(question: str) -> tuple[list[str], list[str], list[str]]:
    answer = bullets(
        '我会把记忆分成三层：当前会话短期记忆、跨会话长期记忆、用户画像/业务外部知识。三层职责不同，不能混在一起。',
        '短期记忆解决当前任务上下文连续性，通常用窗口、摘要或关键状态维护；长期记忆存稳定偏好、历史任务结论、可复用事实；外部知识则是知识库或业务系统，不应该伪装成“记忆”。',
        '记忆不是全量写入，而是事件触发写入：比如用户偏好更新、任务完成结论、长期有效约束。否则噪声会把召回质量拖垮。',
        '读的时候我会按用户、任务阶段、时间窗口、置信度过滤，再做摘要拼接，避免把过多低价值历史塞回上下文。',
        '真正的难点是治理：冲突怎么处理、过期怎么清、隐私如何隔离、并发更新如何保证一致性。',
    )
    plus = bullets('如果被追问评估，回答“看跨轮成功率、历史事实命中率、无关记忆污染率”。', '提到“全都记住通常是坏事”会显得你真做过。')
    avoid = bullets('不要把聊天历史直接等同于记忆。', '不要只讲向量库，不讲写入策略和淘汰策略。')
    return answer, plus, avoid


def answer_rag_system(question: str) -> tuple[list[str], list[str], list[str]]:
    answer = bullets(
        '我会先说明为什么需要 RAG：核心不是“让模型更聪明”，而是补齐私域知识、降低幻觉、提高可控性和可引用性。',
        '完整链路是：文档接入 -> 清洗/结构化 -> 切块 -> 建索引 -> 召回 -> 重排 -> 生成 -> 引用/拒答。',
        '关键设计点通常是 chunk 粒度、元数据设计、混合检索、query rewrite、低置信度拒答，以及引用证据如何回传到答案。',
        '如果是 Agentic RAG，我会强调它不是普通 RAG 加个名字，而是在检索前后允许模型做任务分解、查询改写、多轮检索和结果验证。',
        '最后讲评估：检索命中率、答案正确率、引用一致性、任务成功率和线上反馈闭环。',
    )
    plus = bullets('如果题目偏业务，补“为什么不用纯 LLM 直答”。', '如果题目偏工程，补“PDF、表格、OCR 需要保留结构信息”。')
    avoid = bullets('不要只讲向量数据库。', '不要把 RAG 说成一个检索接口调用。')
    return answer, plus, avoid


def answer_retrieval(question: str) -> tuple[list[str], list[str], list[str]]:
    q = question.lower()
    if 'hyde' in q:
        answer = bullets(
            'HyDE 的核心思路是先让模型为用户问题生成一个“假想答案”，再拿这个假想答案去做向量检索，因为它通常比原始 query 语义更完整。',
            '它适合原始 query 很短、表达模糊、领域术语缺失的场景，尤其当语料本身是描述性文本时会有帮助。',
            '但它也可能害人：如果模型先编出错误方向，检索会被带偏，尤其在高风险场景或 query 已经很明确时反而会引入噪声。',
            '所以我的做法通常不是盲开，而是做成可配置策略，并通过 Recall@K、MRR、端到端正确率验证收益。',
        )
    elif 'ivf' in q or 'pq' in q or '索引' in q:
        answer = bullets(
            '向量索引的本质是用空间划分或近似搜索，把“全量暴力比对”变成“更小候选集上的近似检索”。',
            'HNSW 更适合高召回、低时延和中大规模场景；IVF 先做粗聚类，再只搜少量桶；PQ 通过量化压缩向量降低存储和计算；IVF-PQ 则是两者结合，换空间和召回来换规模能力。',
            '所以没有绝对最优，只有业务 trade-off：如果你更看重召回质量，优先 HNSW；如果向量规模极大、内存压力大，才更认真考虑 IVF/PQ 体系。',
            '优秀候选人会补一句：索引优化不能只看 QPS，还要看召回率和端到端答案质量是否下降。',
        )
    elif '召回闭环' in q or '多路召回' in q or '重排序' in q:
        answer = bullets(
            '我会把召回闭环分成四件事：离线标注集、线上失败样本回流、查询改写策略、重排与阈值调优。',
            '召回层通常不只一路，我更倾向 BM25、向量检索、规则召回并行，然后用 rerank 统一排序，避免单路召回盲区。',
            '闭环的关键不是“多做一些 trick”，而是建立失败样本到策略改进的路径，比如 query rewrite、chunk 策略调整、元数据过滤和重排阈值优化。',
            '最终验证看 Recall@K、MRR、NDCG，以及端到端正确率是否真的提升。',
        )
    else:
        answer = bullets(
            '检索优化我会从召回质量、排序质量、延迟、存储成本四个维度来答，而不是只盯着某一个索引算法。',
            '常见手段包括混合检索、query rewrite、HyDE、元数据过滤、重排模型、chunk 优化和结构化信息保留。',
            '如果文档是 PDF、OCR、表格，版面结构和字段抽取往往比单纯换索引更重要。',
        )
    plus = bullets('回答检索题时，记得最后落到评估指标。', '如果提到 PDF/OCR/表格，会显得更贴近真实业务。')
    avoid = bullets('不要把“召回”和“重排”混为一谈。', '不要只背 HNSW/IVF 名字，不讲适用场景。')
    return answer, plus, avoid


def answer_eval(question: str) -> tuple[list[str], list[str], list[str]]:
    answer = bullets(
        '我会先把问题拆开：检索效果评测、生成效果评测、业务效果评测，三者不能混成一个分数。',
        '检索层看 Recall@K、MRR、NDCG；生成层看正确率、引用一致性、拒答合理性、任务成功率；业务层看转化、耗时、人工替代率等指标。',
        '离线数据集最好来自三类：真实日志回流、人工构造难例、线上失败样本。这样才能覆盖常见 query、边界 query 和高风险 query。',
        '幻觉治理我会从输入约束、检索增强、输出校验三层处理：必要时要求引用、关键事实做 grounding 检查、低置信度直接拒答。',
        '如果是在线实验，我会强调 AI 应用比传统 AB 更难，因为输出非确定、长尾问题多、人工标注成本高，所以要结合抽样复核和灰度放量。',
    )
    plus = bullets('补一句“不要把用户反馈当唯一指标”，很加分。', '高风险场景主动提拒答和人工复核。')
    avoid = bullets('不要说“效果主要看感觉”。', '不要只讲一个 LLM-as-a-judge 分数。')
    return answer, plus, avoid


def answer_framework(question: str) -> tuple[list[str], list[str], list[str]]:
    answer = bullets(
        '我通常先说定位：LangChain 更像快速搭建链路的应用框架，LangGraph 更适合有显式状态、分支、循环、重试、人工介入的复杂编排。',
        '如果流程比较线性，比如检索、生成、解析、存储几步串起来，LangChain 会更轻；如果任务有状态机特征、需要 checkpoint 或中断恢复，LangGraph 更合适。',
        '选型时我会看五个维度：开发效率、状态管理、可观测性、故障恢复、维护成本，而不是看哪个概念更新。',
        '如果题目问到 Spring AI / LangChain4j / Ailibaba，我会把答案落在语言生态、团队技术栈、接入成本和扩展性上。',
    )
    plus = bullets('最加分的是结合自己项目给出“为什么这次这样选”。', '提到 checkpoint、人工介入、回放，会显得更工程化。')
    avoid = bullets('不要把框架名当能力本身。', '不要为了显得高级而强行上复杂编排。')
    return answer, plus, avoid


def answer_tools(question: str) -> tuple[list[str], list[str], list[str]]:
    answer = bullets(
        '我的回答会先把概念拆开：Function Calling/Tool Calling 是模型触发某个工具；Skill 是把一类能力封装成可复用单元；MCP 更像工具与上下文接入协议。',
        '它们的关系可以理解为：模型负责规划，Tool/Skill 负责执行，MCP 负责以统一方式暴露能力和上下文。',
        '工程上我更关心权限、参数校验、超时、幂等、失败重试和可观测性，因为真正线上不稳定的往往不是“模型会不会调工具”，而是工具链路本身。',
        '如果问 skill 联动，我会强调它们当然可以组合，但组合前提是输入输出契约清晰、权限边界明确、异常能定位。',
    )
    plus = bullets('优秀候选人会主动补一句“这些概念不要混着用”。', '如果提到 schema 校验、审计日志，会更强。')
    avoid = bullets('不要把 MCP 说成某个具体产品。', '不要只讲业务价值，不讲技术拆分。')
    return answer, plus, avoid


def answer_intent(question: str) -> tuple[list[str], list[str], list[str]]:
    answer = bullets(
        '意图识别我一般不把它只当分类模型问题，而是当路由问题：决定后续是检索、工具调用、澄清追问还是直接回答。',
        '实现上可以是规则、小模型分类、大模型判断、混合路由；具体选什么看业务复杂度和稳定性要求。',
        '我会特别强调低置信度处理：不要硬判错意图，而是回退到澄清问句或保守路径。',
        '评估除了整体准确率，更要看混淆类目、长尾 query、线上误判成本，因为错路由的代价通常比“不答”更高。',
    )
    plus = bullets('把“低置信度兜底”说出来很加分。', '如果是电商/客服，可补充上下文和用户行为特征。')
    avoid = bullets('不要只讲一个分类模型名字。', '不要忽略多意图和歧义 query。')
    return answer, plus, avoid


def answer_ai_coding(question: str) -> tuple[list[str], list[str], list[str]]:
    answer = bullets(
        '我会把 AI Coding 当成提效工具，而不是把代码责任外包给模型。我的流程一般是：先澄清需求、拆小任务、提供上下文、生成代码、补测试、人工 review。',
        '保证结果稳定的关键不是“换更强模型”，而是把任务拆成可验证的小步，并明确约束、输入输出、边界条件和验收标准。',
        '我通常让 AI 处理脚手架、重复样板、测试、重构建议、文档整理；核心设计、跨模块改动和最终验收仍然由我自己负责。',
        '如果问收益，我会说它最稳定的价值是缩短实现和排查时间，而不是保证一次生成正确。',
    )
    plus = bullets('补一句“我会让 AI 给出测试样例和失败用例”，很加分。', '如果你真在用 Claude Code，可以举一两个协作实例。')
    avoid = bullets('不要说“我基本都让 AI 写”。', '不要回避质量控制和安全问题。')
    return answer, plus, avoid


def answer_scene(question: str) -> tuple[list[str], list[str], list[str]]:
    answer = bullets(
        '场景题我会先讲目标用户、核心任务和成功指标，再讲系统结构；优秀候选人不会一上来就堆技术方案。',
        '系统层通常拆成：意图识别、知识/检索、工具调用、状态管理、输出约束、评测监控。',
        '如果是高风险场景，比如安全、医疗、金融，我会强调权限控制、引用证据、拒答策略、人工兜底和审计日志。',
        '如果是电商或客服场景，我会补充业务指标，比如转化率、客服节省时长、订单完成率、投诉率等。',
        '最后再解释为什么这里需要 Agent，而不是普通 workflow 或问答系统。',
    )
    plus = bullets('一定主动谈稳定性和安全性。', '如果能补离线评测+灰度上线，会更完整。')
    avoid = bullets('不要把场景题答成“我会用一个大模型”。', '不要忽略业务指标。')
    return answer, plus, avoid


def answer_backend(question: str) -> tuple[list[str], list[str], list[str]]:
    q = question.lower()
    if 'redis' in q:
        answer = bullets(
            'Redis 题我会先回到业务用途：缓存、会话、限流、排行榜、向量检索缓存，而不是只背定义。',
            '如果问单线程高性能，我会讲内存操作、IO 多路复用、数据结构高效、避免线程切换四点；如果问集群，我会补 slot 分片、主从复制、故障转移和一致性代价。',
            '如果问缓存设计，我会把 key 设计、过期策略、热点处理、穿透击穿雪崩、回源治理讲清。',
            '如果问向量检索缓存，我会说缓存的是 query embedding、召回结果或 rerank 结果，并说明失效策略和命中条件。',
        )
    elif 'mq' in q or 'rabbitmq' in q or 'kafka' in q:
        answer = bullets(
            'MQ 题我会先讲为什么需要它：解耦、削峰、异步，而不是先背消息模型。',
            '选型时会比较吞吐、延迟、顺序性、消费语义、生态和团队熟悉度；如果当时项目只是课程项目用了 RabbitMQ，也可以坦诚，但要补“生产上我会这样比较”。',
            '线上一定要补幂等、重复消费、丢消息、积压、死信和监控，否则会显得只停留在 demo 层。',
        )
    else:
        answer = bullets(
            '后端基础题我会尽量落到真实业务：为什么引入缓存/MQ/限流，解决了什么瓶颈，带来了什么副作用。',
            '优秀候选人会把概念、工程实现和故障治理连起来答，而不是只背八股。',
        )
    plus = bullets('如果能结合自己项目中的 key/value 设计或监控指标，会很加分。', '回答时别忘了异常场景和治理。')
    avoid = bullets('不要只背“Redis 很快因为单线程”。', '不要说“当时只学了这个所以用了这个”然后就结束。')
    return answer, plus, avoid


def answer_model(question: str) -> tuple[list[str], list[str], list[str]]:
    q = question.lower()
    if 'temperature' in q or 'top-p' in q or 'top-k' in q:
        answer = bullets(
            'Temperature 本质上是在调节采样分布的平滑程度。温度越高，输出越发散；越低，输出越稳定、保守。',
            '所以它不是“越高越聪明”，而是多样性和稳定性的权衡。在事实问答、工具调用场景，我通常会把温度设低；在创意生成场景才会适当调高。',
            '如果继续追问，我会顺带解释 top-p、top-k：它们也是控制采样空间的方法，只是作用方式不同。',
        )
    elif 'kv cache' in q:
        answer = bullets(
            'KV Cache 缓存的是历史 token 在每层 self-attention 里对应的 Key 和 Value，这样自回归生成时就不用对历史部分重复计算。',
            '它能显著加速 decode 阶段，但代价是显存占用会随着序列长度增长，所以长上下文场景里显存管理很关键。',
            '优秀答法最好补一句：KV Cache 主要提升推理吞吐和延迟，不会改变模型能力本身。',
        )
    else:
        answer = bullets(
            '模型基础题我会坚持“概念 + 工程影响”一起答。比如讲 self-attention，不只说公式，而要说它为什么能建模长距离关系、为什么更利于并行。',
            '如果问 Transformer，我会覆盖 attention、前馈层、位置编码、残差与归一化；如果问采样，我会讲稳定性和多样性的 trade-off。',
        )
    plus = bullets('回答模型题时，别只背名词，补一层“这对线上效果意味着什么”。', '如果不确定某个细节，不要强编。')
    avoid = bullets('不要把 temperature 说成控制“创造力”的玄学参数。', '不要把 KV Cache 说成训练技巧。')
    return answer, plus, avoid


def answer_algorithm(question: str) -> tuple[list[str], list[str], list[str]]:
    q = question.lower()
    if '合并k个升序链表' in q:
        answer = bullets(
            '这题我会先给结论：用最小堆维护 k 个链表当前头结点，时间复杂度 O(N log k)，空间复杂度 O(k)。',
            '具体做法是先把每个非空链表头放入堆，每次弹出最小节点接到结果链表后面，再把它的 next 放回堆。',
            '如果面试官继续追问，我会补充分治合并的解法：两两合并，时间复杂度同样是 O(N log k)。',
        )
    elif '中位数' in q:
        answer = bullets(
            '如果数据量大到单机内存放不下，我会先说明是否允许多次扫描、是否允许外部排序。若允许离线处理，最稳的是分桶/外排序；若要求流式近似，可以用双堆或分位数近似算法。',
            '优秀答法重点不是背一个算法名，而是先确认数据规模、内存限制、是否精确、是否实时，然后给出合适方案。',
        )
    else:
        answer = bullets(
            '算法题我会先确认输入输出和边界，再先说思路和复杂度，最后再写代码。',
            '如果一开始没想到最优解，我也会先给可行解，再讲如何优化，这比一直沉默更像成熟候选人。',
            '写完后我会主动用样例和边界条件验证，包括空输入、重复值、极端长度等。',
        )
    plus = bullets('说复杂度时尽量顺带解释为什么是这个复杂度。', '边写边说关键不变量，很加分。')
    avoid = bullets('不要一上来就写代码。', '不要写完不测。')
    return answer, plus, avoid


def answer_default(question: str, topic: str) -> tuple[list[str], list[str], list[str]]:
    answer = bullets(
        f'这题我会按“结论 -> 关键拆分 -> 工程落地 -> 验证方式”来答，先把问题放回 {topic} 的核心目标里。',
        '面试里最重要的是别只给名词定义，要把适用边界、代价和失败处理讲出来。',
        '如果这题和你的项目相关，最好补一句“我在项目里是怎么做的，或者如果重做我会怎么做”。',
    )
    plus = bullets('尽量补指标、trade-off 和兜底方案。')
    avoid = bullets('不要把答案讲成百科解释。')
    return answer, plus, avoid


def answer_for(question: str, topic: str) -> tuple[list[str], list[str], list[str]]:
    topic = topic_from_question(question, topic)
    mapping = {
        '项目介绍/项目拷打': answer_project,
        'Agent 与 workflow/单多 Agent 选型': answer_agent,
        '记忆系统设计': answer_memory,
        'RAG 系统设计': answer_rag_system,
        '检索/召回/重排/向量索引优化': answer_retrieval,
        'RAG/Agent 评测与幻觉治理': answer_eval,
        'LangChain / LangGraph / 编排框架选型': answer_framework,
        'MCP / Function Calling / Skills / Tool Calling': answer_tools,
        '意图识别与 Query 理解': answer_intent,
        'AI Coding / Claude Code 实践': answer_ai_coding,
        '场景设计题（游戏/电商/安全/客服）': answer_scene,
        '后端基础：Redis/缓存/MQ/高并发': answer_backend,
        '模型基础：Transformer/KV Cache/Temperature': answer_model,
        '算法题/手撕题': answer_algorithm,
    }
    fn = mapping.get(topic)
    if not fn:
        return answer_default(question, topic)
    return fn(question)


def main() -> None:
    analysis = json.loads(ANALYSIS_JSON.read_text(encoding='utf-8'))
    grouped: dict[str, list[dict]] = {topic: [] for topic in TOPIC_ORDER}

    for fallback_topic, info in analysis['topic_summary'].items():
        topic = fallback_topic if fallback_topic in grouped else topic_from_question('', fallback_topic)
        if topic not in grouped:
            grouped[topic] = []
        for question, count in info['top_questions'][:6]:
            add_entry(grouped, topic_from_question(question, topic), question, count)

    entries = []
    for topic in TOPIC_ORDER:
        for item in grouped.get(topic, []):
            answer, plus, avoid = answer_for(item['question'], topic)
            entries.append({
                'topic': topic,
                'question': item['question'],
                'count': item['count'],
                'answer': answer,
                'plus': plus,
                'avoid': avoid,
            })

    md_lines = [
        '# 牛客近6个月AI应用开发面经：逐题优秀答案稿',
        '',
        '> 说明：这不是“标准答案”，而是适合优秀候选人的答题模板。重点是回答结构、工程取舍、评估与复盘意识。项目相关题请按你自己的真实经历替换占位信息，不要编造。',
        '',
        '## 优秀候选人的共性答法',
        '',
    ]
    md_lines.extend([f'- {item}' for item in STYLE_GUIDE])
    md_lines.extend(['', '## 逐题答案', ''])

    for topic in TOPIC_ORDER:
        topic_entries = [entry for entry in entries if entry['topic'] == topic]
        if not topic_entries:
            continue
        md_lines.extend([f'### {topic}', ''])
        for idx, entry in enumerate(topic_entries, start=1):
            md_lines.append(f'#### {idx}. {entry["question"]}')
            md_lines.append('')
            md_lines.append(f'- 命中次数：{entry["count"]}')
            md_lines.append('- 优秀答法：')
            for line in entry['answer']:
                md_lines.append(f'  - {line}')
            if entry['plus']:
                md_lines.append('- 加分点：')
                for line in entry['plus']:
                    md_lines.append(f'  - {line}')
            if entry['avoid']:
                md_lines.append('- 避坑：')
                for line in entry['avoid']:
                    md_lines.append(f'  - {line}')
            md_lines.append('')

    OUT_MD.write_text('\n'.join(md_lines).rstrip() + '\n', encoding='utf-8')
    OUT_JSON.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'md={OUT_MD}')
    print(f'json={OUT_JSON}')
    print(f'entries={len(entries)}')


if __name__ == '__main__':
    main()
