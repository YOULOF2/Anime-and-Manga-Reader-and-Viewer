from functools import wraps
from loguru import logger
import requests
from bs4 import BeautifulSoup


class ApiBase:
    # ===== Private methods ===== #
    # Decorators
    @staticmethod
    def _logger(function):
        """
        This is a wrapper function to log the use of the method being decorated
        :param function:
        :return function():
        """
        @wraps(function)
        def inner(*args, **kwargs):
            logger.info(f"{function.__name__} has been called")
            return function(*args, **kwargs)

        return inner

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

    @staticmethod
    def _get_request(endpoint, **kwargs):
        """
        Does a GET request to the inputted endpoint along with the params.
        To return the html text and the request status code
        :param endpoint:
        :param params:
        :return:
        """
        params = kwargs.get("params", None)
        request = requests.get(endpoint, params)
        status_code = request.status_code
        logger.info(f"request sent to {endpoint}, with status code {status_code}")
        request.raise_for_status()
        return request.text, status_code
