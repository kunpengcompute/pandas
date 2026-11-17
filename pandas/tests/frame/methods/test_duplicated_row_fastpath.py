"""
Tests for the AArch64 row-wise fastpath of DataFrame.duplicated.

The fastpath hashes whole rows as tuples of canonical 64-bit values instead of
factorizing every column and hashing the combined codes, so it must produce
exactly the same mask as the generic implementation.
"""

import sys

import numpy as np
import pytest

import pandas as pd
from pandas import (
    DataFrame,
    NaT,
    Timestamp,
    Timedelta,
    date_range,
)
import pandas._testing as tm
from pandas._libs import swisstable
from pandas.core import (
    algorithms,
    frame,
)

N = 2048


@pytest.fixture(autouse=True)
def force_row_kernel(monkeypatch):
    # The fastpath is AArch64-only; enable it everywhere so the parity tests
    # also run on the other platforms pandas supports.
    monkeypatch.setattr(frame, "IS_ARM", True, raising=False)
    monkeypatch.setattr(algorithms, "IS_ARM", True, raising=False)
    with pd.option_context("compute.use_swisstable", True):
        yield


def _generic_duplicated(df, keep, subset=None):
    """DataFrame.duplicated without the row kernel."""
    with pd.option_context("compute.use_swisstable", False):
        return df.duplicated(subset=subset, keep=keep)


def _frame(n=N, seed=0):
    rng = np.random.default_rng(seed)
    return DataFrame(
        {
            "a": rng.integers(-3, 3, n),
            "b": rng.integers(0, 3, n).astype("int8"),
            "c": rng.integers(0, 2, n).astype(bool),
        }
    )


def _column_cases():
    idx = np.arange(N) % 7
    return {
        "bool": idx % 2 == 0,
        "int8": idx.astype("int8"),
        "uint64": idx.astype("uint64"),
        "float32": (idx / 4).astype("float32"),
        "float64": idx / 4,
        "datetime64[ns]": date_range("2020-01-01", periods=7, freq="D")[idx],
        "timedelta64[ns]": (Timedelta("1s") * np.arange(7))[idx],
        "datetime64[ns, UTC]": date_range(
            "2020-01-01", periods=7, freq="D", tz="UTC"
        )[idx],
    }


def test_frame_duplicated_uses_row_kernel(monkeypatch):
    calls = []
    original = swisstable.duplicated_rows

    def spy(columns, is_float, keep="first"):
        calls.append((len(columns), keep))
        return original(columns, is_float, keep=keep)

    monkeypatch.setattr(swisstable, "duplicated_rows", spy)

    df = _frame()
    df.duplicated()

    assert calls == [(3, "first")]


@pytest.mark.parametrize("keep", ["first", "last", False])
@pytest.mark.parametrize("name", list(_column_cases()))
def test_row_kernel_matches_generic_by_dtype(monkeypatch, name, keep):
    df = DataFrame({"x": _column_cases()[name], "y": np.arange(N) % 3})

    calls = []
    original = swisstable.duplicated_rows

    def spy(columns, is_float, keep="first"):
        calls.append(1)
        return original(columns, is_float, keep=keep)

    monkeypatch.setattr(swisstable, "duplicated_rows", spy)
    result = df.duplicated(keep=keep)

    assert calls, f"{name} did not take the row kernel"
    tm.assert_series_equal(result, _generic_duplicated(df, keep))


