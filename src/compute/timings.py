"""Module compute/timings.py"""
import datetime


class Timings:
    """
    Calculates event bridge times
    """

    def __init__(self, arguments: dict, starting: datetime.datetime, ending: datetime.datetime):
        """

        :param arguments: A set of arguments vis-à-vis computation & data operations objectives.
        :param starting:
        :param ending:
        """

        self.__arguments = arguments
        self.__starting = starting
        self.__ending = ending

    def __events_forecasting(self, scheduler: str) -> dict:
        """
        Builds cron expressions, e.g., "cron(45 09,21 * * ? *)"

        :param scheduler:
        :return:
        """

        __scheduler = self.__arguments.get(scheduler)

        # The cron expression template
        expression = "cron({minute} {initial},{later} * * ? *)"

        # Arithmetic
        start = self.__starting + datetime.timedelta(minutes=25)
        additional = start + datetime.timedelta(hours=12)

        # Hence
        __scheduler['schedule_expression'] = expression.format(
            minute=start.minute, initial=start.hour, later=additional.hour)
        __scheduler['starting'] = self.__starting
        __scheduler['ending'] = self.__ending

        return __scheduler

    def __events_fundamental(self, scheduler: str) -> dict:
        """

        :param scheduler:
        :return:
        """

        __scheduler = self.__arguments.get(scheduler)

        # Hence
        __scheduler['starting'] = self.__starting
        __scheduler['ending'] = self.__ending

        return __scheduler

    def __continuous(self, scheduler: str) -> dict:
        """

        :param scheduler:
        :return:
        """

        __scheduler = self.__arguments.get(scheduler)

        # Arithmetic
        __next = self.__ending.date() + datetime.timedelta(days=1)
        __starting = datetime.datetime(
            year=__next.year, month=__next.month, day=__next.day, hour=2, minute=5, second=0)
        __ending = datetime.datetime(
            year=__scheduler.get('terminate').get('year'), month=__scheduler.get('terminate').get('month'),
            day=__scheduler.get('terminate').get('day'))

        # Hence
        __scheduler['starting'] = __starting
        __scheduler['ending'] = __ending

        return __scheduler

    def __warning(self, scheduler: str):
        """

        :param scheduler:
        :return:
        """

        __scheduler = self.__arguments.get(scheduler)

        # Arithmetic
        __starting = self.__starting - datetime.timedelta(minutes=5)

        # Hence
        __scheduler['starting'] = __starting
        __scheduler['ending'] = self.__ending

        return __scheduler

    def exc(self, scheduler: str) -> dict:
        """

        :param scheduler:
        :return:
        """

        match scheduler:
            case 'scheduler_events_forecasting':
                return self.__events_forecasting(scheduler=scheduler)
            case 'scheduler_events_fundamental':
                return self.__events_fundamental(scheduler=scheduler)
            case 'scheduler_continuous':
                return self.__continuous(scheduler=scheduler)
            case 'scheduler_warning':
                return self.__warning(scheduler=scheduler)
            case _:
                raise ValueError(f'{scheduler} is not an option.')
