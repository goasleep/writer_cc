---
type: concept
name: "Concurrent Index Creation"
category: "Database/PostgreSQL"
---

# Concurrent Index Creation

并发索引创建（Concurrent Index Creation）是 PostgreSQL 提供的一种在不阻塞写操作的情况下创建索引的机制。

## 问题背景

### 标准索引创建的问题

```sql
-- 标准 CREATE INDEX 会阻塞所有写操作
CREATE INDEX idx_name ON table_name (column_name);
```

**影响**：
- 获取 `ACCESS EXCLUSIVE` 锁
- 阻塞所有写操作（INSERT、UPDATE、DELETE）
- 在大表上可能持续数分钟甚至数小时

### 生产环境风险

在 [[Claude Pitfalls Database Indexes  Lincoln Loop]] 的案例中：
- 表有 3.1M 行
- 标准 `CREATE INDEX` 可能导致数分钟的写阻塞
- 对于高流量应用，这是不可接受的

## 解决方案：CONCURRENTLY

```sql
CREATE INDEX CONCURRENTLY idx_name
ON table_name (column_name);
```

### 特点

- **不阻塞写操作**：表仍然可以正常读写
- **获取锁**：`SHARE UPDATE EXCLUSIVE` 锁（较弱的锁级别）
- **耗时更长**：通常比标准创建慢 2-3 倍
- **可以失败**：在长时间创建过程中可能因死锁等原因失败

## 限制

### 不能在事务中运行

```python
# Django Migration
class Migration(migrations.Migration):
    atomic = False  # 必须设置为 False
    operations = [
        migrations.RunSQL(
            sql='CREATE INDEX CONCURRENTLY idx_name ON table_name (column)',
        ),
    ]
```

### 限制说明

1. **事务外执行**：必须在事务外执行
2. **无法回滚**：如果失败，需要手动清理遗留索引
3. **不支持所有索引类型**：某些约束索引不支持

## Django 实现

### 方法 1：AddIndexConcurrently（推荐）

```python
from django.contrib.postgres.operations import AddIndexConcurrently
from django.contrib.postgres.indexes import GinIndex

class Migration(migrations.Migration):
    operations = [
        AddIndexConcurrently(
            model_name='image',
            index=GinIndex(fields=['search'], name='idx_image_search'),
        ),
    ]
```

### 方法 2：SeparateDatabaseAndState

```python
class Migration(migrations.Migration):
    atomic = False
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql='CREATE INDEX CONCURRENTLY idx_name ON table_name (column)',
                    reverse_sql='DROP INDEX CONCURRENTLY IF EXISTS idx_name',
                ),
            ],
            state_operations=[
                migrations.AddIndex(
                    model_name='image',
                    index=GinIndex(fields=['search'], name='idx_name'),
                ),
            ],
        ),
    ]
```

## 最佳实践

1. **评估表大小**：小表可以直接创建，大表使用 CONCURRENTLY
2. **测试先行**：在生产快照上测试索引创建时间
3. **监控进度**：使用 `pg_stat_progress_create_index` 监控
4. **准备回滚**：如果创建失败，需要手动清理

## 相关概念

- [[GIN Index]]
- [[Partial Index]]
- [[PostgreSQL]]
- [[Django]]

## 参考来源

- [[Claude Pitfalls Database Indexes  Lincoln Loop]]
- Django Documentation: [Concurrent Index Operations](https://docs.djangoproject.com/en/6.0/ref/contrib/postgres/operations/#concurrent-index-operations)
