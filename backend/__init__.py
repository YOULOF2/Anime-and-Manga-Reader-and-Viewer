from backend._AnimeMangaSearch import _AnimeMangaSearch
from backend._MangaCollector import _MangaCollector
from backend._getAnimeVideo import _get_anime_video

_AMS = _AnimeMangaSearch()
_MC = _MangaCollector()

__all__ = ["search_manga_by_name",
           "search_anime_by_name",
           "get_media_details",
           "get_manga",
           "get_anime_video_link"]


def search_manga_by_name(name):
    return _AMS.search_manga_by_name(name)


def search_anime_by_name(name):
    return _AMS.search_anime_by_name(name)


def get_media_details(ams_id):
    return _AMS.get_media_details_by_id(ams_id)


def get_manga(manga_name, chapter_number):
    return _MC.get_manga_pdf_by_id_and_chapter(manga_name, chapter_number)


def get_anime_video_link(anime_title, episode_number):
    return _get_anime_video(anime_title, episode_number)
