"""Module cuttings.py"""
import logging

import geopandas
import shapely

import src.elements.system as stm


class Cuttings:
    """
    Intersections of polygons
    """

    def __init__(self, reference: geopandas.GeoDataFrame):
        """

        :param reference: The reference sheet of gauges.  Each instance encodes the attributes of a gauge.
        """

        self.__reference = reference
        self.__r_fields = ['ts_id', 'station_id', 'catchment_id', 'geometry']

    def __is_member(self, _polygon: shapely.geometry.polygon.Polygon):
        """
        Determines whether a reference gauge location lies within a polygon; per reference gauge

        :param _polygon: The polygon of a weather warning area
        :return:
        """

        return self.__reference.geometry.apply(lambda y: y.within(_polygon))

    def members(self, _elements: stm.System) -> geopandas.GeoDataFrame:
        """
        .geometry: shapely.geometry.polygon.Polygon -> The polygon of a weather warning area

        :param _elements:
        :return:
        """

        logging.info(_elements)

        states = self.__is_member(_polygon=_elements.geometry)

        frame = self.__reference.copy().loc[states, self.__r_fields]
        frame['issued_date'] = _elements.issuedDate
        frame['warning_level'] = _elements.warningLevel
        frame['warning_id'] = _elements.warningId
        frame['modified'] = _elements.modifiedDate
        frame['starting'] = _elements.validFromDate
        frame['ending'] = _elements.validToDate

        return frame
