
import statsmodels.graphics.tsaplots as sgt

import src.elements.text_attributes as txa
import src.functions.streams


class Correlation:

    def __init__(self):

        self.__streams = src.functions.streams.Streams()

    def exc(self, listings: list):

        for listing in listings[:2]:

            text = txa.TextAttributes(uri=listing, header=0)
            data = self.__streams.read(text=text)

            sgt.plot_pacf(x=data['value'].values)
