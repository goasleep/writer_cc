# Condorcet Method

**类型**: 投票系统
**起源**: 18世纪法国数学家Marie Jean Antoine Nicolas de Caritat Condorcet
**应用**: Python治理选举（2018年）

## 简介

孔多塞方法（Condorcet Method）是一种选举制度，其中候选人通过两两比较来确定获胜者。如果在所有两两对决中，某位候选人都能击败其他候选人，则该候选人被称为"孔多塞获胜者"（Condorcet winner）。2018年，Python社区采用此方法选举新的治理模式。

## 核心原理

### 两两比较

**基本机制**:
- 每个候选人在一对一的对决中与其他所有候选人进行比较
- 获得最多选票的候选人赢得该对决
- 如果存在一个候选人在所有对决中都获胜，该候选人即为最终获胜者

**孔多塞获胜者**:
> 在所有两两对决中都击败其他候选人的候选人

### 优势

**代表性**:
- 比即时runoff投票（IRV）更能反映选民真实意愿
- 避免了"投票策略"问题
- 更不容易产生争议结果

**2018年Burlington市长选举案例**:
- 即时runoff投票在此选举中暴露了严重缺陷
- 获胜者并非大多数选民的真实偏好
- 这一案例促使Python社区转向Condorcet方法

**Python应用的优势**:
PEP 8016不仅是孔多塞获胜者，而且即使移除获胜者，剩余选项中仍有孔多塞获胜者，以此类推。这显示了投票系统的稳定性和代表性。

## Python治理中的应用

### 投票机制转变

**原始计划**:
- 投票期：2018年11月下旬，为期2周
- 胜出机制：即时runoff投票
- 投票者：核心开发者

**实际变化**:
- 即时runoff投票被认为不能真正代表选民意愿
- 投票机制改为Condorcet方法
- PEP 8001（Python治理投票流程）相应修改

### 2018年Python治理选举

**选举数据**:
- 合格选民：94人
- 实际投票：62人
- 投票率：约66%

**获胜者**: PEP 8016（Steering Council Model）
- 作者：Nathaniel Smith & Donald Stufft
- 成为Condorcet方法的明确获胜者
- 即使移除获胜者，剩余选项中仍有孔多塞获胜者

## 与其他投票系统的比较

### 即时Runoff投票（IRV）

**缺点**:
- 不能真正代表选民意愿
- 可能产生非直观的结果
- 在 Burlington 案例中暴露问题

**优点**:
- 计算简单
- 易于理解

### 认可投票（Approval Voting）

**用途**:
- 在PEP 8016中用于指导委员会成员选举
-选民可以认可多个候选人
- 得票最多的候选人当选

**特点**:
- 简单易实施
- 鼓励诚实投票
- 适合多席位选举

## 技术实现

### Python选举中的实施

**Donald Stufft的贡献**:
- 总结了多种投票系统的优缺点
- 帮助社区理解Condorcet方法的优势
- 确保了投票系统的技术正确性

**投票过程**:
1. 核心开发者对6个治理PEP进行排名
2. 使用Condorcet方法进行两两比较
3. 确定孔多塞获胜者
4. PEP 8016成为最终获胜方案

## 相关概念

- [[PEP 8016]]
- [[Python治理]]
- [[即时Runoff投票]]
- [[认可投票]]

## 相关实体

- [[Donald Stufft]]（投票系统专家）
- [[Nathaniel Smith]]（PEP 8016作者）
- [[Tim Peters]]（投票方法论参与者）

## 参考资料

- PEP 8016: https://www.python.org/dev/peps/pep-8016/
- PEP 8001: https://www.python.org/dev/peps/pep-8001/
- Python governance vote results: https://discuss.python.org/t/python-governance-vote-december-2018-results/546
- Condorcet method explained: https://en.wikipedia.org/wiki/Condorcet_method

