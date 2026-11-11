# 快速入门

本指南帮助您快速完成鲲鹏加速版pandas的部署，并通过一个典型的数据分析场景体验pandas百兆级数据的极速处理能力。

## 安装pandas

本指南以conda虚拟环境为例，快速安装部署pandas。

```bash
# 创建并激活纯净的Python 3.14环境
conda create -n py314 python=3.14 -y && conda activate py314

# 创建目录
mkdir -p ~/whl-install && cd ~/whl-install

# 一键下载高性能numpy和pandas软件包
curl -fLO -k "https://gitcode.com/boostkit/numpy/releases/download/v2.4.3.0-rc2/numpy-2.4.3-cp314-cp314-manylinux_2_34_aarch64.whl"
curl -fL -k -o "pandas-3.0.1 270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl" \
"https://gitcode.com/boostkit/pandas/releases/download/v3.0.1-poc/pandas-3.0.1%20270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl"
mv "pandas-3.0.1 270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl" pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl

# 严格遵循顺序安装（先安装numpy，再安装pandas）
python -m pip install numpy-2.4.3-cp314-cp314-manylinux_2_34_aarch64.whl
python -m pip install pandas-3.0.1+270.g5a98f9ba40-cp314-cp314-manylinux_2_34_aarch64.whl
```

## 核心业务体验

安装完成后，通过一段标准的高频业务代码，体验鲲鹏加速算子的能力。

1. 创建`demo.py`文件并运行。

    ```cmd
    touch demo.py
    python demo.py
    ```

2. 打开`demo.py`文件。

    ```cmd
    vi demo.py
    ```

3. 复制以下示例代码到`demo.py`文件中。

    ```python
    import numpy as np
    import pandas as pd

    # 模拟生成一个100万行的用户消费数据集
    print("正在生成百万级测试数据...")
    rng = np.random.default_rng(42)
    df = pd.DataFrame({
        "user_id": rng.integers(10000, 99999, 1_000_000),
        "category": rng.choice(["Electronics", "Clothing", "Books", "Home"], 1_000_000),
        "spend": rng.exponential(scale=50.0, size=1_000_000)
    })

    # 使用鲲鹏加速算子进行高性能分组聚合（Groupby + Sum）
    print("正在执行鲲鹏优化算子分析...")
    result = df.groupby("category")["spend"].sum()

    # 打印分析结果
    print("\n统计结果成功输出：")
    print(result)
    ```

4. 输入”:wq"保存并退出编辑。

5. 查看返回信息，确认运行成功。

    ```cmd
    统计结果成功输出：
    category
    Books          1.248620e+07
    Clothing       1.251537e+07
    Electronics    1.245945e+07
    Home           1.250805e+07
    Name: spend, dtype: float64
    ```
