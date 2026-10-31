# 安装部署指南

本指南说明如何在适合的环境中快速体验pandas鲲鹏ARM64优化版。

## 配套版本<a id="配套版本"></a>

| 项目 | 内容 |
|---|---|
| 代码仓 | gitcode.com/boostkit/pandas |
| Release | `v3.0.1-poc` |
| wheel文件 | `pandas-3.0.1 270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl` |
| 依赖 | NumPy（建议配套使用Boostkit优化版NumPy 2.4.3）、python-dateutil |
| 说明 | 面向ARM64/鲲鹏平台优化关键计算路径，与上游pandas API、行为、异常语义和数值结果兼容 |

## 安装前环境检查

在配置软件前，请确保您的系统底层硬件与核心系统库满足环境要求。

1. 确认CPU架构为ARM64。

    ```bash
    uname -m
    ```

    预期输出：

    ```output
    aarch64
    ```

2. 确认glibc版本大于或等于2.34。

    ```bash
    ldd --version | head -1
    ```

    预期输出示例：

    ```output
    ldd (GNU libc) 2.34
    ```

3. 确认Python 3.14解释器可用。

    wheel为`cp314`规格，只能安装在Python 3.14上。本指南统一使用`python3.14`命令。但不会强行把系统原本默认的`python` 命令改成指向`python3.14`。

    1. 执行以下命令，确认系统是否安装python 3.14和第三方工具pip。

        ```bash
        python3.14 --version
        python3.14 -m pip --version
        ```

        预期输出示例：

        ```output
        Python 3.14.x
        pip 26.x.x from /home/envs/conda/py314/lib/python3.14/sit-packages/pip (python 3.14)
        ```

        - 若输出示例如上，表示系统已成功安装python 3.14和pip工具。
        - 若`python3.14`命令不存在或版本不对，执行以下步骤获得Python 3.14。

    2. 安装python 3.14。

        conda环境隔离是在系统里开启一个独立的虚拟空间。激活这个空间后，系统会将默认的`python`指向`python3.14`。适用于开发者服务器中存在多个不同Python项目且没有root权限的场景。这种安装方式，不影响外部环境，激活后可直接使用简写命令，随时可以一键彻底删除。

        ```bash
        conda create -n py314 python=3.14 -y
        conda activate py314
        ```

## 获取软件包<a id="获取软件包"></a>

1. 在终端执行以下命令，强制卸载可能引发版本冲突的公网原生包。

    如果您此前在全局环境安装过普通版本的NumPy或pandas，请先执行静默卸载。若无旧版系统会自动跳过。
  
    ```bash
    python3.14 -m pip uninstall -y pandas numpy
    ```

2. 创建离线工作目录，将NumPy与pandas的加速包及官方SHA256校验文件下载至本地。

    ```bash
    # 创建并进入统一的工作目录
    mkdir -p ~/whl-install && cd ~/whl-install

    # 一键下载NumPy 2.4.3优化包及校验文件
    curl -fLO -k "https://gitcode.com/boostkit/numpy/releases/download/v2.4.3.0-rc2/numpy-2.4.3-cp314-cp314-manylinux_2_34_aarch64.whl"
    curl -fLO -k "https://gitcode.com/boostkit/numpy/releases/download/v2.4.3.0-rc2/numpy-2.4.3-cp314-cp314-manylinux_2_34_aarch64.whl.sha256"

    #  一键下载pandas 3.0.1优化包及校验文件
    curl -fL -k -o "pandas-3.0.1 270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl" \
      "https://gitcode.com/boostkit/pandas/releases/download/v3.0.1-poc/pandas-3.0.1%20270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl"
    curl -fL -k -o "pandas-3.0.1 270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl.sha256" \
      "https://gitcode.com/boostkit/pandas/releases/download/v3.0.1-poc/pandas-3.0.1%20270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl.sha256"
      mv "pandas-3.0.1 270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl" pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl
      mv "pandas-3.0.1 270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl.sha256" pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl.sha256
    ```

