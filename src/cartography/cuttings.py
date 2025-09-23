"""Module cuttings.py"""
import geopandas
import shapely


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

    def members(self, _polygon: shapely.geometry.polygon.Polygon) -> geopandas.GeoDataFrame:
        """

        :param _polygon: The polygon of a weather warning area
        :return:
        """

        outputs = self.__is_member(_polygon=_polygon)

        return self.__reference.loc[outputs, :]

    def states(self, _polygon: shapely.geometry.polygon.Polygon) -> int:
        """

        :param _polygon: The polygon of a weather warning area
        :return:
        """

        # Is y a member of polygon `_polygon`? `y` is a geometry point of self.__instances
        outputs = self.__is_member(_polygon=_polygon)

        return sum(outputs)
