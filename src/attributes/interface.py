"""Module interface.py"""
import src.attributes.correlation
import src.attributes.listings


class Interface:
    """
    For steps investigating series features.
    """

    def __init__(self):
        pass

    @staticmethod
    def exc():
        """

        :return:
        """

        listings = src.attributes.listings.Listings().exc()
        src.attributes.correlation.Correlation().exc(listings=listings)
