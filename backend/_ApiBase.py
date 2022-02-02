from functools import wraps
from backend.utilities import logger


class ApiBase:
    # ===== Private methods ===== #
    # Decorators
    @staticmethod
    def _try_except_na(function):
        """
        Wraps the method in a try-except, to return n/a
        if the method being decorated is raises an Attribute error when the request returns None
        :param function:
        :return function():
        """

        @wraps(function)
        def inner(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except AttributeError:
                logger.info(f"{function.__name__} function returns n/a")
                return "n/a"

        return inner

    # Repeatedly used methods
    @staticmethod
    def _format_to_return(status: int, payload):
        """
        This formats the data json properly to be directly sent to the main app
        :param status:
        :param payload:
        :return formatted json:
        """
        return {
            "status": status,
            "payload": payload
        }
