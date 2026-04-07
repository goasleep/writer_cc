# 📚 Obsidian 个人写作库系统设计方案

## 一、Vault 文件夹结构设计

### 推荐结构（PARA + Zettelkasten 混合）

```
📁 Writing-Vault/
│
├── 📁 00-Inbox/                    # 收件箱 - 临时存放待处理文章
│   └── 📄 待整理文章.md
│
├── 📁 01-Projects/                 # 项目 - 当前正在进行的写作项目
│   ├── 📁 项目A-技术博客系列/
│   │   ├── 📄 项目索引.md
│   │   ├── 📄 文章1-主题.md
│   │   └── 📄 文章2-主题.md
│   └── 📁 项目B-年度总结/
│       └── 📄 ...
│
├── 📁 02-Areas/                    # 领域 - 持续维护的主题领域
│   ├── 📁 技术/
│   │   ├── 📁 编程语言/
│   │   ├── 📁 框架工具/
│   │   └── 📁 架构设计/
│   ├── 📁 产品/
│   │   ├── 📁 用户研究/
│   │   ├── 📁 数据分析/
│   │   └── 📁 增长策略/
│   ├── 📁 行业观察/
│   │   ├── 📁 AI人工智能/
│   │   ├── 📁 区块链/
│   │   └── 📁 新能源/
│   └── 📁 个人成长/
│       ├── 📁 学习方法/
│       ├── 📁 时间管理/
│       └── 📁 思维模型/
│
├── 📁 03-Resources/                # 资源 - 参考素材和收藏文章
│   ├── 📁 文章收藏/
│   │   ├── 📁 按来源/
│   │   │   ├── 📁 微信公众号/
│   │   │   ├── 📁 知乎/
│   │   │   ├── 📁 掘金/
│   │   │   └── 📁 个人博客/
│   │   └── 📁 按日期/
│   │       ├── 📁 2024/
│   │       └── 📁 2025/
│   ├── 📁 书籍摘录/
│   ├── 📁 论文文献/
│   ├── 📁 视频笔记/
│   └── 📁 金句收集/
│
├── 📁 04-Archive/                  # 归档 - 已完成或暂停的项目
│   ├── 📁 2023项目/
│   └── 📁 2024项目/
│
├── 📁 05-System/                   # 系统文件
│   ├── 📁 Templates/               # 模板文件夹
│   │   ├── 📄 文章模板.md
│   │   ├── 📄 读书笔记模板.md
│   │   ├── 📄 项目索引模板.md
│   │   ├── 📄 每日笔记模板.md
│   │   └── 📄 MOC模板.md
│   ├── 📁 Scripts/                 # 自动化脚本
│   ├── 📁 Attachments/             # 附件资源
│   └── 📁 MOCs/                    # Map of Contents 索引地图
│       ├── 📄 MOC-技术.md
│       ├── 📄 MOC-产品.md
│       └── 📄 MOC-写作灵感.md
│
└── 📁 99-Daily/                    # 每日笔记（可选）
    ├── 📁 2024/
    └── 📁 2025/
```

---

## 二、标准化 Frontmatter 模板设计

### 2.1 基础文章模板

```markdown
---
# ===== 基础信息 =====
title: "文章标题"
aliases: ["别名1", "别名2"]
created: {{date:YYYY-MM-DD}}T{{time:HH:mm:ss}}
modified: {{date:YYYY-MM-DD}}T{{time:HH:mm:ss}}

# ===== 来源信息 =====
source: "原文链接或来源"
author: "原作者"
published: "2024-01-15"
source_type: "article"  # article | book | video | podcast | paper

# ===== 分类标签 =====
tags:
  - type/article      # 内容类型
  - status/processed  # 处理状态
  - topic/technology  # 主题分类
  - area/programming  # 领域分类

# ===== 元数据 =====
rating: 4            # 1-5 评分
importance: high     # high | medium | low
read_time: 15        # 预计阅读时间（分钟）
word_count: 3200     # 字数统计

# ===== 处理状态 =====
status: processed    # inbox | reading | processed | writing | published | archived

# ===== 关联项目 =====
project: "项目名称"
related:
  - "[[相关文章1]]"
  - "[[相关文章2]]"

# ===== 关键词 =====
keywords:
  - "关键词1"
  - "关键词2"

# ===== 摘要 =====
summary: "文章核心观点摘要（100字以内）"
---

# {{title}}

## 核心观点

## 详细笔记

## 个人思考

## 行动项
- [ ] 

## 参考资料
```

### 2.2 读书笔记模板

