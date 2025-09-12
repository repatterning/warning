"""Module cuttings.py"""
import geopandas
import shapely


class Cuttings:
    """
    Intersections of polygons
    """

    def __init__(self, reference: geopandas.GeoDataFrame):
        """

        instances: the geometry field of `instances` encodes the points from a single/distinct parent catchment
        """

        self.__reference = reference

    def __is_member(self, _polygon: shapely.geometry.polygon.Polygon):
        """

        :param _polygon:
        :return:
        """

        return self.__reference.geometry.apply(lambda y: y.within(_polygon))

    def members(self, _polygon: shapely.geometry.polygon.Polygon) -> geopandas.GeoDataFrame:
        """

        :param _polygon:
        :return:
        """

        outputs = self.__is_member(_polygon=_polygon)

        return self.__reference.loc[outputs, :]

    def inside(self, _polygon: shapely.geometry.polygon.Polygon) -> int:
        """

        :param _polygon:
        :return:
        """

        # Is y a member of polygon `_polygon`? `y` is a geometry point of self.__instances
        outputs = self.__is_member(_polygon=_polygon)

        return sum(outputs)
