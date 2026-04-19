# LSM Tree

**全称**: Log-Structured Merge Tree
**中文**: 日志结构合并树
**类型**: 数据结构
**复杂度**: O(log n)

## 概述

LSM Tree是一种磁盘数据结构，专门为高写入吞吐量优化。根据[Do You Even Need a Database?](../sources/Do You Even Need a Database.md)的描述，它是处理追加写入破坏排序问题的标准解决方案。

## 核心思想

LSM Tree将数据分为多层：
1. **Memory Table (MemTable)**: 内存中的有序结构
2. **Immutable MemTable**: 内存中不可写的快照
3. **SSTables (Sorted String Tables)**: 磁盘上的有序文件
4. **Compaction**: 后台合并过程

## 工作原理

### 写入路径
1. **写入MemTable**: 数据写入内存中的有序结构
2. **MemTable满**: 转换为Immutable MemTable
3. **刷盘**: Immutable MemTable写入新的SSTable
4. **追加写入**: 新SSTable追加到现有文件

### 读取路径
1. **查找MemTable**: 首先检查内存表
2. **查找Immutable MemTable**: 检查不可写内存表
3. **查找SSTables**: 按从新到旧顺序查找磁盘文件
4. **合并结果**: 返回找到的最新值

### Compaction（合并）
- **后台进程**: 定期合并多个SSTables
- **去重**: 删除旧版本的重复键
- **排序**: 保持全局有序
- **删除标记**: 处理删除操作

## 在Flat File Storage中的应用

根据[Do You Even Need a Database?](../sources/Do You Even Need a Database.md)的描述：

### 问题场景
追加新记录会破坏排序：
- 数据文件按ID排序
- 新记录追加到末尾
- 二分查找索引失效

### LSM解决方案
1. **保持主文件有序**: 不直接修改主文件
2. **Write-Ahead Buffer**: 维护无序的追加buffer
3. **周期性合并**: 将buffer合并到主文件
4. **重建索引**: 合并后重建二分查找索引

### 实现模式
```
主文件（有序） ← Buffer（无序追加）
       ↓
   定期合并
       ↓
新的有序主文件 + 重建索引
```

## 优势

### 1. 写入性能
- **追加写入**: O(1)写入复杂度
- **批量刷盘**: 减少磁盘I/O
- **无随机写入**: 顺序写性能更高

### 2. 读取性能
- **内存优先**: 热数据在内存中
- **层次查找**: 最小化磁盘访问
- **Bloom Filter**: 减少不必要的磁盘查找

### 3. 压缩率
- **SSTable压缩**: 有序数据压缩更好
- **前缀编码**: 键的前缀可以压缩
- **块压缩**: 减少存储空间

## 劣势

### 1. 写入放大
- **多次写入**: 同一数据可能写入多次
- **Compaction开销**: 合并过程消耗资源
- **空间放大**: 临时需要额外空间

### 2. 读取延迟
- **多层查找**: 可能需要查找多个SSTables
- **缓存未命中**: 冷数据需要磁盘访问
- **Compaction干扰**: 后台合并影响性能

### 3. 复杂性
- **实现复杂**: 需要管理多个层次
- **调优困难**: 需要平衡写入和读取性能
- **监控重要**: 需要监控Compaction健康状况

## 与其他数据结构的对比

### vs B-Tree
| 维度 | LSM Tree | B-Tree |
|------|----------|--------|
| 写入性能 | 高（追加） | 中（随机写） |
| 读取性能 | 中（多层查找） | 高（单层查找） |
| 空间使用 | 高（写放大） | 低 |
| 实现复杂度 | 高 | 中 |
| 适用场景 | 写多读少 | 读多写少 |

### vs Binary Search on Disk
- **Binary Search**: 适合静态数据，重建索引开销大
- **LSM Tree**: 适合动态数据，增量更新

## 实际应用

### 数据库系统
- **RocksDB**: Facebook开源的LSM实现
- **LevelDB**: Google开发的键值存储
- **Cassandra**: 使用LSM作为存储引擎
- **HBase**: Hadoop的LSM实现
- **SQLite**: WAL模式类似LSM思想

### 使用场景
1. **时序数据**: 按时间追加写入
2. **日志系统**: 顺序写入日志
3. **缓存系统**: 高吞吐量写入
4. **事件溯源**: 不可变事件流

## 性能考虑

### Compaction策略
1. **Size-Tiered**: 相似大小的SSTables合并
2. **Leveled**: 每层固定大小，更频繁合并
3. **Tiered vs Leveled**: 权衡写入放大和读取性能

### 优化技术
1. **Bloom Filter**: 快速判断键是否在SSTable中
2. **Caching**: 热SSTables缓存在内存中
3. **Partitioning**: 按键范围分区
4. **Compression**: 减少磁盘I/O

## 相关概念

- [[Flat File Storage]]
- [[Binary Search]]
- [[In-Memory Index]]
- [[B-tree]]
- [[SSTable]]

## 相关实体

- [[RocksDB]]
- [[LevelDB]]
- [[Cassandra]]
- [[SQLite]]
