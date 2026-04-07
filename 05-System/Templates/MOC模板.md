---
title: "MOC - {{topic}}"
aliases: ["{{topic}}知识地图"]
created: {{date:YYYY-MM-DD}}
modified: {{date:YYYY-MM-DD}}

tags:
  - type/moc
  - topic/{{topic}}
---

# {{topic}} 知识地图

## 概述
<!-- 该主题的核心概念介绍 -->

## 核心概念
- [[概念1]]
- [[概念2]]
- [[概念3]]

## 相关文章
```dataview
TABLE title, rating, status, modified
FROM ""
WHERE contains(tags, "topic/{{topic}}") AND file.name != this.file.name
SORT rating DESC, modified DESC
```

## 子主题
- [[子主题1]]
- [[子主题2]]

## 实践案例
- 

## 资源推荐
- 

## 待学习
- [ ] 

---

## 更新记录
- {{date:YYYY-MM-DD}}: 创建MOC
