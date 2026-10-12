# pandas 3.0.1 鲲鹏（ARM64）优化版使用指南

本指南说明如何在鲲鹏（ARM64）服务器上安装 boostkit/pandas 发布的优化版 wheel 包，并验证优化版本已成功生效。

发行版信息：

| 项目 | 内容 |
|---|---|
| 代码仓 | gitcode.com/boostkit/pandas |
| Release | `v3.0.1-poc` |
| wheel 文件 | `pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl` |
| 依赖 | numpy（建议配套使用 boostkit 优化版 numpy 2.4.3）、python-dateutil |
| 说明 | 面向 ARM64/鲲鹏平台优化关键计算路径，与上游 pandas API、行为、异常语义和数值结果兼容 |

> 本指南中所有命令均已在鲲鹏 920b 实机（AlmaLinux 9.4, aarch64）端到端验证通过。

## 1. 安装前环境检查

### 1.1 确认 CPU 架构为 ARM64

```bash
uname -m
```

预期输出：

```
aarch64
```

### 1.2 确认 Python 3.14 解释器可用（必需）

wheel 为 `cp314` 规格，**只能安装在 Python 3.14 上**。本指南统一使用 `python3.14` 命令（不修改系统已有的 `python` 命令指向），请先确认其可用：

```bash
python3.14 --version
# 预期输出: Python 3.14.x

python3.14 -m pip --version
```

若 `python3.14` 命令不存在或版本不对，任选一种方式获得 Python 3.14：

```bash
# 方式一（root）：安装 python3.14，提供 /usr/bin/python3.14 命令
dnf install -y python3.14

# 方式二（推荐，任何环境通用）：conda 创建 3.14 环境并激活
# 激活后 python 与 python3.14 均指向 3.14
conda create -n py314 python=3.14 -y
conda activate py314
```

> 本指南不覆盖、不改名系统已有的 `python` 命令（避免影响整机 Python 环境）。若你习惯使用 `python`，请在激活虚拟环境后再使用。

### 1.3 确认 glibc 版本 ≥ 2.34（必需）

```bash
ldd --version | head -1
```

预期输出（示例）：

```
ldd (GNU libc) 2.34
```

### 1.4 检查已有 numpy / pandas

pandas 依赖 numpy。**建议先安装 boostkit 优化版 numpy 2.4.3**（见《NumPy-2.4.3-鲲鹏优化版使用指南》），再安装优化版 pandas，保证整条链路均为优化构建：

```bash
python3.14 -m pip show numpy pandas
```

- 若已有旧版 pandas，按第 3 节卸载后再装，或直接使用 venv 隔离。

## 2. 下载 wheel 并校验完整性

本指南需要下载两个 wheel：**配套的优化版 numpy 2.4.3**（pandas 依赖它，必须使用优化版配套安装）和**优化版 pandas 3.0.1**。

### 2.1 下载配套的优化版 numpy wheel

```bash
mkdir -p ~/whl-install && cd ~/whl-install

# 下载 numpy wheel 与官方 sha256 校验文件
curl -fLO "https://gitcode.com/boostkit/numpy/releases/download/v2.4.3.0-rc2/numpy-2.4.3-cp314-cp314-manylinux_2_34_aarch64.whl"
curl -fLO "https://gitcode.com/boostkit/numpy/releases/download/v2.4.3.0-rc2/numpy-2.4.3-cp314-cp314-manylinux_2_34_aarch64.whl.sha256"

# 校验
sha256sum -c numpy-2.4.3-cp314-cp314-manylinux_2_34_aarch64.whl.sha256
```

预期输出：

```
numpy-2.4.3-cp314-cp314-manylinux_2_34_aarch64.whl: OK
```

### 2.2 下载优化版 pandas wheel

```bash
cd ~/whl-install

# 下载 wheel 与官方 sha256 校验文件
curl -fL -o "pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl" \
  "https://gitcode.com/boostkit/pandas/releases/download/v3.0.1-poc/pandas-3.0.1%20270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl"
curl -fL -o "pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl.sha256" \
  "https://gitcode.com/boostkit/pandas/releases/download/v3.0.1-poc/pandas-3.0.1%20270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl.sha256"

# 校验
sha256sum -c pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl.sha256
```

预期输出：

```
pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl: OK
```

## 3. 安装

### 方式 A（推荐）：venv 虚拟环境隔离安装

```bash
cd ~/whl-install

python3.14 -m venv pandas-env
source pandas-env/bin/activate

python --version          # 确认 3.14
python -m pip install --upgrade pip

# 安装 2.1 节下载的优化版 numpy wheel
python -m pip install numpy-2.4.3-cp314-cp314-manylinux_2_34_aarch64.whl

# 安装 2.2 节下载的优化版 pandas wheel（依赖 python-dateutil 会自动从 PyPI 获取）
python -m pip install "pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl"
```

> 关键：**先装优化版 numpy 再装 pandas**。若环境里没有 numpy，pip 会自动从 PyPI 拉取上游 numpy，导致 pandas 配套的是非优化版 numpy。若需要完全离线/固定依赖，可加 `--no-deps` 后自行安装 python-dateutil。

### 方式 B：卸载旧版后直接安装

