---
type: concept
name: "Partial Index"
category: "Database/PostgreSQL"
---

# Partial Index

部分索引（Partial Index）是一种只对表中满足特定条件的行创建索引的索引类型，在 PostgreSQL 中通过 `WHERE` 子句实现。

## 基本语法

```sql
CREATE INDEX idx_name
ON table_name (column_name)
WHERE condition;
```

## 应用场景

### 1. 排除 NULL 值

```sql
CREATE INDEX idx_orders_status
ON orders (status)
WHERE status IS NOT NULL;
```

**优势**：
- 索引更小
- 维护成本更低
- 查询优化器能更好地利用

### 2. 特定业务条件

```sql
-- 只索引活跃用户
CREATE INDEX idx_users_active
ON users (email)
WHERE is_active = true;

-- 只索引未完成订单
CREATE INDEX idx_orders_pending
ON orders (customer_id)
WHERE status != 'completed';
```

### 3. 时间范围数据

```sql
-- 只索引最近 30 天的数据
CREATE INDEX idx_logs_recent
ON logs (created_at)
WHERE created_at > NOW() - INTERVAL '30 days';
```

## 性能优势

### GIN 索引的场景

在 [[Claude Pitfalls Database Indexes  Lincoln Loop]] 一文中，部分索引的关键优势：

1. **数据填充期间**：NULL → 非NULL 转换时不触发索引维护
2. **并发写入**：NULL 行的更新不触及索引
3. **查询性能**：显式限制索引范围，优化器选择更准确

### 对比表

| 操作 | 全量索引 | 部分索引 |
|------|---------|---------|
| NULL → NULL UPDATE | 触及索引 | 不触及 |
| NULL → 非NULL UPDATE | 触及索引 | 触及索引 |
| 非NULL → 非NULL UPDATE | 触及索引 | 触及索引 |
| 新插入 NULL 行 | 触及索引 | 不触及 |

## 查询使用条件

部分索引只会在查询满足 WHERE 条件时被使用：

```sql
-- 会使用部分索引
SELECT * FROM orders WHERE status = 'pending' AND status IS NOT NULL;

-- 不会使用部分索引
SELECT * FROM orders WHERE status IS NULL;
```

## 注意事项

1. **查询必须匹配 WHERE 条件**：否则优化器不会选择部分索引
2. **条件选择要谨慎**：过于严格会导致索引利用率低
3. **维护多个索引**：可能需要创建多个部分索引覆盖不同场景

## 相关概念

- [[GIN Index]]
- [[Concurrent Index Creation]]
- [[PostgreSQL]]

## 参考来源

- [[Claude Pitfalls Database Indexes  Lincoln Loop]]
- PostgreSQL Documentation: [Partial Indexes](https://www.postgresql.org/docs/current/indexes-partial.html)
