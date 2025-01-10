"""Module partitions.py"""
import typing

import numpy as np


class Partitions(typing.NamedTuple):
    """
    The data type class ⇾ Partitions

    Attributes
    ----------
    ts_id: int

    period: str

    catchment_size: float

    gauge_datum: float
        The elevation above ...
    on_river: bool
        
    """

    ts_id: int
    period: str
    catchment_size: float
    gauge_datum: float
    on_river: bool