```markdown
---
title: "《书名》读书笔记"
aliases: []
created: {{date:YYYY-MM-DD}}
modified: {{date:YYYY-MM-DD}}

source: "《书名》"
author: "作者名"
published: "2023"
source_type: "book"

tags:
  - type/book-note
  - status/reading
  - topic/个人成长

rating: 5
status: reading
progress: 35  # 阅读进度 %

keywords:
  - "关键词1"
  - "关键词2"

summary: "本书核心观点"
---

# {{title}}

## 书籍信息
- **作者**: 
- **出版社**: 
- **阅读时间**: 
- **阅读方式**: 纸质书/电子书/听书

## 核心观点

## 章节笔记

## 金句摘录

## 实践应用

## 相关书籍
- [[另一本书]]
```

### 2.3 项目索引模板 (MOC)

```markdown
---
title: "MOC - 项目名称"
aliases: ["项目地图"]
created: {{date:YYYY-MM-DD}}
modified: {{date:YYYY-MM-DD}}

tags:
  - type/moc
  - status/active
  - project/项目名称

status: active
progress: 30
---

# {{title}}

## 项目概述
项目描述和目标...

## 进度追踪
- [x] 阶段1: 资料收集
- [ ] 阶段2: 大纲撰写 (进行中)
- [ ] 阶段3: 初稿完成
- [ ] 阶段4: 修改润色
- [ ] 阶段5: 发布

## 相关文章
```dataview
TABLE title, status, rating, modified
FROM "01-Projects/项目名称"
WHERE file.name != this.file.name
SORT modified DESC
```

## 参考资料
- [[相关文章1]]
- [[相关文章2]]

## 灵感收集
- 
```

### 2.4 每日笔记模板

```markdown
---
title: "{{date:YYYY-MM-DD}} 每日笔记"
date: {{date:YYYY-MM-DD}}
day: {{date:dddd}}
week: {{date:WW}}

tags:
  - type/daily
---

# {{title}}

## 今日聚焦
- [ ] 重要任务1
- [ ] 重要任务2

## 阅读记录
- 

## 写作灵感
- 

## 今日复盘
### 完成的事
### 学到的东西
### 明日计划

## 快速链接
- [[MOC-写作灵感]]
- [[项目索引]]
```

---

## 三、标签体系设计

### 3.1 标签分类架构

```
📌 标签体系总览

类型标签 (type/)
├── type/article        # 收藏文章
├── type/book-note      # 读书笔记
├── type/video-note     # 视频笔记
├── type/paper          # 论文文献
├── type/idea           # 灵感想法
├── type/moc            # 地图索引
├── type/daily          # 每日笔记
├── type/project        # 项目文件
└── type/template       # 模板文件

状态标签 (status/)
├── status/inbox        # 待处理
├── status/reading      # 阅读中
├── status/processed    # 已处理
├── status/writing      # 写作中
├── status/review       # 待复习
├── status/published    # 已发布
└── status/archived     # 已归档

主题标签 (topic/)
├── topic/technology    # 技术
├── topic/product       # 产品
├── topic/design        # 设计
├── topic/business      # 商业
├── topic/ai            # 人工智能
├── topic/blockchain    # 区块链
├── topic/growth        # 个人成长
├── topic/reading       # 阅读
└── topic/writing       # 写作

领域标签 (area/)
├── area/programming    # 编程
├── area/frontend       # 前端
├── area/backend        # 后端
├── area/devops         # 运维
├── area/data           # 数据
├── area/ux             # 用户体验
├── area/marketing      # 营销
└── area/management     # 管理

优先级标签 (priority/)
├── priority/high       # 高优先级
├── priority/medium     # 中优先级
└── priority/low        # 低优先级

来源标签 (source/)
├── source/wechat       # 微信公众号
├── source/zhihu        # 知乎
├── source/juejin       # 掘金
├── source/csdn         # CSDN
├── source/github       # GitHub
├── source/youtube      # YouTube
├── source/bilibili     # B站
└── source/podcast      # 播客
```

### 3.2 标签使用规则

| 规则 | 说明 | 示例 |
|------|------|------|
| 层级命名 | 使用 `/` 分隔层级 | `type/article` |
| 小写规范 | 全部使用小写字母 | `topic/technology` |
| 简洁明了 | 标签名不超过3个单词 | `area/frontend` |
| 组合使用 | 每篇文章2-4个标签 | 类型+状态+主题 |
| 定期整理 | 每月检查标签使用情况 | 合并相似标签 |

---

## 四、双向链接使用策略

### 4.1 链接类型与使用场景

