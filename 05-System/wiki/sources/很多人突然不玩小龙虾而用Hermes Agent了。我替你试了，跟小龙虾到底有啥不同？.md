---
type: source
title: "很多人突然不玩小龙虾而用Hermes Agent了。我替你试了，跟小龙虾到底有啥不同？"
source_url: "https://mp.weixin.qq.com/s?__biz=Mzk0NzQzOTczOA==&mid=2247523977&idx=1&sn=51f95a0e3ffea44cf91c9cd086ff0337&chksm=c2996b520b31a2bb300a1316f277a59434c947fe2b68f9dabd1fca0ebf0d1a18bffe2d1f5cb4&mpshare=1&scene=1&srcid=0409HFGsDPOJjCi4J6rxjCUZ&sharer_shareinfo=5ab6cf21d7de0a1d92c6b9ef4bf1c331&sharer_shareinfo_first=634ff1f2bf36f76b5754f6681c4a4cb9"
collected_at: "2026-04-11"
author: "AI范儿"
platform: "微信公众号"
tags: ["AI工具", "产品测评", "技术对比"]
---

# 很多人突然不玩小龙虾而用Hermes Agent了。我替你试了，跟小龙虾到底有啥不同？

## 核心论点

这是一篇关于两个开源 AI 助理工具（OpenClaw/小龙虾 vs Hermes Agent）的对比测评文章。作者通过亲身测试，从安装、功能、技术架构、安全性等多个维度进行了对比分析。

核心观点：
- **OpenClaw**："你来指挥的系统"，强调用户控制权
- **Hermes Agent**："自己会长大的助手"，强调 AI 自学习
- 两者的差异不在"有没有"功能，而在"怎么做"

## 主要发现

### 技术架构差异

1. **Skills 机制**
   - OpenClaw：人工编写的 Markdown 文件（5700+ 社区贡献）
   - Hermes：程序性记忆，完成复杂任务后自动提炼成 Skill，后续自动优化

2. **记忆系统**
   - OpenClaw：MEMORY.md + 每日笔记（Markdown，透明可编辑）
   - Hermes：三层结构（MEMORY.md 环境信息 + USER.md 用户偏好 + Session Search 全文检索）

3. **安全机制**
   - OpenClaw：依赖模型判断力
   - Hermes：框架级安全（授权审批、安全扫描、容器隔离、凭证泄露拦截）

### 生态现状

- Hermes：GitHub 两个月 3 万星，文档优秀，slash 命令丰富（类似 Claude Code）
- OpenClaw：社区更大，但文档零碎

## 关键洞察

文章最后提出了一个值得思考的产品哲学分歧：

> "AI 助理的终极形态不是'更聪明'，而是'不需要你重复说第二遍'。"

这个分歧可能决定 AI 助理这个品类最终长成什么样：
- **控制派**：给用户最大的控制权，人来指挥，AI 来执行
- **自学派**：让 AI 自己学会怎么干活，人只需要说一次

## 实用建议

作者针对不同用户群体给出了差异化建议：
- **已入坑 OpenClaw 的**：别急着搬家，但值得试试
- **未入坑的**：建议先试 Hermes（上手更简单，文档更友好）
- **喜欢 Claude Code 的**：强烈建议入坑 Hermes（slash 命令体验相似）
- **技术底子好的**：两个都装，各取所长

## 相关实体

- [[Hermes Agent]]
- [[OpenClaw]]
- [[Nous Research]]
- [[Claude]]

## 相关概念

- [[AI Agent]]
- [[AI 助理]]
- [[程序性记忆]]
- [[安全扫描]]
- [[容器隔离]]
