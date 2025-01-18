import src.attributes.correlation
import src.attributes.listings


class Interface:

    def __init__(self):
        pass

    def exc(self):

        listings = src.attributes.listings.Listings().exc()
        src.attributes.correlation.Correlation().exc(listings=listings)
