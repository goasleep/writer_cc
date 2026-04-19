# Flat File Storage

**定义**: 使用普通文件系统文件存储数据，而非专门的数据库系统
**别名**: 文件存储、平面文件存储

## 概述

Flat File Storage是指使用操作系统的普通文件来存储和访问数据，而不使用专门的数据库管理系统。根据[Do You Even Need a Database?](../sources/Do You Even Need a Database.md)的分析，对于许多早期应用来说，文件存储可能是比数据库更合适的选择。

## 核心观点

> "A database is just files. SQLite is a single file on disk. PostgreSQL is a directory of files with a process sitting in front of them."

问题不是是否使用文件（你总是在使用文件），而是使用数据库的文件还是你自己的文件。对于许多应用，尤其是早期阶段的，答案可能是：你自己的。

## 三种实现策略

### 1. Linear Scan（线性扫描）
- **方法**: 每次请求时打开文件，逐行扫描，解析JSON，检查ID
- **复杂度**: O(n)
- **性能**: 数据规模增大时线性下降
- **适用场景**: 数据集很小（< 10k记录）

### 2. In-Memory Map（内存哈希表）
- **方法**: 启动时读取整个文件到哈希表，读写都是O(1)查找
- **复杂度**: O(1)
- **性能**: 任何规模下97k req/s（Go实现）
- **限制**: 数据集必须能放入RAM
- **适用场景**: 数据集适合单机内存

### 3. Binary Search on Disk（磁盘二分查找）
- **方法**: 数据按ID排序，构建固定宽度索引，使用ReadAt二分查找
- **复杂度**: O(log n)
- **性能**: 1M记录时38k req/s，数据增长100倍性能仅下降15%
- **优势**: 不需要加载全部数据到RAM
- **适用场景**: 数据集不适合RAM但需要快速查找

## 性能基准

根据[Do You Even Need a Database?](../sources/Do You Even Need a Database.md)的测试：

| 方法 | 10k记录 | 1M记录 | 可支撑日活 |
|------|---------|--------|-----------|
| Linear Scan | 783 req/s | 23 req/s | 280万 |
| In-Memory Map | 97k req/s | 97k req/s | 3.49亿 |
| Binary Search | 45k req/s | 38k req/s | 1.44亿 |
| SQLite | 26k req/s | 25k req/s | 9000万 |

## 数据格式

### JSONL（JSON Lines）
- 每行一个记录
- 写入时追加
- 格式：`{"id": "abc-123", "name": "..."}`
- 适合：单实体类型文件

### 索引格式
固定宽度索引（用于二分查找）：
- 每条记录一行，精确58字节
- 格式：`<36-char UUID>:<20-digit byte offset in data file>\n`
- 可以通过`ReadAt(buf, entryIndex * 58)`直接跳转

## 适用场景

### 适合使用Flat File的情况
- **早期阶段产品**: 数据集小，查询简单
- **内部工具**: 单机部署，用户量有限
- **原型开发**: 快速迭代，不需要复杂查询
- **单实例应用**: 不需要多进程并发写入
- **简单查询**: 只需要按ID查找

### 不适合的情况
- **数据集超过RAM**: 需要分页加载数据
- **多字段查询**: 需要按多个条件查找
- **需要JOIN**: 需要关联多个实体
- **多进程写入**: 需要外部数据源协调
- **跨实体事务**: 需要ACID保证

## 优势

1. **简单**: 无需安装、配置数据库
2. **透明**: 数据格式人类可读
3. **可迁移**: JSONL可轻松导入任何数据库
4. **性能**: 对于小规模数据，性能优异
5. **无vendor lock-in**: 不被任何数据库锁定

## 劣势

1. **扩展性**: 数据规模增长时性能下降
2. **查询能力**: 只能做简单查找
3. **并发**: 单进程内的并发保护
4. **事务**: 需要自己实现事务日志
5. **JOIN**: 需要在应用代码中手动组装

## 迁移路径

**文件仍在那里，需要时可以迁移**：
- JSONL格式可轻松导入任何数据库
- 没有vendor lock-in
- 可以在需要时平滑迁移到数据库

## 相关概念

- [[Binary Search]]
- [[In-Memory Index]]
- [[LSM Tree]]
- [[SQLite]]
- [[PostgreSQL]]

## 相关实体

- [[DB Pro]]
- [[SQLite]]
- [[PostgreSQL]]
