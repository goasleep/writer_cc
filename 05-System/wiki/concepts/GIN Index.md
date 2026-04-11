---
type: concept
name: "GIN Index"
category: "Database/PostgreSQL"
---

# GIN Index

GIN (Generalized Inverted Index) 是 PostgreSQL 中的一种索引类型，专门用于处理多值类型数据，如数组、全文搜索、JSONB 等。

## 核心特性

### NULL 值处理

**关键行为**：GIN 索引**不索引 NULL 值**。

这是本文揭示的最重要的发现：

```sql
-- 新添加的列，所有行都是 NULL
ALTER TABLE images ADD COLUMN search tsvector;

-- 创建 GIN 索引
CREATE INDEX ON images USING gin (search);

-- 即使表有 3.1M 行，索引创建也是瞬间的
-- 因为 GIN 完全跳过 NULL 值
```

### 适用场景

- **全文搜索**：`tsvector` 类型
- **数组**：`integer[]`, `text[]` 等
- **JSONB**：`jsonb` 类型的键值对
- **范围类型**：`int4range`, `tsrange` 等

## 性能特点

| 特性 | 说明 |
|------|------|
| 查询性能 | 优秀，特别是包含操作符（`@>`, `@@` 等） |
| 插入/更新成本 | 较高，因为需要维护多值索引 |
| 索引大小 | 通常较大，但 NULL 值不占用空间 |
| 并发创建 | 支持 `CONCURRENTLY` 选项 |

## 与 B-Tree 索引的对比

| 特性 | B-Tree | GIN |
|------|--------|-----|
| 数据类型 | 单值类型 | 多值类型 |
| 等值查询 | 优秀 | 一般 |
| 范围查询 | 优秀 | 不适用 |
| 包含查询 | 不适用 | 优秀 |
| 索引大小 | 较小 | 较大 |
| 维护成本 | 低 | 高 |

## 部分索引优化

对于 GIN 索引，部分索引（`WHERE column IS NOT NULL`）在以下场景有优势：

1. **数据填充期间**：NULL → 非NULL 转换时不触发索引维护
2. **混合 NULL/非 NULL 数据**：减少索引维护开销
3. **查询优化**：显式告诉查询优化器索引的适用范围

```sql
CREATE INDEX CONCURRENTLY idx_image_search_gin
ON images USING gin (search)
WHERE search IS NOT NULL;
```

## 相关概念

- [[Partial Index]]
- [[Concurrent Index Creation]]
- [[PostgreSQL]]

## 参考来源

- [[Claude Pitfalls Database Indexes  Lincoln Loop]]
- PostgreSQL Documentation: [GIN Indexes](https://www.postgresql.org/docs/current/gin.html)
