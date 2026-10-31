# 用户指南

本项目专为ARM64架构（重点面向华为鲲鹏服务器）打造，旨在深度优化pandas在大规模数据分析场景下的执行效率。

## 特性介绍

项目不改变用户原有的开发习惯，而是通过底层技术的加持实现全方位加速。

### 核心优化策略

* 算法演进：引入先进的哈希与数据结构算法。
* 计算下沉：将热点执行路径下沉至高性能底层（C++/SIMD指令集）。
* 硬件加速：充分利用ARM64的SIMD向量化指令能力。
* 架构调优：优化CPU缓存（Cache）访问模式，消除不必要的内存与对象开销。

### 功能模块

<table style="table-layout: fixed; width: 1000px"><colgroup>
<col style="width: 200px">
<col style="width: 350px">
<col style="width: 450px">
</colgroup>
<thead>
  <tr>
    <th>功能</th>
    <th>技术实现</th>
    <th>优化结果</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>哈希密集型操作</td>
    <td>引入支持SIMD矢量加速的SwissTable哈希表实现。</td>
    <td>提升数值数据的哈希表构建、批量查找、唯一值处理（unique）、成员判断（isin）、值计数（value_counts）、重复值处理（drop_duplicates）及因子化（factorize）的计算效率。</td>
  </tr>
  <tr>
    <td>分组与聚合计算（GroupBy）</td>
    <td>重构底层聚合循环在ARM64平台上的执行效率，减少分组过程中的中间对象创建、重复计算与数据重排。</td>
    <td>提升分组构建、数值与字符串聚合、数据变换（transform）及累计计算路径的执行效率。</td>
  </tr>
  <tr>
    <td>窗口与滚动计算（Window &amp; Rolling）</td>
    <td>引入增量计算方式，优化内存访问模式与底层数据结构。</td>
    <td>提升固定窗口、可变窗口及扩展窗口（Rolling &amp; Expanding）场景下的边界生成、数值聚合与中位数计算效率。</td>
  </tr>
  <tr>
    <td>索引、合并与基础数据结构操作</td>
    <td>优化内存对齐与结果构造开销，加速查找与映射逻辑。</td>
    <td>提升DataFrame/Series构造、布尔索引、数据对齐及缺失值（NaN）处理效率。<br>降低RangeIndex、MultiIndex在数据合并merge与连接join中的对齐和查找开销。</td>
  </tr>
  <tr>
    <td>特殊数据类型加速（字符串、分类与时序）</td>
    <td>降低类型转换（Cast）开销，规避冗余的Python对象创建。</td>
    <td>字符串与分类：加速字符串拼接/处理，以及分类数据categorical的索引与统计。<br>时间序列：优化时间偏移、Timedelta/Datetime属性访问以及数据重采样（resample）路径。</td>
  </tr>
</tbody></table>

### 动态路由与上游兼容性

为确保优化后的pandas能在任何生产环境中安全替换上游版本，项目确立了严格的兼容性边界。

* API级兼容：保持与上游社区pandas的公共API、用户可见行为、异常处理和计算语义的一致性。
* 智能动态路由：优化实现会动态评估运行平台、数据类型和数据规模，自适应选择执行路径。

  * 平台条件：SwissTable后端在aarch64/arm64平台默认启用，其他平台默认关闭。

  * 类型条件：主要对数值类型（整数、浮点数等）生效，具体覆盖范围因算子而异。

  * 规模条件：部分算子设有数据规模阈值（如100万元素以内）。

  * 满足条件时：自动走SIMD/SwissTable高速路径；任一条件不满足时：自动回退（Fallback）至原有常规路径，保持原有的行为和顺序语义。

* 平台级隔离：针对ARM64/鲲鹏平台特定的底层实现，使用运行时检测（Runtime Detection）或独立路径进行隔离，不影响通用代码库。

### Benchmark性能验证体系

为保障优化成果的真实性与稳定性，项目建立了常态化性能监控。

* 测试工具：采用开源标准的ASV (Airspeed Velocity) Benchmark框架进行全量评估。

* 专项覆盖：专门针对鲲鹏服务器硬件特性、SwissTable算子性能以及典型的大数据处理工作负载定制了增量测试集。

* 质量闭环：测试结果不仅用于验证版本间的性能收益，更用于高敏感度地监控性能波动，及时识别并拦截任何可能的性能劣化（Regression）场景。

## 代码示例

SwissTable是本项目引入的实验性哈希表实现，用于加速成员判断（isin）、唯一值处理（unique）、去重（drop_duplicates）、分组以及连接等强依赖哈希运算的操作。该后端在aarch64/arm64平台默认启用，在其他平台默认关闭。

### 查看当前配置

用于检查当前运行环境下，pandas是否默认开启了SwissTable加速。默认值跟随运行平台：aarch64/arm64上默认为`True`，其他平台默认为`False`。

```python
import pandas as pd

pd.get_option("compute.use_swisstable")
```

### 临时局部切换

可以在`with`代码块内部配置临时启用或关闭SwissTable，退出代码块后自动恢复全局默认值。

```python
with pd.option_context("compute.use_swisstable", True):
    result = df["key"].isin(values)

with pd.option_context("compute.use_swisstable", False):
    result = df["key"].isin(values)
```

### 全局配置切换

在整个Python脚本执行以下代码，可以全局设置启用或关闭SwissTable，改变后续所有相关算子的默认行为。

```python
pd.set_option("compute.use_swisstable", True)
pd.set_option("compute.use_swisstable", False)
```
