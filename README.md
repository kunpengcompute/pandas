# Pandas鲲鹏加速版

Pandas鲲鹏加速版是专为华为鲲鹏架构ARM64与openEuler操作系统深度定制优化的高性能数据分析基础库。本项目在原生pandas的基础上，针对鲲鹏多核算力及openEuler底层编译环境进行了深度适配与硬件级加速。为解决传统数据科学组在ARM平台上的编译兼容性问题，并充分释放鲲鹏计算平台的并发性能。

## 简介

BoostKit pandas是基于上游社区pandas的高性能优化项目，作为鲲鹏应用使能套件Kunpeng BoostKit生态的重要组成部分，主要用于提升pandas在ARM64/鲲鹏架构环境下的数据处理与分析性能。

在大数据量分析场景中，传统Python数据栈常面临单核算力瓶颈与内存开销大等挑战。本项目通过深入鲲鹏微架构，利用硬件指令级加速与并行计算技术，对pandas底层核心算子实施了深度重构，旨在为企业级数据科学、量化金融及物联网分析提供极致的算力支撑。

## 版本说明

本项目基于上游pandas 3.0.1开发，处于持续开发和优化阶段。

当前工作重点包括ARM64/鲲鹏平台性能优化、benchmark结果验证，以及保持与上游pandas行为的兼容性。

## 功能介绍

BoostKit pandas深度融合鲲鹏ARM64架构特性，在保持与上游社区pandas生态兼容的前提下，通过算法改良与硬件级加速，构建了高性能的数据处理矩阵。

### 核心优化领域

| 功能模块 | 原生pandas能力描述 | BoostKit鲲鹏加速特性 | 典型受益API |
| :--- | :--- | :--- | :--- |
| **数据结构与基础操作** <br>*(Data Structures)* | 提供高效的DataFrame与Series结构，支持海量异构数据的清洗与转换。 | 优化内存布局与对齐，减少Cache Miss<br>重构多表关联与级联算法，降低内存开销 | `merge()`, `join()`, `concat()`, `drop_duplicates()`, `fillna()` |
| **数学与统计计算** <br>*(Statistical Computing)* | 支持各类矩阵运算、描述性统计以及复杂的分组聚合业务指标计算。 | 引入鲲鹏SIMD（矢量计算）指令集加速<br>高基数（High-cardinality）哈希聚合多核并行化 | `groupby().agg()`, `mean()`, `sum()`, `std()`, `cov()` |
| **时间序列分析** <br>*(Time Series Analysis)* | 针对金融量化、物联网时序数据提供强大的时间戳索引与窗口函数。 | 优化滑动窗口指针移动逻辑，实现循环展开<br>加速时钟周期重采样与频率转换效率 | `rolling()`, `resample()`, `shift()`, `to_datetime()` |
| **数据处理工具集** <br>*(Data Utilities)* | 提供灵活的数据切片、条件过滤、排序及格式导出等基础工具。 | 基于鲲鹏多核架构优化并发排序算法<br>提升大文本/数值类型转换的向量化执行效率 | `sort_values()`, `astype()`, `query()`, `loc/iloc` |

## 环境部署

推荐在Linux ARM64/aarch64环境下构建和运行本项目，重点目标平台为鲲鹏服务器。其他Linux平台可用于兼容性和性能回归验证。

推荐环境如下：

- Python 3.14
- NumPy 2.4.3
- Cython 3.2.4
- Meson / meson-python
- PyArrow 24.0.0
- Numba 0.66.0
- NumExpr 2.14.1
- ASV
- pytest / pytest-xdist

具体构建依赖和版本要求以`pyproject.toml`、`meson.build`和`docs/source/development/contributing_environment.rst`中的说明为准。

## 参考文档

详细的设计说明、构建指南、开发说明和benchmark请参阅以下文档或目录。

<table style="table-layout: fixed; width: 1002px"><colgroup>
<col style="width: 301px">
<col style="width: 701px">
</colgroup>
<thead>
  <tr>
    <th>文档名称</th>
    <th>内容简介</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><a href="https://gitcode.com/boostkit/pandas/docs/zh/release_notes.md">版本说明书</a></td>
    <td>提供pandas软件发布说明。</td>
  </tr>
  <tr>
    <td><a href="https://gitcode.com/boostkit/pandas/docs/zh/quick_start.md">快速入门</a></td>
    <td>提供pandas特性在一个典型使用场景下的最简化快速上手指导。</td>
  </tr>
  <tr>
    <td><a href="https://gitcode.com/boostkit/pandas/docs/zh/compilation_build_guide.md">编译构建指南</a></td>
    <td>提供pandas软件源码包编译构建指导。</td>
  </tr>
  <tr>
    <td><a href="https://gitcode.com/boostkit/pandas/docs/zh/installation_guide.md">安装指南</a></td>
    <td>提供pandas软件打包后二进制包的安装指导。</td>
  </tr>
  <tr>
    <td><a href="https://gitcode.com/boostkit/pandas/docs/zh/user_guide.md">用户指南</a></td>
    <td>提供pandas特性功能、架构、原理、应用场景、配置使能、运维、故障处理等使用指导。</td>
  </tr>
</tbody>
</table>

其他参考资料：

- [Pandas数据结构与操作、数学与统计计算、时间序列分析及数据处理工具性能优化RFC](<docs/rfc/26.2.0/RFC - Pandas 数据结构与操作、数学与统计计算、时间序列分析及数据处理工具性能优化.md>)：本项目的优化目标、技术方案、功能设计和验证要求。
- [鲲鹏920B benchmark](asv_bench/benchmarks/aggregate_920b)：面向鲲鹏920B平台的数据处理benchmark。
- [鲲鹏950 benchmark](asv_bench/benchmarks/aggregate_950)：面向鲲鹏950平台的数据处理benchmark。
- [SwissTable benchmark](asv_bench/benchmarks/swisstable.py)：SwissTable哈希表相关性能测试。
- [自定义工作负载benchmark](asv_bench/benchmarks/custom_case.py)：典型数据处理工作负载性能测试。
- [开发环境说明](docs/source/development/contributing_environment.rst)：上游pandas源码构建和开发环境说明。
- [测试与benchmark指南](docs/source/development/contributing_codebase.rst)：上游pandas功能测试和ASV使用说明。
- [pandas用户文档](https://pandas.pydata.org/docs/)：pandas公共API和用户指南。

## License

本项目遵循上游pandas的BSD 3-Clause License，并遵循相关第三方依赖的许可证要求。

## 贡献声明

欢迎大家为社区做贡献，如果使用过程中有任何问题/建议，或者需要反馈特性需求和bug报告，可以提交[Issues](https://gitcode.com/boostkit/pandas/issues)联系我们。同时也欢迎大家在讨论专区展开讨论交流。感谢您的支持。
