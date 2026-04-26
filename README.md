# 个人写作库系统

> 一个以 **Obsidian Vault** 为核心，由 **Claude Code** 驱动的个人写作库。
> **你的入口只有 Claude Code 和 Obsidian。所有工具操作，交给 Claude Code。**

---

## 快速开始

1. 在 Claude Code 中打开本目录
2. 在 Obsidian 中将 `writer_cc/` 作为 Vault 打开
3. 直接对话：
   - `"采集 https://example.com/article"`
   - `"帮我整理一下收件箱"`
   - `"我想仿写这篇文章，主题是..."`
   - `"看看今天的 MOC 需要更新吗"`

---

## 系统架构

```
┌──────────────────────────────────────────────────────────────┐
│                        个人写作库系统                         │
├────────────────────┬───────────────────┬─────────────────────┤
│     文章收集        │     知识落库       │      仿写创作        │
├────────────────────┼───────────────────┼─────────────────────┤
│ 你: "采集这篇文章"  │ 你: Obsidian      │ 你: "仿写这篇文章"   │
│ ↓                  │ ↓                 │ ↓                   │
│ Claude Code        │ 阅读、链接、写作   │ Claude Code         │
│ ↓                  │                   │ ↓                   │
│ 自动调用 Python工具 │                   │ 三维分析 + 生成初稿 │
│ ↓                  │                   │ ↓                   │
│ raw/articles/      │ 03-Resources/     │ 01-Projects/        │
│ 05-System/wiki/    │                   │                     │
└────────────────────┴───────────────────┴─────────────────────┘
```

**关键原则：**
- 你不用记任何 CLI 命令
- Python 工具**只由 Claude Code 自动调用**
- 你只在 Obsidian 中阅读和写作

---

## Claude Code 命令

| 命令 | 作用 |
|------|------|
| `/collect <url>` | 采集文章到 `raw/articles/`，自动更新 wiki |
| `/batch <file>` | 批量采集文章 |
| `/query <问题>` | 搜索 wiki 并沉淀答案 |
| `/lint` | 检查并修复 wiki 健康度 |
| `/imitate` | 参考文章仿写 |
| `/moc` | 查看/更新主题地图 |
| `/clean <file>` | 清理 Markdown 格式 |

详细工作指令见：`.claude/CLAUDE.md`

---

## Vault 目录结构

```
writer_cc/                    # ← 本目录即 Obsidian Vault
├── 00-Inbox/                 # 已废弃（待迁移清空）
├── 01-Projects/              # 进行中的写作项目
├── 02-Areas/                 # 持续维护的领域知识
├── 03-Resources/             # 手写笔记、读书笔记、金句
├── 04-Archive/               # 归档项目
├── 05-System/
│   ├── Templates/            # Obsidian 模板
│   ├── MOCs/                 # 主题地图
│   ├── wiki/                 # LLM 维护的 wiki 知识网络
│   └── 仪表盘.md             # Dataview 仪表盘
├── 99-Daily/                 # 每日笔记
├── raw/                      # 精修后的原文层（immutable）
│   └── articles/
├── docs/                     # 详细文档
├── src/writer_tools/         # Python 工具源码（Claude Code 专用）
├── .claude/                  # Claude Code 配置
│   └── CLAUDE.md             # 工作指令
└── pyproject.toml            # 工具依赖配置
```

---

## LLM Wiki 架构

Vault 采用双层架构：

- **`raw/`** — 精修原文层，LLM 写入后 immutable
- **`05-System/wiki/`** — LLM 全权维护的知识网络层（sources / entities / concepts / queries / index / log）
- **`03-Resources/`** — 人类手写笔记层，LLM 不自动修改

> 每次 `/collect` 会自动触发 wiki ingest 全流程。

---

## 文档索引

| 文档 | 路径 | 说明 |
|------|------|------|
| Vault 设置指南 | `docs/vault_setup.md` | Obsidian 目录、标签、插件配置 |
| 仿写工作流 | `docs/writing_imitation_workflow.md` | 三维分析框架、7 步仿写法 |
| Prompt 速查 | `docs/imitation_prompt_cheatsheet.md` | 11 个 Prompt 模板 |
| 个人写作库指南 | `docs/personal_writing_library_guide.md` | 完整采集与整理方案 |
| Claude Code 工作指令 | `.claude/CLAUDE.md` | 详细命令规范与禁止行为 |

---

## 推荐 Obsidian 插件

| 插件 | 用途 | 必装 |
|------|------|------|
| **Dataview** | 元数据查询、仪表盘 | ⭐ |
| **Templater** | 模板自动化 | ⭐ |
| **Tag Wrangler** | 标签管理 | ⭐ |
| **Periodic Notes** | 周期性笔记 | 推荐 |
| **Obsidian Git** | 版本控制 | 推荐 |

---

## Bases 文章质量库

Vault 根目录的 `文章质量库.base` 是 Obsidian Bases 数据库视图，可对 `05-System/analyses/articles` 下的文章分析数据进行交互式筛选和过滤。

### 前置条件

- Obsidian v1.9.0+，已启用 **Bases** 核心插件

### 10 个预设视图

| 视图 | 筛选条件 |
|------|---------|
| 📊 全览 | 所有文章，按深度降序 |
| 🏆 质量分级 | 按 S/A/B/C `groupBy` 分组 |
| ⭐ S/A 级精华 | `quality_tier == "S" \|\| "A"` |
| 💡 高原创 | `score_originality >= 80` |
| 📖 高可读 | `score_readability >= 80` |
| 🗣️ 极具人味 | `score_ai_flavor >= 70` |
| 🛠️ 高技巧 | `score_technique >= 80` |
| 🏗️ 强结构 | `score_structure >= 80` |
| 📚 按类型 | 按 `article_type` 分组 |
| 🌐 按语言 | 按 `language` 分组 |

### Bases vs Dataview

- **Bases**：交互式浏览、快速筛选、多视图切换、直接编辑属性
- **Dataview**：复杂查询、笔记内嵌表格、与内容联动

两者共用同一套 `score_*` 扁平化字段，查询语法完全一致。

### 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| 视图空白 | 文件路径不匹配 | 确认 `.base` 中的 `file.folder` 路径正确 |
| 分数列为文本 | 字段类型识别错误 | 确保 frontmatter 中值为纯数字（无引号） |
| 过滤不生效 | Bases 版本过旧 | 升级到 Obsidian v1.9.1+ |
| 分组异常 | 空值处理 | 确保 `quality_tier` 和 `article_type` 都有值 |

---

## 许可证

MIT License
