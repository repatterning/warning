
import typing

import pandas as pd


class Parts(typing.NamedTuple):
    """
    The data type class ⇾ Parts

    Attributes
    ----------

    """

    training: pd.DataFrame
    testing: pd.DataFrame
    futures: pd.DataFrame
