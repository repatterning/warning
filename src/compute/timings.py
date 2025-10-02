import datetime

import src.compute.continuous


class Timings:

    def __init__(self, arguments: dict, starting: datetime.datetime, ending: datetime.datetime):
        """

        :param arguments:
        :param starting:
        :param ending:
        """

        self.__arguments = arguments
        self.__starting = starting
        self.__ending = ending

    def __events_forecasting(self, focus: str) -> dict:
        """
        Builds cron expressions, e.g., "cron(45 09,21 * * ? *)"

        :param focus:
        :return:
        """

        # The cron expression template
        expression = "cron({minute} {initial},{later} * * ? *)"

        # The start & in-between times
        start = self.__starting + datetime.timedelta(minutes=25)
        inbetween = start + datetime.timedelta(hours=12)

        # Scheduler
        __scheduler = self.__arguments.get(focus)
        __scheduler['schedule_expression'] = expression.format(
            minute=start.minute, initial=start.hour, later=inbetween.hour)
        __scheduler['starting'] = self.__starting
        __scheduler['ending'] = self.__ending

        return __scheduler

    def __events_fundamental(self, focus: str) -> dict:
        """

        :param focus:
        :return:
        """

        __scheduler = self.__arguments.get(focus)
        __scheduler['starting'] = self.__starting
        __scheduler['ending'] = self.__ending

        return __scheduler

    def __continuous(self, focus: str) -> dict:
        """

        :param focus:
        :return:
        """

        __starting, __ending = src.compute.continuous.Continuous(
            arguments=self.__arguments).exc(ending=self.__ending)

        __scheduler = self.__arguments.get(focus)
        __scheduler['starting'] = __starting
        __scheduler['ending'] = __starting

        return __scheduler

    def exc(self, focus: str) -> dict:
        """

        :param focus:
        :return:
        """

        match focus:
            case 'scheduler_events_forecasting':
                return self.__events_forecasting(focus=focus)
            case 'scheduler_events_fundamental':
                return self.__events_fundamental(focus=focus)
            case 'scheduler_continuous':
                return self.__continuous(focus=focus)
            case _:
                raise ValueError(f'{focus} is not an option.')
