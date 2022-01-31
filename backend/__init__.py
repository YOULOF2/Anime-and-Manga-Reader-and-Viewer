from backend._AnimeMangaSearch import _AnimeMangaSearch
from backend._MangaCollector import _MangaCollector

_AMS = _AnimeMangaSearch()
_MC = _MangaCollector()


def search_manga_by_name(name):
    return _AMS.search_manga_by_name(name)


def search_anime_by_name(name):
    return _AMS.search_anime_by_name(name)


def get_anime_or_manga_by_ams_id(ams_id):
    return _AMS.get_media_details_by_id(ams_id)


def collect_manga(manga_name, chapter_number):
    return _MC.get_manga_pdf_by_id_and_chapter(manga_name, chapter_number)
