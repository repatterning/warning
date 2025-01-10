import typing

import numpy as np


class Partitions(typing.NamedTuple):
    """
    The data type class ⇾ Partitions
    """

    ts_id: int
    period: np.datetime64
    catchment_size: float
    gauge_datum: float
    on_river: bool
