"""Module interface.py"""
import logging
import src.data.codes

class Interface:
    """
    Interface
    """

    def __init__(self):

        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self):

        codes: list[str] = src.data.codes.Codes().exc()
        self.__logger.info(codes)
