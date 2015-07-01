# -*- coding: utf-8 -*-
from engarde.core import CheckSet

none_missing = CheckSet().none_missing
is_shape = CheckSet().is_shape
unique_index = CheckSet().unique_index
is_monotonic = CheckSet().is_monotonic
within_set = CheckSet().within_set
within_range = CheckSet().within_range
within_n_std = CheckSet().within_n_std
has_dtypes = CheckSet().has_dtypes

__all__ = [none_missing, is_shape, none_missing, unique_index, within_n_std,
           within_range, within_set, has_dtypes]
