# 牛客近6个月AI应用开发面经：公司维度对比分析

- 统计公司数：16

## 公司总览

| 公司 | 面经数 | 高频知识点 | 风格提示 |
|---|---:|---|---|
| 字节 | 7 | Agent架构与范式、RAG与检索优化、记忆与上下文管理 | 项目细节会深挖到记忆、评测、数据集、并发隔离，常伴随模型基础或算法题。 |
| 淘天 | 4 | Agent架构与范式、框架、MCP与工具调用、评测、幻觉与数据集 | 偏 Agent 范式、记忆设计、RAG 优化和业务场景落地，也会问实验与成本。 |
| 快手 | 4 | 算法与编码题、后端基础与工程化、Agent架构与范式 | AI 应用 + 后端八股混合考，Redis/MQ/框架选型比重高。 |
| 腾讯 | 3 | 后端基础与工程化、算法与编码题、记忆与上下文管理 | 偏应用架构与工程实现，常问记忆、Skill/MCP、状态机、LangChain/LangGraph。 |
| 蚂蚁 | 2 | 框架、MCP与工具调用、项目介绍与项目拷打、RAG与检索优化 | 偏 RAG 细节、重排、幻觉、采样参数和项目追问。 |
| 阿里国际 | 2 | 后端基础与工程化、算法与编码题、AI Coding与协作方式 | 除了 AI 应用本身，还会穿插 Python/计网/操作系统等通用基础。 |
| 小红书 | 1 | 项目介绍与项目拷打、Agent架构与范式、框架、MCP与工具调用 | Agent / RAG / 向量索引问得系统，喜欢考概念边界与检索细节。 |
| 阿里云 | 1 | 项目介绍与项目拷打、业务场景设计、RAG与检索优化 | 偏场景系统设计和高风险场景治理，重视 RAG 评测与幻觉控制。 |
| 高德 | 1 | 项目介绍与项目拷打、前端与跨端工程、后端基础与工程化 | 偏跨端工程与 AI Coding 协作方式，也会问 Agent skill 拆分。 |
| 京东 | 1 | 项目介绍与项目拷打、Agent架构与范式、评测、幻觉与数据集 | 重 workflow、RAG、意图识别和电商业务场景，兼顾缓存与压测。 |
| 阿里灵犀互娱 | 1 | AI Coding与协作方式、业务场景设计、评测、幻觉与数据集 | 强业务场景题，尤其游戏客服/游戏助手/多 Agent 设计。 |
| 金山云 | 1 | 项目介绍与项目拷打、后端基础与工程化、RAG与检索优化 | 以具体项目深挖为主，建议按该公司的高频知识点准备。 |
| 阿里淘天 | 1 | 记忆与上下文管理、Agent架构与范式、AI Coding与协作方式 | 以具体项目深挖为主，建议按该公司的高频知识点准备。 |
| 米哈游 | 1 | 项目介绍与项目拷打、模型基础与推理机制、Agent架构与范式 | 偏游戏场景下的 Agent 设计、状态定义与记忆管理。 |
| 百度 | 1 | Agent架构与范式、记忆与上下文管理、评测、幻觉与数据集 | 偏 Agent 项目深挖，关注规划、记忆、工具调用和评测。 |
| 蔚来 | 1 | 后端基础与工程化、RAG与检索优化、算法与编码题 | 更偏服务端基础 + AI 应用结合。 |

## 逐公司分析

### 字节

- 面经数：7
- 风格画像：项目细节会深挖到记忆、评测、数据集、并发隔离，常伴随模型基础或算法题。
- 高频知识点：
  - Agent架构与范式: 7
  - RAG与检索优化: 7
  - 记忆与上下文管理: 6
  - 框架、MCP与工具调用: 6
  - 模型基础与推理机制: 6
  - 算法与编码题: 6
