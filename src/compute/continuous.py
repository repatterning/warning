"""Module cartography/continuous.py"""
import datetime
import typing


class Continuous:
    """
    Calculates the latest schedule times of the standard hydrography state machine.
    """

    def __init__(self, arguments: dict):
        """

        :param arguments: A set of arguments vis-à-vis computation & data operations objectives.
        """

        self.__terminate: dict = arguments.get('scheduler_continuous').get('terminate')

    def exc(self, ending: datetime.datetime) -> typing.Tuple[datetime.datetime, datetime.datetime]:
        """

        :param ending: The time the warning period ends
        :return:
        """

        # Start
        __next = ending.date() + datetime.timedelta(days=1)
        __starting = datetime.datetime(year=__next.year, month=__next.month, day=__next.day, hour=2, minute=5, second=0)

        # End
        __ending = datetime.datetime(
            year=self.__terminate.get('year'),
            month=self.__terminate.get('month'),
            day=self.__terminate.get('day'))

        return __starting, __ending
