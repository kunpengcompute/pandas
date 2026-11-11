# 版本说明书

## 版本配套说明

<table style="undefined;table-layout: fixed; width: 500px"><colgroup>
<col style="width: 250px">
<col style="width: 250px">
</colgroup>
<thead>
  <tr>
    <th>产品</th>
    <th>版本信息</th>
  </tr></thead>
<tbody>
  <tr>
    <td>产品名称</td>
    <td>Kunpeng BoostKit</td>
  </tr>
  <tr>
    <td>产品版本</td>
    <td>3.0.1-poc</td>
  </tr>
  <tr>
    <td>wheel文件</td>
    <td>pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl</td>
  </tr>
</tbody>
</table>

## 软件版本配套信息

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

## 版本更新说明

### 更新说明

无

### 已解决的问题

无

### 遗留问题

无

## 版本配套文档

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

## 修订记录

| 日期 | 修改内容 | 变更原因 | 
| --- | --- | --- | 
| 2026-10-31 | 新增源码构建指南、快速入门、安装指南、用户指南。 | 第一次正式发布。 |