3. 验证安装包完整性。

    ```bash
    sha256sum -c numpy-2.4.3-cp314-cp314-manylinux_2_34_aarch64.whl.sha256
    sha256sum -c pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl.sha256
    ```
    
    预期输出：

    ```bash
    numpy-2.4.3-cp314-cp314-manylinux_2_34_aarch64.whl: OK
    pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl: OK
    ```
    
## 部署方案

- 本地化环境部署（深度定制）
    - 性能增强：直接在物理机或虚拟机运行，减少容器层的虚拟化开销，适合追求极致生产性能的业务。
    - 适用场景：物理服务器或虚拟机上的生产环境、需要多项目隔离的开发机。

- 云原生容器部署（极速通道）

    - 一秒即用：无需处理任何复杂的依赖关系和下载校验，官方镜像已内置全部环境。
    - 适用场景：单元测试（UT）、开发验证、K8s集群部署。

### 本地化部署<a id="本地化部署"></a>

请务必先安装优化版NumPy，再安装pandas。如果颠倒顺序，pip会自动从公网PyPI仓库拉取未优化的上游原生NumPy，导致整个鲲鹏加速链路失效。以下操作示例使用conda虚拟环境。

```bash
# 创建并激活专用的Python 3.14环境
conda create -n py314 python=3.14 -y && conda activate py314

# 执行流水线安装
mkdir -p ~/whl-install && cd ~/whl-install
python -m pip install --upgrade pip
python -m pip install numpy-2.4.3-cp314-cp314-manylinux_2_34_aarch64.whl
python -m pip install pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl
```

### 云原生容器化部署

对于习惯使用容器或在K8s集群中部署的用户，可以使用Docker镜像。该镜像内置了编译完成的鲲鹏优化版pandas、NumPy以及全套开发工具链，实现即开即用。

1. 请在已安装Docker的鲲鹏服务器上执行以下命令，直接从华为云SWR镜像仓库拉取官方专属镜像。

    ```shell
    docker pull swr.cn-north-4.myhuaweicloud.com/cloud_boostkit/openeuler22.03_lts_sp3:pandas-3.0.1
    ```

2. 先启动并进入容器，再初始化容器环境。

    ```shell
    # 运行并进入容器

    docker run -it --name pandas-3.0.1 \
    swr.cn-north-4.myhuaweicloud.com/cloud_boostkit/openeuler22.03_lts_sp3:pandas-3.0.1 \
    /bin/bash

    # 加载conda环境管理脚本
    source /opt/miniforge3/etc/profile.d/conda.sh

    # 激活专门针对鲲鹏加速版优化的专属沙盒环境
    conda activate pandas_930

    # 导出高性能GCC 12编译器路径。确保底层加速算子正常调度。
    export PATH=/opt/rh/gcc-toolset-12/root/usr/bin:$PATH
    ```

    镜像中预装的`pandas_930`是一个专门定制的Conda环境，内部包含了完整的构建组件与测试依赖。推荐用于功能测试（UT）、性能基准压测以及开发验证场景。