@pytest.mark.parametrize("keep", ["first", "last", False])
def test_row_kernel_nan_and_negative_zero(keep):
    df = DataFrame(
        {
            "f": [0.0, -0.0, np.nan, np.nan, 0.0, 1.0] * (N // 6),
            "t": [
                Timestamp("2020-01-01"),
                NaT,
                Timestamp("2020-01-02"),
                NaT,
                Timestamp("2020-01-01"),
                Timestamp("2020-01-02"),
            ]
            * (N // 6),
            "i": [0, 0, -1, -1, 0, 2] * (N // 6),
        }
    )
    result = df.duplicated(keep=keep)

    tm.assert_series_equal(result, _generic_duplicated(df, keep))


def test_row_kernel_duplicate_labels_and_subset():
    df = DataFrame(
        {
            "a": [1, 1, 2, 2] * (N // 4),
            "b": [1, 2, 3, 4] * (N // 4),
            "c": 0,
        }
    )
    for subset in (None, ["a"], ["a", "b"], ["c", "a"]):
        for keep in ("first", "last", False):
            result = df.duplicated(subset=subset, keep=keep)
            tm.assert_series_equal(
                result, _generic_duplicated(df, keep, subset=subset)
            )

    dup_labels = DataFrame(np.arange(3 * N).reshape(N, 3), columns=["a", "a", "b"])
    for keep in ("first", "last", False):
        tm.assert_series_equal(
            dup_labels.duplicated(keep=keep), _generic_duplicated(dup_labels, keep)
        )


@pytest.mark.parametrize(
    "values",
    [
        ["a", "b"] * (N // 2),
        pd.array(["a", "b"] * (N // 2), dtype="string"),
        pd.Categorical(["a", "b"] * (N // 2)),
        pd.array([1, 2] * (N // 2), dtype="Int64"),
    ],
    ids=["object", "string", "categorical", "masked"],
)
def test_frame_duplicated_falls_back_for_unsupported_dtypes(monkeypatch, values):
    def forbidden(*args, **kwargs):
        pytest.fail("row kernel used for an unsupported dtype")

    monkeypatch.setattr(swisstable, "duplicated_rows", forbidden)

    df = DataFrame({"a": values, "b": np.arange(len(values))})
    result = df.duplicated()

    tm.assert_series_equal(result, _generic_duplicated(df, "first"))


def test_frame_duplicated_invalid_keep():
    df = _frame()
    with pytest.raises(ValueError, match="keep must be"):
        df.duplicated(keep="invalid")


def test_row_kernel_requires_arm(monkeypatch):
    monkeypatch.setattr(algorithms, "IS_ARM", False)

    df = _frame()
    columns = [df["a"].values, df["b"].values]

    assert algorithms.duplicated_rows_swisstable(columns) is None
    tm.assert_series_equal(df.duplicated(), _generic_duplicated(df, "first"))


def test_row_kernel_requires_swisstable_option():
    df = _frame()
    columns = [df["a"].values, df["b"].values]

    with pd.option_context("compute.use_swisstable", False):
        assert algorithms.duplicated_rows_swisstable(columns) is None


@pytest.mark.parametrize("ncols", [1, 9])
def test_row_kernel_column_count_gate(ncols):
    columns = [np.arange(N, dtype=np.int64)] * ncols

    assert algorithms.duplicated_rows_swisstable(columns) is None


def test_row_kernel_min_rows_gate():
    columns = [np.arange(16, dtype=np.int64)] * 2

    assert algorithms.duplicated_rows_swisstable(columns) is None


def test_row_kernel_length_mismatch_gate():
    columns = [np.arange(N, dtype=np.int64), np.arange(N + 1, dtype=np.int64)]

    assert algorithms.duplicated_rows_swisstable(columns) is None


def test_row_kernel_table_size_gate(monkeypatch):
    monkeypatch.setattr(algorithms, "_ROW_DEDUP_MAX_TABLE_BYTES", 1)

    column = np.arange(N, dtype=np.int64)

    assert algorithms.duplicated_rows_swisstable([column, column]) is None


@pytest.mark.parametrize(
    "n, ncols, expected",
    [
        (0, 2, 16 * (1 + 8 * 2 + 8)),
        (1 << 20, 3, (1 << 21) * (1 + 8 * 3 + 8)),
    ],
)
def test_row_table_nbytes(n, ncols, expected):
    assert algorithms._row_table_nbytes(n, ncols) == expected


@pytest.mark.parametrize(
    "values, is_float",
    [
        (np.array([True, False]), 0),
        (np.array([1, 2], dtype="int8"), 0),
        (np.array([1, 2], dtype="uint64"), 0),
        (np.array([1, 2], dtype="int64").view("M8[s]"), 0),
        (np.array([1.0, 2.0], dtype="float16"), 1),
        (np.array([1.0, 2.0], dtype="float32"), 1),
        (np.array([1.0, 2.0], dtype="float64"), 1),
        (pd.array(date_range("2020-01-01", periods=2)), 0),
        (pd.array(pd.to_timedelta([1, 2], unit="s")), 0),
    ],
    ids=[
        "bool",
        "int8",
        "uint64",
        "datetime64",
        "float16",
        "float32",
        "float64",
        "datetimearray",
        "timedeltaarray",
    ],
)
def test_row_key_array_accepts(values, is_float):
    converted = algorithms._row_key_array(values)

    assert converted is not None
    array, flag = converted
    assert array.dtype == np.dtype("int64")
    assert flag == is_float


@pytest.mark.parametrize(
    "values",
    [
        np.zeros((2, 2)),
        [1, 2],
        pd.array(["a", "b"], dtype="string"),
        pd.array([1, 2], dtype="Int64"),
        pd.Categorical(["a", "b"]),
        pd.array([1 + 1j, 2j]),
        np.array([1, 2], dtype="complex64"),
    ],
    ids=["2d", "list", "string", "masked", "categorical", "complex128", "complex64"],
)
def test_row_key_array_rejects(values):
    assert algorithms._row_key_array(values) is None


@pytest.mark.skipif(
    np.dtype(np.longdouble).itemsize == 8, reason="longdouble is a float64 alias"
)
def test_row_key_array_rejects_longdouble():
    assert algorithms._row_key_array(np.array([1, 2], dtype=np.longdouble)) is None


@pytest.mark.skipif(sys.byteorder == "big", reason="needs a little endian host")
def test_row_key_array_rejects_non_native_byteorder():
    assert algorithms._row_key_array(np.array([1, 2], dtype=">i8")) is None


def test_kernel_canonicalizes_float_bits():
    bits = np.array([0.0, -0.0, np.nan, np.nan, 0.0], dtype="float64").view(
        np.int64
    )
    zeros = np.zeros(5, dtype=np.int64)
    is_float = np.array([1, 0], dtype=np.uint8)

    result = swisstable.duplicated_rows([bits, zeros], is_float, keep="first")

    assert result.tolist() == [False, True, False, True, True]


def test_kernel_float_flag_controls_canonicalization():
    bits = np.array([np.nan, np.nan], dtype="float64").view(np.int64)
    bits[1] ^= 1  # a different NaN payload
    zeros = np.zeros(2, dtype=np.int64)

    as_float = swisstable.duplicated_rows(
        [bits, zeros], np.array([1, 0], dtype=np.uint8), keep="first"
    )
    as_int = swisstable.duplicated_rows(
        [bits, zeros], np.zeros(2, dtype=np.uint8), keep="first"
    )

    assert as_float.tolist() == [False, True]
    assert as_int.tolist() == [False, False]


def test_kernel_requires_two_to_eight_columns():
    column = np.zeros(4, dtype=np.int64)

    with pytest.raises(ValueError, match="2 to 8 columns"):
        swisstable.duplicated_rows([column], np.zeros(1, dtype=np.uint8))
    with pytest.raises(ValueError, match="2 to 8 columns"):
        swisstable.duplicated_rows([column] * 9, np.zeros(9, dtype=np.uint8))


def test_kernel_requires_one_flag_per_column():
    column = np.zeros(4, dtype=np.int64)

    with pytest.raises(ValueError, match="one flag per column"):
        swisstable.duplicated_rows([column] * 2, np.zeros(3, dtype=np.uint8))


def test_kernel_requires_equal_lengths():
    columns = [np.zeros(4, dtype=np.int64), np.zeros(5, dtype=np.int64)]

    with pytest.raises(ValueError, match="same length"):
        swisstable.duplicated_rows(columns, np.zeros(2, dtype=np.uint8))


def test_kernel_rejects_unknown_keep():
    column = np.zeros(4, dtype=np.int64)

    with pytest.raises(ValueError, match="keep must be"):
        swisstable.duplicated_rows(
            [column] * 2, np.zeros(2, dtype=np.uint8), keep="middle"
        )


def test_kernel_empty_input():
    columns = [np.zeros(0, dtype=np.int64)] * 2

    result = swisstable.duplicated_rows(columns, np.zeros(2, dtype=np.uint8))

    assert result.dtype == np.dtype("bool")
    assert len(result) == 0
