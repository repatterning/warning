import typing

import numpy as np


class Partitions(typing.NamedTuple):

    ts_id: int
    period: np.datetime64
    catchment_size: float
    gauge_datum: float
    on_river: bool
