from backend.ApiBase import ApiBase
from bs4 import BeautifulSoup


class MangaCollectorApi(ApiBase):
    def __init__(self):
        super().__init__()
        self._base_endpoint = "https://readmanganato.com/"


