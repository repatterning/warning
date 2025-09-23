"""Module system.py"""
import datetime
import typing

import numpy as np
import shapely


class System(typing.NamedTuple):
    """
    The data type class ⇾ System

    Attributes
    ----------

    """

    Index: int
    issuedDate: datetime.datetime
    warningLikelihood: np.int32
    warningLevel: str
    warningStatus: str
    warningHeadline: str
    warningId: str
    warningVersion: str
    warningFurtherDetails: str
    modifiedDate: datetime.datetime
    validFromDate: datetime.datetime
    affectedAreas: str
    warningImpact: np.int32
    validToDate: datetime.datetime
    geometry: shapely.geometry.polygon.Polygon
