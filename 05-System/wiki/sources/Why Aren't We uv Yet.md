# Why Aren't We uv Yet?

**Source URL**: https://lobste.rs/s/xfbwic/why_aren_t_we_uv_yet
**Source**: Lobsters（技术社区讨论）
**Date**: 2026（OpenAI收购Astral后）
**Language**: 英文

## 核心论点

尽管uv在技术性能上远超pip，但Python社区并未大规模采用它。主要障碍包括：1）VC-backed/AI公司收购的信任危机；2）对"工具用Rust写Python工具"的语言纯洁主义争议；3）现有pip+setuptools+venv栈的路径依赖；4）LLM推荐驱动的工具选择。

## 作者观点

### 为什么避免uv

**原因1：VC支持的工具必然enshittify**
> 这个融资模式保证工具会以某种方式变得糟糕，我不想在工具变得糟糕时还在使用它。

OpenAI收购证实了预期，但更早之前就预料到类似情况。

**原因2：跨语言工具的质疑**
> 我对用语言B写的语言A工具印象不佳，特别是当它们被宣传为"解决你五个工具问题的一个大工具……但更快"时。

80/20端口问题：宣传为drop-in replacement但实际不是，覆盖了常见的20%但没覆盖困难的20%。

**回应**: 作者本人（uv维护者之一）澄清，uv维护者包括Python packaging工具的核心贡献者

## 核心争议

### VC/AI公司收购的影响

**担忧**:
- OpenAI收购Astral后，uv的未来变得不确定
- 担心被enshittify（功能膨胀、商业化、破坏性变更）
- 开源许可（MIT/Apache 2.0）意味着可以fork，但社区分裂风险

**乐观观点**:
> uv是开源的，有人基本保证会fork成openuv或类似项目，在没有垃圾的情况下继续。

**现实**: 
- OpenAI成本太高，不太可能从uv直接盈利
- 但大公司无法始终以长远利益行事
- 代码已经成熟，即使公司停止维护，社区可以fork

### 语言纯洁主义 vs 工具实用主义

**质疑**: Python工具应该用Python写，不应该用Rust

**反驳**:
- Python一直是胶水语言（glue language），绑定C/C++/Rust库
- Numpy (C), SciPy (C++), PyTorch (C++/CUDA), Pydantic (Rust), cryptography (Rust)
- PyO3的成功证明Python和Rust社区很接近
- 限制工具语言会损害生态系统发展

### pip+setuptools+venv：真的"battle-tested"吗？

**质疑者观点**:
> pip+setuptools+venv栈是社区维护的、经过实战测试的，比uv慢。3/4不坏。

**维护者回应**:
- 使用这个栈10年，**从未感觉**"经过实战测试"
- 它是hack on top of hack，要支持从`setup.py`开始的全部历史
- 用户体验差，常出bug，修复缓慢

**现实**:
- 2026年新建项目使用uv的比例：80%
- 但老项目迁移缓慢，因为现有工具链已经集成

## 采用障碍

### 1. 路径依赖与沉没成本
- 大型组织有完整的pip+requirements.txt+CI脚本
- 迁移成本高，ROI不明确
- "我们一直用pip，知道它怎么用，不改"

### 2. 社区采用滞后
- Python社区很多在科学/ML圈，使用Anaconda
- 不太关注生态系统其他部分
- 广泛采用需要多年时间

### 3. LLM驱动的工具选择
> 我查看了2026年创建的top 10星标Python项目，8个是slop。非slop中，1个用uv，1个用pip。

**担忧**: LLM推荐影响工具选择，导致低质量工具泛滥

### 4. 信任危机
**收购后的犹豫**:
> 我刚用uv一周，才发现它不是开源工具。我不会再用了。我已经做过了shittification的下游受害者太多了。

**回应**: uv使用MIT许可，是开源的

## 技术优势

### 为什么uv确实更好

1. **速度**: 比pip快10-100倍（某些基准测试）
2. **依赖解析**: PEP 723脚本依赖解析
3. **Python版本管理**: 自动管理Python版本
4. **统一体验**: 替代pip+setuptools+venv多个工具
5. **可靠性**: 虚拟环境始终保持最新

### 性能数据（文章提及）
- ty在home-assistant项目上比mypy快50x
- uv比mypy daemon快10x+

## 替代方案

### PDM
- 特点：支持uv作为后端，也可独立使用
- 状态：已经很成熟，uv之前就已好用

### micromamba
- 特点：单便携可执行文件
- 优势：快速高效处理多环境
- 适用：MKL加速的NumPy和SciPy（通过conda forge）

## 关键洞察

### adoption ≠ approval
文章引用了"ttdont">Why Not Tell People to Simply Use</a>的更新，讽刺地说：

> 然后他们更新文章说"就用uv"。*钢琴砸地面的声音*

### 开源的本质
> uv的开源性质确保Astral对Python packaging/linting/typing等的贡献将继续惠及社区，无论任何结果如何。

但fork意愿不代表愿意承受分裂的痛苦。

## 相关实体

- [[Astral]]（被OpenAI收购）
- [[OpenAI]]
- [[uv]]
- [[pip]]
- [[setuptools]]
- [[venv]]
- [[poetry]]
- [[PDM]]
- [[micromamba]]

## 相关概念

- [[Python包管理]]
- [[VC-backed软件]]
- [[Enshittification]]
- [[开源fork]]

## 参考资料

- uv GitHub: https://github.com/astral-sh/uv
- uv许可: https://github.com/astral-sh/uv/blob/main/LICENSE-MIT
- Python packaging compatibility: https://github.com/astral-sh/uv/blob/e176e17144fb6e4ec010f56a7c8fa098b66ba80b/docs/pip/compatibility.md
- Why Not Tell People to Simply Use: https://www.bitecode.dev/p/why-not-tell-people-to-simply-use