3. 下载和安装命令，请参见[本地化部署](#本地化部署)。

## 验证性能

安装完成后，请在激活环境后在终端验证性能。

### 检查版本

```bash
python3.14 - <<'EOF'
import sys
print("python :", sys.version.split()[0])
import numpy, pandas
print("numpy  :", numpy.__version__)
print("pandas :", pandas.__version__)
assert numpy.__version__ == "2.4.3"
from numpy.version import git_revision
assert git_revision == "558304423d330034cfdc40b1f55175b4675d437c"   # 配套优化版NumPy的制品源码校验
assert pandas.__version__.startswith("3.0.1")   # 实际为3.0.1+270.g5a98f9ba40
print("VERSION_CHECK_OK")
EOF
```

预期输出：

```output
python : 3.14.3
numpy  : 2.4.3
pandas : 3.0.1+270.g5a98f9ba40
VERSION_CHECK_OK
```

### 确认构建信息

为了确保您安装的pandas是经过鲲鹏BoostKit深度加速优化的版本，而非从公网下载的普通开源版本，您可以通过检查源码提交哈希值Commit ID来进行最终审计。

```bash
python3.14 -c "import pandas; pandas.show_versions()"
```

输出关键确认点：

```output
INSTALLED VERSIONS
------------------
commit                : 5a98f9ba4026b41df4aa2babb0bd2dd840ae4c7b   ← 与 Release 基线提交一致
python                : 3.14.3
machine               : aarch64
processor             : aarch64
```

`pandas.show_versions()`会打印构建时的源码commit，与Release基线提交比对即可确认。`commit == 5a98f9ba4026...`且`machine == aarch64`，说明安装的是鲲鹏优化构建。

### 确认安装的wheel平台标签

为了防止开发人员误用公网常规开源版本覆盖掉高性能构建，请复制并运行以下命令。该脚本将通过静态读取元数据的方式，强制审计NumPy和pandas的构建标签。

```bash
python3.14 - <<'EOF'
import importlib.metadata as im
for dist in ("numpy", "pandas"):
    tag = [l.split(": ")[1] for l in im.distribution(dist).read_text("WHEEL").splitlines() if l.startswith("Tag:")][0]
    print(dist, "wheel tag:", tag)
    assert tag == "cp314-cp314-manylinux_2_34_aarch64"
print("WHEEL_TAG_OK")
EOF
```

- 如果终端完整输出`WHEEL_TAG_OK`，说明构建标签正确。
- 如果触发`AssertionError`报错，说明当前环境引入了非鲲鹏加速版本的第三方包，请执行环境清理命令并重新安装。

## 自动化性能基准测试

请将以下命令完整复制并粘贴到您的终端中运行。本脚本将自动对安装后的pandas进行以下检查。

- 正确性校验：通过断言机制，确保核心数据算子功能100%正常。

- 性能基准测试：在500万行大数据集上执行性能压测，并输出耗时。

```bash
# 安装测试需要的依赖
pip install asv openpyxl python-dateutil tzdata matplotlib sqlalchemy scipy odfpy
# 注册机器硬件信息
asv machine --yes
# 切换到测试基准工作目录
cd pandas/asv_bench
# 获取指定版本的git提交哈希值
OPT_HASH=$(git rev-parse v3.0.1-poc)
# 启动性能基准测试
asv run -b "^custom_case" -E existing --set-commit-hash $OPT_HASH
```

预期输出：

```output
· Discovering benchmarks
· Running 13 total benchmarks (1 commits * 1 environments * 13 benchmarks)
[ 0.00%] · For pandas commit 632052a1 :
[ 0.00%] ·· Building for existing-py_home_envs_conda_py314_bin_python
[ 0.00%] ·· Benchmarking existing-py_home_envs_conda_py314_bin_python
[ 3.85%] ··· Running (custom_case.ApplyRowwise.time_apply_rowwise--)...
[15.38%] ··· Running (custom_case.GroupByAggregation.time_groupby_agg--)..
[23.08%] ··· Running (custom_case.MergeUser.time_merge_user--)..
[30.77%] ··· Running (custom_case.PivotCrosstab.time_pivot_table--)..
[38.46%] ··· Running (custom_case.StringCategorical.time_to_categorical--)..
[46.15%] ··· Running (custom_case.TimeSeriesResampleRolling.time_resample--)..
[53.85%] ··· custom_case.ApplyRowwise.time_apply_rowwise 4.26±0.01s
[57.69%] ··· custom_case.ApplyVectorized.time_vectorized 76.7±0.7ms
[61.54%] ··· custom_case.DataFrameGeneration.time_generate_dataframe 2.01±0.03s
[65.38%] ··· custom_case.GroupByAggregation.time_groupby_agg 2.30±0s
[69.23%] ··· custom_case.MergeCategory.time_merge_category 130±0.7ms
[73.08%] ··· custom_case.MergeUser.time_merge_user 273±1ms
[76.92%] ··· custom_case.PivotCrosstab.time_crosstab 1.41±0.03s
[80.77%] ··· custom_case.PivotCrosstab.time_pivot_table 842±5ms
[84.62%] ··· custom_case.StringCategorical.time_string_ops 902±20ms
[88.46%] ··· custom_case.StringCategorical.time_to_categorical 925±3ms
[92.31%] ··· custom_case.StringCategorical.time_value_counts 13.4±0.05ms
[96.15%] ··· custom_case.TimeSeriesResampleRolling.time_resample 253±1ms
[100.00%] ··· custom_case.TimeSeriesResampleRolling.time_rolling_24h 325±2μs
```

## 环境清理与卸载

如果您需要将系统彻底恢复至安装前的纯净状态，请根据您之前选择的安装路径执行对应的清理指令。

### Conda虚拟环境的卸载方式

```bash
# 退出当前虚拟环境并彻底销毁它
conda deactivate
conda remove -n py314 --all -y
# 可选：清理下载目录
rm -rf ~/whl-install
```

### 容器环境部署清理与卸载

容器环境的清理分为两个层次：停止并销毁运行中的容器，以及删除下载的官方镜像。

1. 在容器的交互式终端内，执行`exit`退出容器。
    
2. 在宿主机终端执行以下命令，停止并销毁当前容器实例。
        
    ```bash
    #  查找正在运行或已退出的pandas容器的ID
    docker ps -a | grep pandas-3.0.1

    # 停止并强制删除该容器实例（假设容器ID或名称为pandas_test）
    docker rm -f pandas_test
    ```

3. 删除官方预构建镜像。

    如果您后续不再需要进行测试或开发，可以彻底删除拉取的华为云SWR镜像，以释放数GB的磁盘空间。

    ```bash
    # 删除pandas 3.0.1官方镜像
    docker rmi swr.cn-north-4.myhuaweicloud.com/cloud_boostkit/openeuler22.03_lts_sp3:pandas-3.0.1
    ```

4. 一键清理容器残留卷与缓存。

    Docker在运行过程中可能会产生一些未挂载的匿名数据卷或缓存，执行以下命令可确保宿主机“零垃圾残留”。

    ```bash
    docker volume prune -f
    ```

## 常见问题

| 现象 | 原因与处理 |
|---|---|
| `python3.14 --version`不是3.14.x或命令不存在 | 未安装3.14。请参见[安装前环境检查](#安装前环境检查)。|
| `ERROR: ... not a supported wheel on this platform` | Python版本不是3.14，或架构不是aarch64。请参见[安装前环境检查](#安装前环境检查)。|
| `sha256sum -c`文件名不匹配 | 下载文件名是空格版（`pandas-3.0.1 270...`），需重命名为带 `+` 的规范名。请参见[配套版本](#配套版本)。|
| 安装pandas时拉取了上游NumPy | 环境里原本没有NumPy。先装优化版NumPy 2.4.3，再安装 pandas。请参见[本地化部署](#本地化部署)。|
| numpy `git_revision` 断言失败 | 安装的不是Boostkit NumPy Release发布制品，可能装了上游NumPy。请参见[获取软件包](#获取软件包)。|
| `pandas.__version__` 与3.0.1不完全一致 | 优化版带本地构建号，显示为`3.0.1+270.g5a98f9ba40`，属正常；判断时用`startswith("3.0.1")`。|
| 误执行`pip install -U pandas/numpy`导致性能回退 | 该命令会从PyPI拉取上游版本覆盖优化版，请重新执行[本地化部署](#本地化部署)。|
| glibc/libgomp相关加载错误 | 系统glibc小于2.34，需升级操作系统或更换满足manylinux_2_34的环境。|
