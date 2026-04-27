# Index Manager Skill

**描述**: 管理和更新个人写作库的各种索引，包括URL索引、wiki索引、analyses索引等。

## 触发条件

当用户请求以下操作时触发此skill：
- `/build-index` - 构建和更新所有索引
- "构建索引"、"更新索引"、"重建索引"等相关表述

## 功能

### 1. URL索引管理
- 重建URL索引缓存
- 显示URL索引统计信息
- 验证URL索引有效性

### 2. Wiki索引管理
- 更新wiki/index.md
- 验证wiki双向链接
- 同步wiki相关索引

### 3. Analyses索引管理
- 更新analyses相关索引
- 重新生成analyses聚合索引

## 执行流程

1. **URL索引重建**
   - 调用 `uv run writer-collect rebuild-index`
   - 显示索引统计信息（总URL数、构建耗时）

2. **Wiki索引更新**
   - 扫描 `05-System/wiki/` 目录结构
   - 检查sources、entities、concepts目录
   - 更新 `wiki/index.md` 中的链接列表
   - 验证所有双向链接的有效性

3. **Analyses索引更新**
   - 扫描 `05-System/analyses/articles/` 目录
   - 读取所有分析文件
   - 更新by-style、by-technique、by-article-type索引
   - 更新时间戳

4. **生成汇总报告**
   - 显示各索引的统计信息
   - 报告任何发现的问题

## 工具使用

使用Bash工具执行以下命令：
- `uv run writer-collect rebuild-index` - 重建URL索引
- `ls -la 05-System/wiki/` - 检查wiki目录结构
- `find 05-System/analyses/ -name "*.md"` - 查找分析文件

## 输出格式

```
🔧 开始构建所有索引...

1️⃣ URL索引
✅ 索引构建完成，共 29 个URL

2️⃣ Wiki索引
✅ Sources: 29篇文章
✅ Entities: 46个实体
✅ Concepts: 95个概念
✅ 双向链接验证完成

3️⃣ Analyses索引
✅ 分析文章: 29篇
✅ 索引已更新至 2026-04-20

📊 索引构建完成！所有索引均为最新状态。
```

## 错误处理

- 索引文件损坏时自动重建
- 目录不存在时给出提示
- 链接失效时报告问题
- 权限不足时提示用户

## 注意事项

1. 大部分索引会在采集/分析时自动更新，此命令主要用于完整重建
2. 运行时间取决于文章数量，一般几秒到几十秒
3. 建议定期运行以确保所有索引同步
4. 如果发现索引问题，可以随时运行此命令修复
