# 文章查询页面

> 使用Dataview插件查询分析数据。安装Dataview后，复制下方代码块到Obsidian，切换到阅读模式查看结果。

---

## 1. 🏆 按质量等级筛选

### S级文章（范式级内容）
```dataview
TABLE
  score_content_depth as "深度",
  score_readability as "可读",
  score_originality as "原创",
  quality_tier as "等级"
FROM "05-System/analyses/articles"
WHERE quality_tier = "S"
SORT score_content_depth DESC
```

### A级文章（优秀内容）
```dataview
TABLE
  score_content_depth as "深度",
  score_readability as "可读",
  score_originality as "原创",
  score_ai_flavor as "人味",
  quality_tier as "等级"
FROM "05-System/analyses/articles"
WHERE quality_tier = "A"
SORT score_content_depth DESC
```

---

## 2. 📊 按具体分数筛选

### 高深度文章（content_depth ≥ 85）
```dataview
TABLE
  score_content_depth as "深度",
  score_readability as "可读",
  score_originality as "原创",
  quality_tier as "等级"
FROM "05-System/analyses/articles"
WHERE score_content_depth >= 85
SORT score_content_depth DESC
```

### 极具人味文章（ai_flavor ≥ 80，越像人类越好）
```dataview
TABLE
  file.link as "文章",
  score_ai_flavor as "人味",
  style_tags as "风格"
FROM "05-System/analyses/articles"
WHERE score_ai_flavor >= 80
SORT score_ai_flavor DESC
```

### 高可读性文章（readability ≥ 85）
```dataview
TABLE
  file.link as "文章",
  score_readability as "可读",
  estimated_read_time as "分钟",
  target_audience as "受众"
FROM "05-System/analyses/articles"
WHERE score_readability >= 85
SORT score_readability DESC
```

### 高原创性文章（originality ≥ 85）
```dataview
TABLE
  file.link as "文章",
  score_originality as "原创",
  article_type as "类型",
  core_hook as "核心钩子"
FROM "05-System/analyses/articles"
WHERE score_originality >= 85
SORT score_originality DESC
```

---

## 3. 🎯 按文章类型筛选

### 技术深度文章
```dataview
TABLE
  score_content_depth as "深度",
  score_originality as "原创",
  quality_tier as "等级"
FROM "05-System/analyses/articles"
WHERE contains(article_type, "technical") OR contains(article_type, "技术")
SORT score_content_depth DESC
```

### 科普文章
```dataview
TABLE
  file.link as "文章",
  score_readability as "可读",
  score_virality_potential as "传播",
  estimated_read_time as "分钟"
FROM "05-System/analyses/articles"
WHERE contains(article_type, "科普") OR contains(article_type, "pop")
SORT score_readability DESC
```

---

## 4. 🔥 按风格标签筛选

### 口语化/对话式文章
```dataview
TABLE
  file.link as "文章",
  score_ai_flavor as "人味",
  score_readability as "可读"
FROM "05-System/analyses/articles"
WHERE contains(style_tags, "conversational") OR contains(style_tags, "对话式") OR contains(style_tags, "口语化")
SORT score_ai_flavor DESC
```

### 工程实践向文章
```dataview
TABLE
  file.link as "文章",
  score_content_depth as "深度",
  score_technique as "技巧",
  quality_tier as "等级"
FROM "05-System/analyses/articles"
WHERE contains(style_tags, "engineering") OR contains(style_tags, "技术") OR contains(style_tags, "工程")
SORT score_content_depth DESC
```

---

## 5. 📈 组合条件筛选

### 深度且可读（content_depth ≥ 80 AND readability ≥ 80）
```dataview
TABLE
  file.link as "文章",
  score_content_depth as "深度",
  score_readability as "可读",
  score_originality as "原创",
  quality_tier as "等级"
FROM "05-System/analyses/articles"
WHERE score_content_depth >= 80 AND score_readability >= 80
SORT score_content_depth DESC
```

### A级以上 + 高人味（quality_tier IN ("S", "A") AND ai_flavor ≥ 70）
```dataview
TABLE
  file.link as "文章",
  score_ai_flavor as "人味",
  score_content_depth as "深度",
  style_tags as "风格"
FROM "05-System/analyses/articles"
WHERE (quality_tier = "S" OR quality_tier = "A") AND score_ai_flavor >= 70
SORT score_ai_flavor DESC
```

### 技术文章 + 高实践价值（originality ≥ 80 AND technique ≥ 80）
```dataview
TABLE
  file.link as "文章",
  score_originality as "原创",
  score_technique as "技巧",
  key_techniques as "关键技巧"
FROM "05-System/analyses/articles"
WHERE score_originality >= 80 AND score_technique >= 80
SORT score_technique DESC
```

---

## 6. 📋 统计信息

### 质量等级分布
```dataview
TABLE
  quality_tier as "等级",
  length(rows) as "数量"
FROM "05-System/analyses/articles"
GROUP BY quality_tier
```

### 平均分数统计
```dataview
TABLE WITHOUT ID
  round(average(score_content_depth), 1) as "平均深度",
  round(average(score_readability), 1) as "平均可读",
  round(average(score_originality), 1) as "平均原创",
  round(average(score_ai_flavor), 1) as "平均人味"
FROM "05-System/analyses/articles"
```

---

## 7. 🎓 学习路径推荐

### 学习写作技巧（按technique降序）
```dataview
TABLE
  file.link as "文章",
  score_technique as "技巧",
  score_structure as "结构",
  score_style as "风格",
  technique_tags as "技巧标签"
FROM "05-System/analyses/articles"
WHERE score_technique >= 75
SORT score_technique DESC
LIMIT 10
```

### 模仿人类写作（按ai_flavor降序）
```dataview
TABLE
  file.link as "文章",
  score_ai_flavor as "人味",
  style_tags as "风格标签",
  emotional_triggers as "情感触发"
FROM "05-System/analyses/articles"
WHERE score_ai_flavor >= 70
SORT score_ai_flavor DESC
LIMIT 10
```

---

## 使用说明

1. **复制查询**：选中任意代码块（```dataview ... ```）
2. **粘贴到Obsidian**：创建新note，粘贴代码
3. **切换阅读模式**：点击右上角阅读模式图标
4. **查看结果**：Dataview会自动渲染成表格

### 自定义查询

修改WHERE条件可以组合任意维度：

```dataview
WHERE score_content_depth >= 80           # 深度≥80
  AND score_readability >= 75             # 且可读≥75
  AND (quality_tier = "S" OR quality_tier = "A")  # 且S/A级
  AND contains(style_tags, "technical")    # 且技术风格
```

### 排序选项

```dataview
SORT score_content_depth DESC    # 按深度降序
SORT score_ai_flavor ASC         # 按AI味升序（低分在前=更像人）
SORT file.ctime DESC              # 按创建时间降序
```

### 显示字段

可以在TABLE中指定任意frontmatter字段：

```dataview
TABLE
  file.link,                       # 文章链接
  score_content_depth,             # 深度分数
  source_url,                       # 原始URL
  estimated_read_time,              # 阅读时间
  key_techniques,                   # 关键技巧
  emotional_triggers                # 情感触发点
```