- 高频题型：
  - RAG/Agent 评测与幻觉治理: 6
  - 检索/召回/重排/向量索引优化: 6
  - 算法题/手撕题: 6
  - 模型基础：Transformer/KV Cache/Temperature: 5
  - 记忆系统设计: 4
  - MCP / Function Calling / Skills / Tool Calling: 4
- 相关面经：
  - 2026-04-10｜[字节 剪映 ai应用开发](https://www.nowcoder.com/feed/main/detail/2e53f0ec451a4e71b2e3418252071ba4)
  - 2026-04-09｜[字节agent开发实习一面凉经](https://www.nowcoder.com/feed/main/detail/69b9cd21f1244d3cb19499f249228b50)
  - 2026-04-09｜[字节Agent开发一面90min凉经](https://www.nowcoder.com/feed/main/detail/91c5394e57c14927841d7a86bfe427c2)
  - 2026-04-08｜[AI应用开发日常实习二面-字节](https://www.nowcoder.com/feed/main/detail/0607316a2492400896408c95e10951e0)
  - 2026-04-08｜[字节AI应用开发实习面经分享](https://www.nowcoder.com/feed/main/detail/76448605da6e4aee99a394da83d1718f)
  - 2026-04-02｜[字节 ai应用开发](https://www.nowcoder.com/feed/main/detail/c5947496fc29440883611173478dc257)
  - 2026-03-21｜[字节 大模型应用开发 二面 日常实习](https://www.nowcoder.com/feed/main/detail/30b6f37830414df5a32d851f2004df7a)

### 淘天

- 面经数：4
- 风格画像：偏 Agent 范式、记忆设计、RAG 优化和业务场景落地，也会问实验与成本。
- 高频知识点：
  - Agent架构与范式: 4
  - 框架、MCP与工具调用: 4
  - 评测、幻觉与数据集: 3
  - 记忆与上下文管理: 2
  - 项目介绍与项目拷打: 2
  - RAG与检索优化: 2
- 高频题型：
  - LangChain / LangGraph / 编排框架选型: 3
  - RAG/Agent 评测与幻觉治理: 3
  - MCP / Function Calling / Skills / Tool Calling: 3
  - Agent 与 workflow/单多 Agent 选型: 2
  - 场景设计题（游戏/电商/安全/客服）: 2
  - 项目介绍/项目拷打: 2
- 相关面经：
  - 2026-04-12｜[淘天 AI应用开发 二面](https://www.nowcoder.com/discuss/872816572199464960)
  - 2026-04-10｜[淘天AI应用开发 agent岗一面 好难](https://www.nowcoder.com/feed/main/detail/a0306a045d594b02b63fb0654d517901)
  - 2026-04-09｜[4.9-淘天agent-二面](https://www.nowcoder.com/discuss/871774510138023936)
  - 2026-04-03｜[淘天-ai应用开发-一面](https://www.nowcoder.com/feed/main/detail/076a8d1acaae4795a28d4a5370872bd6)

### 快手

- 面经数：4
- 风格画像：AI 应用 + 后端八股混合考，Redis/MQ/框架选型比重高。
- 高频知识点：
  - 算法与编码题: 4
  - 后端基础与工程化: 3
  - Agent架构与范式: 3
  - 框架、MCP与工具调用: 2
  - 记忆与上下文管理: 2
  - 业务场景设计: 2
- 高频题型：
  - 算法题/手撕题: 4
  - 后端基础：Redis/缓存/MQ/高并发: 2
  - 记忆系统设计: 2
  - 场景设计题（游戏/电商/安全/客服）: 2
  - LangChain / LangGraph / 编排框架选型: 1
  - 项目介绍/项目拷打: 1
- 相关面经：
  - 2026-04-11｜[快手ai应用服务端开发 二面](https://www.nowcoder.com/discuss/872512773710696448)
  - 2026-04-10｜[快手 AI agent开发二面分享 1h](https://www.nowcoder.com/feed/main/detail/afa98a916503444aa708fcfffb263d38)
  - 2026-04-09｜[快手AI Agent开发一面（已过）](https://www.nowcoder.com/feed/main/detail/7ce89f19368b46da853c718f2ae2f53c)
  - 2026-04-08｜[实习-快手电商-大模型数据应用开发一面](https://www.nowcoder.com/discuss/871506086656761856)

### 腾讯

- 面经数：3
- 风格画像：偏应用架构与工程实现，常问记忆、Skill/MCP、状态机、LangChain/LangGraph。
- 高频知识点：
  - 后端基础与工程化: 3
  - 算法与编码题: 3
  - 记忆与上下文管理: 2
  - Agent架构与范式: 2
  - RAG与检索优化: 2
  - 框架、MCP与工具调用: 1
- 高频题型：
  - 算法题/手撕题: 3
  - 记忆系统设计: 2
  - LangChain / LangGraph / 编排框架选型: 1
  - MCP / Function Calling / Skills / Tool Calling: 1
  - AI Coding / Claude Code 实践: 1
  - 检索/召回/重排/向量索引优化: 1
- 相关面经：
  - 2026-04-10｜[腾讯 AI应用开发面经](https://www.nowcoder.com/feed/main/detail/acd3e53eecbc405296335edae4d5cf88)
  - 2026-04-09｜[腾讯日常实习一面-AI应用开发 1h](https://www.nowcoder.com/feed/main/detail/37e847fa267b4c3898b38e2952b5286e)
  - 2026-04-09｜[腾讯暑期实习 ai agent开发一面](https://www.nowcoder.com/feed/main/detail/497e14617f01453db84dfbc264e5751e)

### 蚂蚁

- 面经数：2
- 风格画像：偏 RAG 细节、重排、幻觉、采样参数和项目追问。
- 高频知识点：
  - 框架、MCP与工具调用: 2
  - 项目介绍与项目拷打: 1
  - RAG与检索优化: 1
  - 记忆与上下文管理: 1
  - 评测、幻觉与数据集: 1
  - 模型基础与推理机制: 1
- 高频题型：
  - 项目介绍/项目拷打: 1
  - 检索/召回/重排/向量索引优化: 1
  - RAG/Agent 评测与幻觉治理: 1
  - 模型基础：Transformer/KV Cache/Temperature: 1
  - LangChain / LangGraph / 编排框架选型: 1
  - 算法题/手撕题: 1
- 相关面经：
  - 2026-04-10｜[蚂蚁金融Agent开发暑期面经分享](https://www.nowcoder.com/feed/main/detail/1f90384e8ff54172b65b50d853b00da0)
  - 2026-04-05｜[蚂蚁ai应用开发实习二面](https://www.nowcoder.com/feed/main/detail/718c5a06a65645d7a462a56b457cb35e)

### 阿里国际

- 面经数：2
- 风格画像：除了 AI 应用本身，还会穿插 Python/计网/操作系统等通用基础。
- 高频知识点：
  - 后端基础与工程化: 1
  - 算法与编码题: 1
  - AI Coding与协作方式: 1
  - 框架、MCP与工具调用: 1
  - 业务场景设计: 1
- 高频题型：
  - 算法题/手撕题: 1
  - 后端基础：Redis/缓存/MQ/高并发: 1
  - AI Coding / Claude Code 实践: 1
  - MCP / Function Calling / Skills / Tool Calling: 1
- 相关面经：
  - 2026-04-10｜[阿里国际AI应用开发暑期一面 1h](https://www.nowcoder.com/feed/main/detail/580e5a35eddb47e0851952165004f233)
  - 2026-04-09｜[阿里国际AI应用开发二面](https://www.nowcoder.com/feed/main/detail/c2772ead209549a0bb6e54f2df205a31)

### 小红书

- 面经数：1
- 风格画像：Agent / RAG / 向量索引问得系统，喜欢考概念边界与检索细节。
- 高频知识点：
  - 项目介绍与项目拷打: 1
  - Agent架构与范式: 1
  - 框架、MCP与工具调用: 1
  - 记忆与上下文管理: 1
  - RAG与检索优化: 1
- 高频题型：
  - 项目介绍/项目拷打: 1
  - Agent 与 workflow/单多 Agent 选型: 1
  - MCP / Function Calling / Skills / Tool Calling: 1
  - 记忆系统设计: 1
  - RAG 系统设计: 1
  - 检索/召回/重排/向量索引优化: 1
- 相关面经：
  - 2026-04-12｜[小红书 AI Agent开发 一面](https://www.nowcoder.com/discuss/872820735335485440)

### 阿里云

- 面经数：1
- 风格画像：偏场景系统设计和高风险场景治理，重视 RAG 评测与幻觉控制。
- 高频知识点：
  - 项目介绍与项目拷打: 1
  - 业务场景设计: 1
  - RAG与检索优化: 1
  - 评测、幻觉与数据集: 1
  - Agent架构与范式: 1
  - 前端与跨端工程: 1
- 高频题型：
  - 项目介绍/项目拷打: 1
  - 场景设计题（游戏/电商/安全/客服）: 1
  - RAG 系统设计: 1
  - RAG/Agent 评测与幻觉治理: 1
- 相关面经：
  - 2026-04-12｜[阿里云 AI应用开发 一面](https://www.nowcoder.com/discuss/872810222128021504)

### 高德

- 面经数：1
- 风格画像：偏跨端工程与 AI Coding 协作方式，也会问 Agent skill 拆分。
- 高频知识点：
  - 项目介绍与项目拷打: 1
  - 前端与跨端工程: 1
  - 后端基础与工程化: 1
  - Agent架构与范式: 1
  - AI Coding与协作方式: 1
  - 模型基础与推理机制: 1
- 高频题型：
  - 项目介绍/项目拷打: 1
  - 检索/召回/重排/向量索引优化: 1
  - MCP / Function Calling / Skills / Tool Calling: 1
  - AI Coding / Claude Code 实践: 1
- 相关面经：
  - 2026-04-10｜[高德 AI应用开发 一面](https://www.nowcoder.com/discuss/872229606252675072)

### 京东

- 面经数：1
- 风格画像：重 workflow、RAG、意图识别和电商业务场景，兼顾缓存与压测。
- 高频知识点：
  - 项目介绍与项目拷打: 1
  - Agent架构与范式: 1
  - 评测、幻觉与数据集: 1
  - RAG与检索优化: 1
  - 后端基础与工程化: 1
  - 业务场景设计: 1
- 高频题型：
  - 项目介绍/项目拷打: 1
  - Agent 与 workflow/单多 Agent 选型: 1
  - RAG 系统设计: 1
  - RAG/Agent 评测与幻觉治理: 1
  - 意图识别与 Query 理解: 1
  - 检索/召回/重排/向量索引优化: 1
- 相关面经：
  - 2026-04-10｜[27暑期实习-京东Agent开发二面分享](https://www.nowcoder.com/feed/main/detail/6af1c8611e434bbe8ba9cfa2bd0eaf18)

### 阿里灵犀互娱

- 面经数：1
- 风格画像：强业务场景题，尤其游戏客服/游戏助手/多 Agent 设计。
- 高频知识点：
  - AI Coding与协作方式: 1
  - 业务场景设计: 1
  - 评测、幻觉与数据集: 1
  - Agent架构与范式: 1
  - 记忆与上下文管理: 1
- 高频题型：
  - AI Coding / Claude Code 实践: 1
  - 场景设计题（游戏/电商/安全/客服）: 1
  - RAG/Agent 评测与幻觉治理: 1
  - 意图识别与 Query 理解: 1
  - Agent 与 workflow/单多 Agent 选型: 1
  - 记忆系统设计: 1
- 相关面经：
  - 2026-04-10｜[阿里灵犀互娱AI应用开发暑期二面](https://www.nowcoder.com/feed/main/detail/3dbec664147348d685f3e2b8b50288f8)

### 金山云

- 面经数：1
- 风格画像：以具体项目深挖为主，建议按该公司的高频知识点准备。
- 高频知识点：
  - 项目介绍与项目拷打: 1
  - 后端基础与工程化: 1
  - RAG与检索优化: 1
  - AI Coding与协作方式: 1
  - 框架、MCP与工具调用: 1
- 高频题型：
  - 项目介绍/项目拷打: 1
  - 后端基础：Redis/缓存/MQ/高并发: 1
  - 检索/召回/重排/向量索引优化: 1
  - RAG/Agent 评测与幻觉治理: 1
  - AI Coding / Claude Code 实践: 1
  - MCP / Function Calling / Skills / Tool Calling: 1
- 相关面经：
  - 2026-04-10｜[27届-日常实习-金山云-AI应用平台开发-一面](https://www.nowcoder.com/discuss/872055401926164480)

### 阿里淘天

- 面经数：1
- 风格画像：以具体项目深挖为主，建议按该公司的高频知识点准备。
- 高频知识点：
  - 记忆与上下文管理: 1
  - Agent架构与范式: 1
  - AI Coding与协作方式: 1
- 高频题型：
  - Agent 与 workflow/单多 Agent 选型: 1
  - AI Coding / Claude Code 实践: 1
  - 算法题/手撕题: 1
- 相关面经：
  - 2026-04-09｜[阿里淘天 AI应用开发 暑期实习一面](https://www.nowcoder.com/feed/main/detail/39627b379e8e46ce9cb3a3b8eae46959)

### 米哈游

- 面经数：1
- 风格画像：偏游戏场景下的 Agent 设计、状态定义与记忆管理。
- 高频知识点：
  - 项目介绍与项目拷打: 1
  - 模型基础与推理机制: 1
  - Agent架构与范式: 1
  - 记忆与上下文管理: 1
  - 框架、MCP与工具调用: 1
  - 算法与编码题: 1
- 高频题型：
  - 项目介绍/项目拷打: 1
  - 模型基础：Transformer/KV Cache/Temperature: 1
  - Agent 与 workflow/单多 Agent 选型: 1
  - 记忆系统设计: 1
  - MCP / Function Calling / Skills / Tool Calling: 1
  - 算法题/手撕题: 1
- 相关面经：
  - 2026-04-09｜[米哈游-AI Agent研发-暑期一面](https://www.nowcoder.com/feed/main/detail/a1566acc2660477dbf54b58885513d6c)

### 百度

- 面经数：1
- 风格画像：偏 Agent 项目深挖，关注规划、记忆、工具调用和评测。
- 高频知识点：
  - Agent架构与范式: 1
  - 记忆与上下文管理: 1
  - 评测、幻觉与数据集: 1
  - 模型基础与推理机制: 1
  - 后端基础与工程化: 1
- 高频题型：
  - RAG/Agent 评测与幻觉治理: 1
  - 模型基础：Transformer/KV Cache/Temperature: 1
- 相关面经：
  - 2026-04-09｜[百度ai agent开发春招一面](https://www.nowcoder.com/feed/main/detail/c807140b75bd4cf3bf4166660676db5d)

### 蔚来

- 面经数：1
- 风格画像：更偏服务端基础 + AI 应用结合。
- 高频知识点：
  - 后端基础与工程化: 1
  - RAG与检索优化: 1
  - 算法与编码题: 1
- 高频题型：
  - 后端基础：Redis/缓存/MQ/高并发: 1
  - 检索/召回/重排/向量索引优化: 1
  - 算法题/手撕题: 1
- 相关面经：
  - 2026-04-09｜[蔚来 AI应用开发 暑期一面分享](https://www.nowcoder.com/feed/main/detail/5af31c8afe254a00a69a6c0141e6908a)

