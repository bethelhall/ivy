# global
import numpy as np
from typing import Tuple
from collections import namedtuple
from packaging import version

import ivy

def unique_inverse(x: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray]:
    out = namedtuple('unique_inverse', ['values', 'inverse_indices'])
    values, inverse_indices = np.unique(x, return_inverse=True)
    nan_count = np.count_nonzero(np.isnan(x))
    if nan_count > 1:
        values = np.append(values, np.full(nan_count - 1, np.nan)).astype(x.dtype)
    inverse_indices = inverse_indices.reshape(x.shape)
    return out(values, inverse_indices)


def unique_values(x: np.ndarray, out: np.ndarray = None) \
        -> np.ndarray:
    nan_count = np.count_nonzero(np.isnan(x))
    if (version.parse(np.__version__) >= version.parse('1.21.0') and nan_count > 1):
        unique = np.append(np.unique(x.flatten()), np.full(nan_count - 1, np.nan)).astype(x.dtype)
    else:
        unique = np.unique(x.flatten()).astype(x.dtype)
    if ivy.exists(out):
        return ivy.inplace_update(out, unique)
    return unique


def unique_counts(x: np.ndarray) \
        -> Tuple[np.ndarray, np.ndarray]:
    v, c = np.unique(x, return_counts=True)
    nan_count = np.count_nonzero(np.isnan(x))
    if nan_count > 1:
        nan_idx = np.where(np.isnan(v))
        c[nan_idx] = 1
        v = np.append(v, np.full(nan_count - 1, np.nan)).astype(x.dtype)
        c = np.append(c, np.full(nan_count - 1, 1)).astype('int32')
    uc = namedtuple('uc', ['values', 'counts'])
    return uc(v, c)
