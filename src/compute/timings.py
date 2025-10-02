import logging
import datetime

class Timings:

    def __init__(self, arguments: dict, starting: datetime.datetime, ending: datetime.datetime):

        self.__arguments = arguments
        self.__starting = starting
        self.__ending = ending

    def __events_forecasting(self, focus: str):
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

    def __events_fundamental(self, focus: str):
        """

        :param focus:
        :return:
        """

        __scheduler = self.__arguments.get(focus)
        __scheduler['starting'] = self.__starting
        __scheduler['ending'] = self.__ending

        return __scheduler

    def exc(self, focus: str):

        match focus:
            case 'scheduler_events_forecasting':
                return self.__events_forecasting(focus=focus)
            case 'scheduler_events_fundamental':
                logging.info(focus)
            case 'scheduler_continuous':
                logging.info(focus)
            case _:
                raise ValueError('{focus} is not an option.')