```bash
python3.14 -m pip uninstall -y pandas
python3.14 -m pip install ~/whl-install/numpy-2.4.3-cp314-cp314-manylinux_2_34_aarch64.whl   # 确保配套优化版 numpy
python3.14 -m pip install "~/whl-install/pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl"
```

## 4. 验证安装成功

### 4.1 版本检查（核心）

```bash
python3.14 - <<'EOF'
import sys
print("python :", sys.version.split()[0])
import numpy, pandas
print("numpy  :", numpy.__version__)
print("pandas :", pandas.__version__)
assert numpy.__version__ == "2.4.3"
from numpy.version import git_revision
assert git_revision == "558304423d330034cfdc40b1f55175b4675d437c"   # 配套优化版 numpy 的制品源码校验
assert pandas.__version__.startswith("3.0.1")   # 实际为 3.0.1+270.g5a98f9ba40
print("VERSION_CHECK_OK")
EOF
```

预期输出：

```
python : 3.14.4
numpy  : 2.4.3
pandas : 3.0.1+270.g5a98f9ba40
VERSION_CHECK_OK
```

### 4.2 构建信息确认

`pandas.show_versions()` 会打印构建时的源码 commit，与 Release 基线提交比对即可确认：

```bash
python3.14 -c "import pandas; pandas.show_versions()"
```

关键确认点（已实测样例）：

```
INSTALLED VERSIONS
------------------
commit                : 5a98f9ba4026b41df4aa2babb0bd2dd840ae4c7b   ← 与 Release 基线提交一致
python                : 3.14.4
machine               : aarch64
processor             : aarch64
```

`commit == 5a98f9ba4026...` 且 `machine == aarch64`，说明安装的是鲲鹏优化构建。

### 4.3 确认安装的 wheel 平台标签

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

### 4.4 功能正确性冒烟 + 性能参考

```bash
python3.14 - <<'EOF'
import numpy as np, pandas as pd, time

rng = np.random.default_rng(42)

# 正确性冒烟
df = pd.DataFrame({"k": ["a","b","a","c","b"]*200, "v": range(1000)})
g = df.groupby("k")["v"].sum()
assert g["a"] == sum(i for i in range(1000) if i % 5 in (0, 2))          # groupby
m = df.merge(df, on="k", suffixes=("_l","_r"))
assert len(m) == 400*400 + 400*400 + 200*200                             # merge
assert df.pivot_table(index="k", values="v", aggfunc="mean").shape == (3,1)
d2 = pd.DataFrame({"x": rng.standard_normal(100_000)})
assert abs(d2["x"].rolling(100).mean().iloc[-1] - d2["x"].iloc[-100:].mean()) < 1e-12   # rolling
print("CORRECTNESS_SMOKE_OK")

# 性能参考（记录基准，便于对比优化效果）
big = pd.DataFrame({"k": rng.integers(0, 1000, 5_000_000),
                    "v": rng.standard_normal(5_000_000)})
t0 = time.perf_counter(); big.groupby("k")["v"].sum(); t1 = time.perf_counter()
t2 = time.perf_counter(); big["v"].rolling(10).mean();   t3 = time.perf_counter()
print(f"groupby-sum(5e6) : {1000*(t1-t0):.1f} ms")
print(f"rolling-mean(5e6): {1000*(t3-t2):.1f} ms")
EOF
```

预期输出（耗时因负载而异）：

```
CORRECTNESS_SMOKE_OK
groupby-sum(5e6) : 39.8 ms      # 920b 实机参考值
rolling-mean(5e6): 18.8 ms      # 920b 实机参考值
```

## 5. 常见问题

| 现象 | 原因与处理 |
|---|---|
| `python3.14 --version` 不是 3.14.x 或命令不存在 | 未安装 3.14。按第 1.2 节安装 `python3.14`（方式一）或使用 conda 环境（方式二）。 |
| `ERROR: ... not a supported wheel on this platform` | Python 版本不是 3.14，或架构不是 aarch64。按第 1 节重新检查。 |
| `sha256sum -c` 文件名不匹配 | 下载文件名是空格版（`pandas-3.0.1 270...`），需重命名为带 `+` 的规范名（见第 2 节）。 |
| 安装 pandas 时拉取了上游 numpy | 环境里原本没有 numpy。**先装优化版 numpy 2.4.3 再装 pandas**（第 3 节方式 A）。 |
| 4.1 节 numpy `git_revision` 断言失败 | 安装的不是 boostkit numpy Release 发布制品（可能装了上游 numpy）。重新执行第 2.1、3 节。 |
| `pandas.__version__` 与 3.0.1 不完全一致 | 优化版带本地构建号，显示为 `3.0.1+270.g5a98f9ba40`，属正常；判断时用 `startswith("3.0.1")`。 |
| 误执行 `pip install -U pandas/numpy` 导致性能回退 | 该命令会从 PyPI 拉取上游版本覆盖优化版，请重新执行第 3 节安装。 |
| glibc/libgomp 相关加载错误 | 系统 glibc < 2.34，需升级操作系统或更换满足 manylinux_2_34 的环境。 |

## 6. 卸载

```bash
python3.14 -m pip uninstall -y pandas numpy   # 方式 B 安装时
# 或（方式 A）：直接删除虚拟环境
deactivate && rm -rf ~/whl-install/pandas-env
```
