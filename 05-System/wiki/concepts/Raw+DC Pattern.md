---
type: concept
name: "Raw+DC Pattern"
category: "设计模式/数据访问"
---

# Raw+DC Pattern

Raw+DC（Raw Queries + Data Classes）是一种数据库访问设计模式，使用原生数据库查询配合带 slots 的 dataclass，替代传统的 ODM（对象文档映射）。

## 核心思想

### 传统 ODM 模式
```python
from mongoengine import Document

class User(Document):
    email = StringField(required=True)
    name = StringField(max_length=50)

user = User.objects.get(email="test@example.com")
```

**问题**：
- 运行时开销大
- 内存占用高
- 难以支持异步

### Raw+DC 模式
```python
from dataclasses import dataclass

@dataclass(slots=True)
class User:
    email: str
    name: str

async def get_user(email: str) -> User:
    doc = await db.users.find_one({"email": email})
    return User(**doc)
```

**优势**：
- 轻量级（slots 减少内存占用）
- 原生支持异步
- 性能更优

## 性能收益

### 内存优化

在 [[Michael Kennedy]] 的实践中：
- 每个 worker 节省：**100 MB**
- 2 workers 总节省：**200 MB**

### 性能提升

- 请求/秒提升：**近 2 倍**
- 数据库查询延迟降低

## 技术细节

### Dataclass Slots

```python
from dataclasses import dataclass

@dataclass(slots=True)
class User:
    email: str
    name: str
```

**`slots=True` 的作用**：
- 禁止动态属性添加
- 减少 `__dict__` 开销
- 内存占用显著降低

### 异步支持

```python
import motor  # 异步 MongoDB 驱动

async def get_users():
    async with await motor_client.start_session() as session:
        cursor = db.users.find({})
        return [User(**doc) async for doc in cursor]
```

## 迁移挑战

### 从 MongoEngine 迁移

[[Michael Kennedy]] 将 Talk Python Training 从 MongoEngine 迁移到 Raw+DC：
- 工作量：较大
- 收益：内存 + 性能双提升
- 必要性：MongoEngine 不支持异步

### 适用场景

✅ **适合**
- 需要异步数据访问
- 内存受限的环境
- 性能要求高的场景

❌ **不适合**
- 简单 CRUD 应用（ODM 足够）
- 团队不熟悉原生查询
- 需要复杂关系映射

## 相关概念

- [[Async Workers]]
- [[Memory Optimization]]
- [[MongoEngine]]

## 参考来源

- [[Cutting Python Web App Memory Over 31%]]
- [Raw+DC Database Pattern: A Retrospective](https://mkennedy.codes/posts/raw-dc-a-retrospective/)
