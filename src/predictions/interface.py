
import dask

import src.elements.specifications as se
import src.elements.parts as pr
import src.predictions.data
import src.predictions.estimates



class Interface:

    def __init__(self):
        pass


    def exc(self, specifications_: list[se.Specifications]):

        __get_data = dask.delayed(src.predictions.data.Data().exc)
        __get_errors = dask.delayed(src.predictions.estimates.Estimates().exc)


        computations = []
        for specifications in specifications_:

            parts: pr.Parts = __get_data(specifications=specifications)
            errors: pr.Parts = __get_errors(parts=parts)
