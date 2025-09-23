"""Module cuttings.py"""
import logging
import geopandas
import shapely
import datetime


class Cuttings:
    """
    Intersections of polygons
    """

    def __init__(self, reference: geopandas.GeoDataFrame):
        """

        :param reference: The reference sheet of gauges.  Each instance encodes the attributes of a gauge.
        """

        self.__reference = reference

    def __is_member(self, _polygon: shapely.geometry.polygon.Polygon):
        """
        Determines whether a reference gauge location lies within a polygon; per reference gauge

        :param _polygon: The polygon of a weather warning area
        :return:
        """

        return self.__reference.geometry.apply(lambda y: y.within(_polygon))

    def members(self, _elements: tuple) -> geopandas.GeoDataFrame:
        """
        .geometry: shapely.geometry.polygon.Polygon -> The polygon of a weather warning area

        :param _elements:
        :return:
        """

        logging.info(_elements)
        logging.info(type(_elements))

        outputs = self.__is_member(_polygon=_elements.geometry)

        return self.__reference.loc[outputs, :]
