"""Module partitions.py"""
import typing


class Partitions(typing.NamedTuple):
    """
    The data type class ⇾ Partitions<br><br>

    Attributes<br>
    ----------<br>
    <b>ts_id</b>: int<br>
        The identification code of a time series.<br>
    <b>datestr</b>: str<br>
        The <b>date string of the start date of a period</b>, format %Y-%m-%d,  i.e., YYYY-mm-dd.<br>
    <b>catchment_size</b>: float<br>
        The size of the catchment the time-series-measuring-station belongs to.<br>
    <b>gauge_datum</b>: float<br>
        The elevation above ...<br>
    <b>on_river</b>: bool<br>
        An on river measuring station?
    """

    ts_id: int
    datestr: str
    catchment_size: float
    gauge_datum: float
    on_river: bool
