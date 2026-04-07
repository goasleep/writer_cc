# 个人写作库系统

> 一个以 **Obsidian Vault** 为核心，由 **Claude Code** 驱动的个人写作库。
> **你的入口只有 Claude Code 和 Obsidian。所有工具操作，交给 Claude Code。**

---

## 核心理念

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
│ 00-Inbox/          │ 03-Resources/     │ 01-Projects/        │
└────────────────────┴───────────────────┴─────────────────────┘
```

**关键原则：**
- 你不用记任何 CLI 命令
- `src/writer_tools/` 下的 Python 工具**只由 Claude Code 自动调用**
- 你的操作路径只有两条：
  1. **跟 Claude Code 对话** → 完成采集、分析、仿写、整理
  2. **在 Obsidian 中** → 阅读、编辑、双向链接、写作创作

---

## 快速开始

### 1. 在 Claude Code 中打开本目录

确保你的 Claude Code 会话工作目录指向 `writer_cc/`。

### 2. 在 Obsidian 中打开本目录

将 `writer_cc/` 作为 Vault 直接在 Obsidian 中打开即可。

### 3. 开始对话

在 Claude Code 中说：
- `"采集 https://example.com/article"`
- `"帮我整理一下收件箱"`
- `"我想仿写这篇文章，主题是..."`
- `"看看今天的 MOC 需要更新吗"`

Claude Code 会自动完成剩下的工作。

---

## Claude Code 命令

与 Claude Code 对话时可以使用以下指令：

| 命令 | 作用 |
|------|------|
| `/collect <url>` | 采集文章到 `00-Inbox/` |
| `/batch <file>` | 批量采集 |
| `/inbox` | 查看 Inbox 状态 |
| `/imitate` | 参考文章仿写 |
| `/moc` | 查看/更新主题地图 |
| `/clean <file>` | 清理 Markdown 格式 |

配置详见：`.claude/CLAUDE.md`

---

## Vault 目录结构

```
writer_cc/                    # ← 本目录即 Obsidian Vault
├── 00-Inbox/                 # 新采集的文章（Claude Code 自动放入）
├── 01-Projects/              # 进行中的写作项目
├── 02-Areas/                 # 持续维护的领域知识
├── 03-Resources/             # 参考文章、读书笔记、金句
├── 04-Archive/               # 归档项目
├── 05-System/
│   ├── Templates/            # Obsidian 模板
│   ├── MOCs/                 # 主题地图
│   ├── Attachments/          # 附件
│   └── 仪表盘.md             # Dataview 仪表盘
├── 99-Daily/                 # 每日笔记
├── docs/                     # 详细文档
│   ├── vault_setup.md
│   ├── writing_imitation_workflow.md
│   ├── imitation_prompt_cheatsheet.md
│   └── personal_writing_library_guide.md
├── src/writer_tools/         # Python 工具源码（Claude Code 专用）
├── .claude/                  # Claude Code 配置
│   ├── CLAUDE.md             # 工作指令
│   └── skills/               # Skills 定义
└── pyproject.toml            # 工具依赖配置
```

---

## 环境准备（首次使用）

如果你需要手动初始化环境（**通常 Claude Code 会自动处理**）：

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装依赖
uv sync
```

> 普通用户不需要关心这一步。交给 Claude Code。

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

## Git 工作流

Claude Code 会在整理完成后建议你提交：

```bash
git add 00-Inbox/ 03-Resources/ 05-System/
git commit -m "collect: articles + update MOCs"
git push
```

你也可以在 Obsidian 中使用 **Obsidian Git** 插件一键提交。

---

## 文档索引

| 文档 | 路径 | 说明 |
|------|------|------|
| Vault 设置指南 | `docs/vault_setup.md` | Obsidian 目录、标签、插件配置 |
| 仿写工作流 | `docs/writing_imitation_workflow.md` | 三维分析框架、7 步仿写法 |
| Prompt 速查 | `docs/imitation_prompt_cheatsheet.md` | 11 个 Prompt 模板 |
| 个人写作库指南 | `docs/personal_writing_library_guide.md` | 完整采集与整理方案 |

---

## 许可证

MIT License
