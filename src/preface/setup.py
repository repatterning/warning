"""Module setup.py"""
import sys

import config
import src.functions.cache
import src.functions.directories


class Setup:
    """
    Description
    -----------

    Sets up local environments
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__directories = src.functions.directories.Directories()

    def __data(self) -> bool:
        """

        :return:
        """

        self.__directories.cleanup(path=self.__configurations.data_)

        return self.__directories.create(path=self.__configurations.data_)

    def __local(self) -> bool:
        """

        :return:
        """

        self.__directories.cleanup(path=self.__configurations.warehouse)

        states = []
        for path in [self.__configurations.points_, self.__configurations.menu_]:
            states.append(self.__directories.create(path=path))

        return all(states)

    def exc(self) -> bool:
        """

        :return:
        """

        if self.__local() & self.__data():
            return True

        src.functions.cache.Cache().exc()

        sys.exit('Error: Set up failure')
