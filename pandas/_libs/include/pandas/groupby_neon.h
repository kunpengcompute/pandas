#pragma once

#include <Python.h>
#include <numpy/ndarraytypes.h>
#include <stdint.h>

/* Aggregate values[i, :] into row `labels[i]` of prodx. Labels must satisfy
 * -1 <= labels[i] < ngroups; a non-negative label outside that range makes
 * the kernel return -1 without writing, so the caller can raise. */
int pandas_group_prod_float64_neon(double *prodx, const double *values,
                                   const npy_intp *labels, int64_t *counts,
                                   Py_ssize_t nrows, Py_ssize_t ncols,
                                   Py_ssize_t ngroups);

int pandas_group_prod_float32_neon(float *prodx, const float *values,
                                   const npy_intp *labels, int64_t *counts,
                                   Py_ssize_t nrows, Py_ssize_t ncols,
                                   Py_ssize_t ngroups);

int pandas_group_prod_float64_neon_colmajor(double *prodx,
                                            const double *values,
                                            const npy_intp *labels,
                                            int64_t *counts, Py_ssize_t nrows,
                                            Py_ssize_t ncols,
                                            Py_ssize_t ngroups);

int pandas_group_prod_float32_neon_colmajor(float *prodx,
                                            const float *values,
                                            const npy_intp *labels,
                                            int64_t *counts, Py_ssize_t nrows,
                                            Py_ssize_t ncols,
                                            Py_ssize_t ngroups);
