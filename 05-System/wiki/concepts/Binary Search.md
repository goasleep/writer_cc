# Binary Search

**中文**: 二分查找
**复杂度**: O(log n)
**类型**: 搜索算法

## 概述

二分查找是一种在有序数组中高效查找特定元素的搜索算法。根据[Do You Even Need a Database?](../sources/Do You Even Need a Database.md)的实践，它也是构建高性能flat file存储系统的核心技术。

## 算法原理

### 基本思想
在有序数组中，通过反复将搜索区间减半来查找目标值：

1. 比较中间元素与目标值
2. 如果相等，返回索引
3. 如果目标值小于中间值，在左半部分继续搜索
4. 如果目标值大于中间值，在右半部分继续搜索
5. 重复直到找到或区间为空

### 复杂度分析
- **时间复杂度**: O(log n)
- **空间复杂度**: O(1)（迭代实现）
- **1M记录**: 约20次比较（log₂(1,000,000) ≈ 20）

## 在Flat File Storage中的应用

根据[Do You Even Need a Database?](../sources/Do You Even Need a Database.md)的实践：

### 实现方法
1. **数据文件排序**: 按ID排序后构建索引
2. **固定宽度索引**: 每条记录58字节（36字节UUID + 20字节偏移量 + 换行符）
3. **直接寻址**: 使用`ReadAt(buf, entryIndex * 58)`跳转到任意条目
4. **两步查找**:
   - 在索引文件中二分查找（O(log n)次ReadAt）
   - 找到偏移量后，在数据文件中Seek并读取单条记录

### 性能表现
- **10k记录**: 45,742 req/s
- **100k记录**: 41,661 req/s
- **1M记录**: 38,866 req/s
- **性能下降**: 数据增长100倍，性能仅下降15%

### 为什么这么快？
1. **OS页缓存**: 热点页面（索引中间部分）始终在内存中
2. **固定宽度**: 可以计算任意条目的精确位置
3. **顺序访问**: 索引查找模式对磁盘友好
4. **单次读取**: 找到后只读取一条数据记录

## 与其他方法的对比

### vs Linear Scan
- **Linear Scan**: O(n)，1M记录时23 req/s
- **Binary Search**: O(log n)，1M记录时38k req/s
- **性能提升**: 约1700倍

### vs SQLite B-tree
- **Binary Search**: 1M记录时38k req/s
- **SQLite**: 1M记录时25k req/s
- **性能优势**: 约1.7倍
- **原因**: SQLite做更多工作（事务、并发、完整性检查）

### vs In-Memory Map
- **In-Memory Map**: O(1)，但需要数据集适合RAM
- **Binary Search**: O(log n)，不需要加载全部数据
- **权衡**: 内存 vs 计算时间

## 实际应用

### 何时使用
- **数据集不适合RAM**: 需要磁盘上的高效查找
- **按主键查询**: 只需要ID查找
- **读取密集**: 读多写少的场景
- **单进程写入**: 不需要复杂的多进程并发

### 实现注意事项
1. **排序开销**: 数据必须按ID排序
2. **写入策略**: 追加会破坏排序，需要定期重建索引
3. **LSM Tree**: 实际系统使用write-ahead buffer + 周期性合并
4. **固定宽度**: 索引必须是固定宽度才能随机访问

## 技术细节

### 索引格式示例
```
a1b2c3d4-e5f6-7890-abcd-ef1234567890:00000000000000012345
uuid-with-36-characters:00000000000000067890
```
- 每行精确58字节
- 36字节UUID + 冒号 + 20字节偏移量 + 换行符

### 代码示例（概念）
```go
// 计算索引条目位置
entryIndex := mid
offset := entryIndex * 58

// 读取索引条目
ReadAt(indexBuf, offset)

// 解析偏移量
dataOffset := parseOffset(indexBuf)

// 跳转到数据记录
Seek(dataOffset)
ReadData(dataRecord)
```

## 相关概念

- [[Flat File Storage]]
- [[In-Memory Index]]
- [[LSM Tree]]
- [[B-tree]]

## 相关实体

- [[DB Pro]]
- [[SQLite]]