```markdown
## 链接类型

### 1. 概念链接 [[概念名]]
- 链接到核心概念笔记
- 示例: [[Obsidian]], [[Zettelkasten]], [[复利效应]]

### 2. 文章链接 [[文章标题]]
- 链接到具体文章
- 示例: [[如何构建知识体系]]

### 3. MOC链接 [[MOC-主题]]
- 链接到主题地图
- 示例: [[MOC-技术]], [[MOC-产品]]

### 4. 日期链接 [[YYYY-MM-DD]]
- 链接到每日笔记
- 示例: [[2024-01-15]]

### 5. 块链接 [[文章标题#^块ID]]
- 链接到具体段落
- 示例: [[如何构建知识体系#^核心观点]]
```

### 4.2 链接建立策略

| 策略 | 说明 | 示例 |
|------|------|------|
| **概念原子化** | 核心概念单独成文 | `[[复利效应]]` 作为独立笔记 |
| **MOC导航** | 用MOC聚合相关笔记 | `[[MOC-写作]]` 汇总所有写作相关 |
| **上下文链接** | 在相关内容处添加链接 | "这类似于[[复利效应]]的原理" |
| **索引链接** | 在笔记底部添加相关链接 | ## 相关笔记 |
| **反向链接利用** | 查看哪些笔记链接到当前 | 使用 backlinks 面板 |

### 4.3 链接维护最佳实践

```markdown
## 每篇文章底部的标准格式

---

## 相关笔记
- [[相关概念1]]
- [[相关文章2]]
- [[MOC-所属主题]]

## 引用来源
- [原文链接](url)

## 更新记录
- {{date:YYYY-MM-DD}}: 创建
- {{date:YYYY-MM-DD}}: 补充XX内容
```

---

## 五、元数据分析方法（Dataview）

### 5.1 基础查询示例

```dataview
// 列出所有未处理的文章
TABLE title, source, rating, created
FROM "03-Resources"
WHERE status = "inbox"
SORT created DESC
```

```dataview
// 按主题统计文章数量
TABLE length(rows) as "文章数"
FROM "03-Resources"
GROUP BY topic
```

```dataview
// 高评分文章列表
TABLE title, rating, summary
FROM "03-Resources"
WHERE rating >= 4
SORT rating DESC
```

### 5.2 进阶查询

```dataview
// 项目进度追踪
TABLE without id
  file.link as "文章",
  status as "状态",
  progress as "进度%",
  rating as "评分"
FROM "01-Projects"
WHERE file.folder != "01-Projects"
SORT progress DESC
```

```dataview
// 按月份统计阅读量
TABLE without id
  dateformat(created, "yyyy-MM") as "月份",
  length(rows) as "文章数",
  sum(rows.word_count) as "总字数"
FROM "03-Resources"
GROUP BY dateformat(created, "yyyy-MM")
SORT dateformat(created, "yyyy-MM") DESC
```

```dataview
// 标签使用情况统计
TABLE without id
  tags as "标签",
  length(rows) as "使用次数"
FROM ""
FLATTEN tags
GROUP BY tags
SORT length(rows) DESC
LIMIT 20
```

### 5.3 仪表盘页面

创建一个 `05-System/仪表盘.md` 文件：

```markdown
---
title: "写作库仪表盘"
tags: [type/dashboard]
---

# 写作库仪表盘

## 统计概览

| 指标 | 数值 |
|------|------|
| 总文章数 | `=length([[]])` |
| 本周新增 | `=length(filter([[]], (f) => dateformat(f.created, "yyyy-WW") = dateformat(date(now), "yyyy-WW")))` |
| 待处理 | `=length(filter([[]], (f) => f.status = "inbox"))` |
| 高评分 | `=length(filter([[]], (f) => f.rating >= 4))` |

## 最近添加
```dataview
TABLE title, source, created
FROM "03-Resources"
SORT created DESC
LIMIT 10
```

## 待处理文章
```dataview
TABLE title, source, created
FROM "03-Resources"
WHERE status = "inbox"
SORT created ASC
```

## 热门主题
```dataview
TABLE without id
  tags as "标签",
  length(rows) as "数量"
FROM "03-Resources"
FLATTEN tags
WHERE contains(tags, "topic/")
GROUP BY tags
SORT length(rows) DESC
LIMIT 10
```
```

---

## 六、检索与发现机制

### 6.1 快速检索方法

| 方法 | 操作 | 适用场景 |
|------|------|----------|
| **快速切换** | `Ctrl/Cmd + O` | 按文件名搜索 |
| **全局搜索** | `Ctrl/Cmd + Shift + F` | 全文搜索 |
| **标签搜索** | `#tag` | 按标签筛选 |
| **图谱浏览** | `Ctrl/Cmd + G` | 可视化探索 |
| **反向链接** | 右侧面板 | 查看关联笔记 |

### 6.2 搜索语法

