# Python gets a new governance model

**Source URL**: https://lwn.net/Articles/775105/
**Source**: LWN.net
**Date**: 2018
**Language**: 英文

## 核心论点

Python社区通过投票选出了新的治理模式：**PEP 8016 Steering Council Model**（指导委员会模式）。这标志着Python从Guido van Rossum的"仁慈独裁者"模式转向社区主导的委员会治理，使用Condorcet投票方法选出获胜方案。

## 背景

### 起因
- Guido van Rossum辞去BDFL（仁慈独裁者终身仁慈独裁者）职务
- 需要新的治理模式来替代其决策角色
- 6个PEP（Python Enhancement Proposals）参与角逐

### 投票过程演变
**原始计划**:
- 投票期：11月下旬，为期2周
- 胜出机制：即时决 runoff投票
- 投票者：核心开发者

**实际变化**:
- 即时runoff投票不受欢迎，被认为不能真正代表选民意愿
- 2018年Burlington市长选举案例暴露了即时runoff的问题
- 投票机制改为Condorcet方法
- PEP 8001（Python治理投票流程）相应修改

## 获胜方案：PEP 8016

### 核心特点
- **名称**: The Steering Council Model
- **作者**: Nathaniel Smith & Donald Stufft
- **选举结果**: Condorcet方法的明确获胜者

### 指导委员会构成

#### 人数与选举
- **人数**: 5人
- **选举者**: 核心团队成员
- **提名**: 必须由核心团队成员提名
- **投票方法**: approval voting（认可投票）
- **任期**: 单个Python特性发布周期

#### 冲突规则
**公司限制**: 不超过2名委员会成员来自同一公司

**原因**:
> 虽然我们相信委员会成员会为Python而非自己或雇主利益行事，但任何单一公司主导Python发展本身就可能有害且侵蚀信任。

**如果第三名同公司成员当选**:
- 被取消资格
- 下一位得票最高者递补

**任期中变化**（如公司收购）:
- 委员必须辞职以确保合规
- 委员会投票补位

### 委员会权限

#### 广泛职权
> 委员会拥有对项目做出决定的广泛职权。

#### 侧重授权
委员会应关注：
- Python质量和稳定性
- CPython实现
- 确保贡献流程顺畅
- 维护核心团队与Python软件基金会（PSF）的关系

#### 治理理念
- **寻求共识**: 而非独断专行
- **广泛授权**: 大部分决策委托给社区
- **最终上诉法院**: 影响语言决策的最后申诉地

#### 限制
- **不能修改治理PEP**: 只能通过核心团队2/3多数投票修改

### 其他机制

#### 不信任投票（No-Confidence Vote）
- **触发**: 核心团队成员可发起
- **条件**: 另一成员附议
- **通过**: 2/3核心团队成员赞成
- **结果**: 移除单个委员或整个委员会，随后立即重新选举

#### 成员移除
- **超级多数**: 4/5委员同意可移除核心团队成员
- **目的**: 处理极端情况

### 否决权（Veto）
根据Django治理文档启发：
- 希望永远不需要使用
- 但存在某些情况下替代方案更糟糕的情况

## 投票统计

### 选举数据
- **合格选民**: 94人
- **实际投票**: 62人
- **投票率**: 约66%

### Condorcet优势
获胜者不仅"击败所有对手"（Condorcet winner），而且即使移除获胜者，剩余7个选项中仍有一个Condorcet获胜者，以此类推一直到"进一步讨论"。

## 其他提案对比

### PEP 8010: Technical Leader Governance Model
- **特点**: 保留"仁慈独裁者"模式
- **结果**: 最不受欢迎的治理选项之一

### PEP 8012: Community Governance Model
- **特点**: 无中央权威
- **结果**: 第二名，表明社区仍希望有某种形式的领导

## 后续步骤

### 委员会选举
1. **提名期**: 2周
2. **投票期**: 2周
3. **就职**: 2019年2月3日

### 首期任期
- **时长**: 缩短期至Python 3.8发布（计划2019年10月）
- **原因**: 需要快速决定PEP批准流程等问题
- **后续**: 标准任期18个月

## 关键人物

- **Guido van Rossum**: 前BDFL，仍积极参与讨论并组织委员会选举
- **Nathaniel Smith**: PEP 8016作者之一，积极参与治理讨论
- **Donald Stufft**: PEP 8016作者之一，总结多种投票系统
- **Tim Peters**: 投票方法论讨论的积极参与者

## 历史意义

这是Python治理演进的关键时刻：
1. **从个人决策到集体决策**: 从单一领袖转向委员会模式
2. **从独裁到民主**: 引入正式投票和选举机制
3. **制度创新**: 采用Condorcet投票等成熟方法论
4. **社区成熟**: 展示Python社区有能力自我治理

## 相关实体

- [[Guido van Rossum]]
- [[Nathaniel Smith]]
- [[Donald Stufft]]
- [[Tim Peters]]
- [[Python Software Foundation]]

## 相关概念

- [[PEP 8016]]
- [[Condorcet Method]]
- [[Python治理]]
- [[Steering Council]]

## 参考资料

- PEP 8016: https://www.python.org/dev/peps/pep-8016/
- Python governance vote results: https://discuss.python.org/t/python-governance-vote-december-2018-results/546
