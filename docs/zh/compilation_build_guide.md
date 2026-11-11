# 源码构建指南

本文档介绍Pandas 3.0.1鲲鹏加速版的源码构建流程，涵盖工具链与构建依赖准备、注入鲲鹏编译优化参数、可编辑模式编译、单元测试与制品打包、以及ASV性能测试，您可以定制C扩展，并适配当前鲲鹏处理器的矢量指令集。

## 工具链要求

- 已安装C++17的编译器，例如GCC 12.3及以上或者Clang 12及以上。
- Python 3.14.3
- Python-Devel包：openEuler/RHEL系安装`python3-devel`，Debian/Ubuntu系安装`python3-dev`

## 安装依赖

```bash
# 拉取源码
git clone https://gitcode.com/boostkit/pandas.git

# 安装依赖
pip install asv build ninja Cython==3.2.4 matplotlib==3.11.1 sqlalchemy==2.0.51 scipy==1.17.1 numba==0.66.0 numexpr==2.14.1 pyarrow==24.0.0 openpyxl==3.1.5 xlsxwriter==3.2.9 odfpy==1.4.1 jinja2==3.1.6 meson==1.11.1 meson-python==0.19.0 numpy==2.4.3 python-dateutil versioneer[toml] hypothesis "pytest<9" pytest-cov pytest-xdist coverage patchelf auditwheel
```

## 可编辑模式编译

进入源码目录并执行可编辑安装。

```bash
# 新增tag
git config --local user.email "you@example.com"
git config --local user.name "Your Name"
git tag -a v3.0.1.1 HEAD -m "v3.0.1.1"

# 编译命令
python -m pip install -e . --no-build-isolation
```

预期输出：

```output
Looking in indexes: https://mirrors.tools.huawei.com/pypi/simple/
Obtaining file:///root/pandas/pandas
Checking if build backend supports build_editable ... done
Preparing editable metadata (pyproject.toml) ... done
Requirement already satisfied: numpy>=2.3.3 in /home/envs/conda/py314/lib/python3.14/site-packages (from pandas==3.0.1.1) (2.4.3)
Requirement already satisfied: python-dateutil>=2.8.2 in /home/envs/conda/py314/lib/python3.14/site-packages (from pandas==3.0.1.1) (4.0.0)
Requirement already satisfied: tzdata in /home/envs/conda/py314/lib/python3.14/site-packages (from python-dateutil>=2.8.2->pandas==3.0.1.1) (2026.6)
Building wheels for collected packages: pandas
Building editable for pandas (pyproject.toml) ... done
Created wheel for pandas: filename=pandas-3.0.1.1-cp314-cp314-linux_aarch64.whl size=12906 sha256=511d35396d06745844b603a1b0c7ebca75a744a8eb719a2ef4ea0d47b2b376e1
Stored in directory: /tmp/pip-ephem-wheel-cache-vy7uwjjf/wheels/7d/b4/6e/9ade3714bd517dbdf1921521d3763019e2f96f79011f974cd2
Successfully built pandas
Installing collected packages: pandas
Attempting uninstall: pandas
Found existing installation: pandas 3.0.1+270.g5a98f9ba40
Uninstalling pandas-3.0.1+270.g5a98f9ba40:
Successfully uninstalled pandas-3.0.1+270.g5a98f9ba40
Successfully installed pandas-3.0.1.1
```

## 单元测试

成功编译并安装后，建议运行以下测试以验证本地构建是否正确。运行基础功能测试，跳过依赖网络、数据库、剪贴板和绘图环境的测试。

### 大规模并发筛选测试

进行全包验证时，使用常规测试命令。

```bash
pytest pandas -n 4 -m "not network and not db and not clipboard" --ignore=pandas/tests/plotting
```

### 单点测试

定位具体问题或验证核心计算性能时，使用精准测试命令。

```bash
pytest pandas/tests/arithmetic/test_numeric.py
```

预期输出：

```output
rootdir: /root/pandas
configfile: pyproject.toml
plugins: hypothesis-6.170.15, platformdirs-4.14.5, cov-7.1.0, xdist-3.8.0
collected 3142 items

pandas/tests/arithmetic/test_numeric.py ........................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss......ss........................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................s..s.....s..s...............................................................................................................................................................................................................................................................................................................................................................................................................................................................................................

----------------------------------------------------------------------- generated xml file: /root/pandas/pandas/test-data.xml -----------------------------------------------------------------------
======================================================================================= slowest 30 durations ========================================================================================
0.02s teardown pandas/tests/arithmetic/test_numeric.py::test_series_add_sub_with_UInt64[python]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestAdditionSubtraction::test_frame_operators[numexpr]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestAdditionSubtraction::test_frame_operators[python]
0.01s call pandas/tests/arithmetic/test_numeric.py::test_empty_str_comparison[numexpr-0-5]
0.01s call pandas/tests/arithmetic/test_numeric.py::test_empty_str_comparison[numexpr-1-5]
0.01s call pandas/tests/arithmetic/test_numeric.py::test_empty_str_comparison[numexpr-2-5]
0.01s call pandas/tests/arithmetic/test_numeric.py::test_empty_str_comparison[python-0-5]
0.01s call pandas/tests/arithmetic/test_numeric.py::test_empty_str_comparison[numexpr-5-5]
0.01s call pandas/tests/arithmetic/test_numeric.py::test_empty_str_comparison[python-5-5]
0.01s call pandas/tests/arithmetic/test_numeric.py::test_empty_str_comparison[python-2-5]
0.01s call pandas/tests/arithmetic/test_numeric.py::test_empty_str_comparison[python-1-5]
0.01s call pandas/tests/arithmetic/test_numeric.py::test_sub_multiindex_swapped_levels[numexpr]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestMultiplicationDivision::test_ops_np_scalar[numexpr-nan]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestMultiplicationDivision::test_ops_np_scalar[numexpr-7]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestMultiplicationDivision::test_ops_np_scalar[numexpr--23]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestMultiplicationDivision::test_ops_np_scalar[python--23]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestMultiplicationDivision::test_ops_np_scalar[numexpr--3.14]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestMultiplicationDivision::test_ops_np_scalar[numexpr-2.718]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestMultiplicationDivision::test_ops_np_scalar[numexpr-inf]
0.01s call pandas/tests/arithmetic/test_numeric.py::test_sub_multiindex_swapped_levels[python]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestMultiplicationDivision::test_ops_np_scalar[python-7]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestMultiplicationDivision::test_ops_np_scalar[python-2.718]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestMultiplicationDivision::test_ops_np_scalar[python-inf]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestMultiplicationDivision::test_ops_np_scalar[python--3.14]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestMultiplicationDivision::test_ops_np_scalar[python-nan]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestAdditionSubtraction::test_datetime64_with_index[numexpr]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestDivisionByZero::test_divmod_zero[numexpr-zero5-Index1]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestNumericArithmeticUnsorted::test_binops_index_scalar[numexpr-2-idx3-mul]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestNumericComparisons::test_df_numeric_cmp_dt64_raises[numexpr-DataFrame]
0.01s call pandas/tests/arithmetic/test_numeric.py::TestNumericArraylikeArithmeticWithDatetimeLike::test_add_sub_datetimedeltalike_invalid[numexpr-Index2-Index-datetime.timedelta(days=1, seconds=25200)]
================================================================================= 3066 passed, 76 skipped in 7.68s ==================================================================================
```