```markdown
// 基础搜索
keyword                    # 包含关键词
"exact phrase"            # 精确短语

// 标签搜索
tag:#topic/technology     # 特定标签
tag:topic/tech*           # 标签通配符

// 属性搜索
rating:4                  # 评分等于4
rating:>3                 # 评分大于3
status:processed          # 特定状态

// 组合搜索
keyword tag:#article      # 关键词+标签
status:inbox OR status:reading  # 或条件
status:processed AND rating:>3  # 与条件

// 路径搜索
path:"03-Resources"       # 特定文件夹
file:"README"             # 文件名
```

### 6.3 发现机制设计

```markdown
## 随机发现
- 使用 Random Note 插件
- 每日浏览图谱中的孤立节点

## 主题探索
- 通过 MOC 页面系统浏览
- 使用 Local Graph 查看关联

## 时间线浏览
- 查看每日笔记的时间线
- 按创建/修改时间排序

## 未链接提及
- 使用 Unlinked Mentions 发现潜在链接
- 定期清理孤儿笔记
```

---

## 七、推荐插件清单

### 7.1 核心插件（必装）

| 插件名 | 功能 | 用途 |
|--------|------|------|
| **Dataview** | 数据库查询 | 元数据分析、仪表盘 |
| **Templater** | 模板引擎 | 自动化模板填充 |
| **Tag Wrangler** | 标签管理 | 批量修改标签 |
| **Graph Analysis** | 图谱分析 | 发现笔记关联 |

### 7.2 效率插件（推荐）

| 插件名 | 功能 | 用途 |
|--------|------|------|
| **QuickAdd** | 快速添加 | 一键创建笔记 |
| **Periodic Notes** | 周期性笔记 | 日记/周记/月记 |
| **Readwise Official** | 阅读同步 | 同步阅读高亮 |
| **Obsidian Git** | Git备份 | 版本控制 |
| **Excalidraw** | 手绘图表 | 可视化思考 |

### 7.3 辅助插件（可选）

| 插件名 | 功能 | 用途 |
|--------|------|------|
| **Supercharged Links** | 链接增强 | 自定义链接样式 |
| **Breadcrumbs** | 面包屑导航 | 层级导航 |
| **Homepage** | 首页设置 | 自定义启动页 |
| **Style Settings** | 样式设置 | 主题自定义 |

---

## 八、工作流示例

### 8.1 文章收集工作流

```
1. 发现好文章 → 保存到 00-Inbox/
2. 使用模板创建笔记 → 填充基础信息
3. 阅读并做笔记 → 更新 status: reading → processed
4. 添加标签和链接 → 建立知识关联
5. 移动到对应主题文件夹 → 03-Resources/主题/
6. 更新 MOC → 在主题地图中添加链接
```

### 8.2 写作项目工作流

```
1. 创建项目文件夹 → 01-Projects/项目名/
2. 创建项目 MOC → 使用项目索引模板
3. 收集参考资料 → 链接到相关文章
4. 撰写文章 → 使用文章模板
5. 定期回顾 → 更新进度和状态
6. 项目完成 → 移动到 04-Archive/
```

---

## 九、文件清单

本方案包含以下文件：

| 文件路径 | 说明 |
|----------|------|
| `05-System/Templates/文章模板.md` | 基础文章模板 |
| `05-System/Templates/读书笔记模板.md` | 书籍笔记模板 |
| `05-System/Templates/项目索引模板.md` | MOC模板 |
| `05-System/Templates/每日笔记模板.md` | 日记模板 |
| `05-System/MOCs/MOC-技术.md` | 技术主题地图 |
| `05-System/MOCs/MOC-产品.md` | 产品主题地图 |
| `05-System/仪表盘.md` | 数据仪表盘 |

---

## 十、最佳实践总结

1. **定期整理**: 每周清理 Inbox，每月整理标签
2. **链接优先**: 多用双向链接，少用文件夹层级
3. **原子笔记**: 一个笔记一个主题，便于复用
4. **MOC导航**: 用地图页面组织主题内容
5. **数据驱动**: 用 Dataview 监控知识库健康度
6. **持续迭代**: 根据使用习惯调整结构和标签

---

## 与 Claude Code 集成

本 Vault 已配置 `.claude/CLAUDE.md`，定义了可直接使用的命令：

| 命令 | 说明 |
|------|------|
| `/collect <url>` | 采集文章到 `00-Inbox/` |
| `/batch <file>` | 批量采集 |
| `/inbox` | 查看收件箱状态 |
| `/imitate` | 启动仿写工作流 |
| `/moc` | 更新主题地图 |
| `/clean <file>` | 清理 Markdown 格式 |

Python 工具源码位于 `src/writer_tools/`，使用 `uv` 管理依赖。
