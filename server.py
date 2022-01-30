import sys
from backend.AnimeMangaSearch import AMSApi
from backend.MangaCollectorApi import MangaCollectorApi
from loguru import logger

annApi = AMSApi()
# print(annApi.search_manga_by_name("Black Clover"))
print(annApi.get_media_details_by_id(17059))
# print(MangaCollectorApi().search_for_manga_by_name("Black Clover"))

