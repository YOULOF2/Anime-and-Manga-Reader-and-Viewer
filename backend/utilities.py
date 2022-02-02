from bs4 import BeautifulSoup
import requests
from loguru import logger

__all__ = ["soupify", "get_request", "logger"]


def soupify(html_site):
    return BeautifulSoup(html_site, "html.parser")


def get_request(endpoint, **kwargs):
    """
    Does a GET request to the inputted endpoint along with the params.
    To return the html text and the request status code
    :param endpoint:
    :return:
    """
    params = kwargs.get("params", None)
    request = requests.get(endpoint, params)
    status_code = request.status_code
    logger.info(f"request sent to {endpoint}, with status code {status_code}")
    request.raise_for_status()
    return request.text, status_code
