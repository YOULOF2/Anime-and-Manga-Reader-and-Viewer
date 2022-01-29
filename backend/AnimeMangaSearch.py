from bs4 import BeautifulSoup
from backend.ApiBase import ApiBase
from loguru import logger
import requests


class AMSApi(ApiBase):
    def __init__(self):
        super().__init__()
        self._ann_search_endpoint = "https://www.animenewsnetwork.com/encyclopedia/search/name"
        self._ann_details_endpoint = "https://www.animenewsnetwork.com/encyclopedia"
        self._ann_base_endpoint = "https://www.animenewsnetwork.com"
        self._readmanganato_base_endpoint = "https://readmanganato.com/"
        self._type = None

    # ===== Private methods ==== #
    def _is_anime(self):
        if self._type == "anime":
            return True
        return False

    def _return_manga_id(self, manga_name: str):
        raw_name = manga_name.replace(" (manga)", "")
        formatted_manga_name = raw_name.replace(" ", "_")
        endpoint = f"{self._readmanganato_base_endpoint}search/story/{formatted_manga_name}"
        html_site, status_code = self._get_request(endpoint)
        soup = BeautifulSoup(html_site, "html.parser")
        manga_details_div = soup.find_all("div", class_="search-story-item")
        for manga_search_item in manga_details_div:
            item_manga_name = manga_search_item.find("a", class_="item-title").text
            if raw_name.title() == item_manga_name.title():
                item_manga_id = manga_search_item.find("a", class_="item-title").get("href").split("-")[1]
                return item_manga_id

    # ===== Public methods ===== #
    def search_anime_by_name(self, name):
        params = {
            "only": "anime",
            "q": name
        }
        html_site, status_code = self._get_request(self._ann_search_endpoint, params=params)
        soup = BeautifulSoup(html_site, "html.parser")
        content_zone = soup.find(id="content-zone")
        all_anchors = content_zone.find_all("a")

        clean_data_list = []
        for anchor in all_anchors[3:]:
            anime_id = str(anchor.get("href")).split("?id=")[1]
            anime_name = anchor.text
            clean_data_list.append(
                {
                    "type": "anime",
                    "title": anime_name,
                    "ann-id": anime_id,
                }
            )

        return self._format_to_return(status_code, clean_data_list)

    def search_manga_by_name(self, name):
        params = {
            "only": "manga",
            "q": name
        }
        html_site, request_status = self._get_request(self._ann_search_endpoint, params=params)
        soup = BeautifulSoup(html_site, "html.parser")
        content_zone = soup.find(id="content-zone")
        all_anchors = content_zone.find_all("a")

        clean_data_list = []
        for anchor in all_anchors[3:]:
            manga_id = str(anchor.get("href")).split("?id=")[1]
            manga_name = anchor.text
            clean_data_list.append(
                {
                    "type": "manga",
                    "title": manga_name,
                    "ann-id": manga_id,
                }
            )

        return self._format_to_return(request_status, clean_data_list)

    def get_media_details_by_id(self, ann_id):
        # ========================== Functions ========================== #
        @self._try_except_na
        @self._logger
        def get_main_title():
            #       --- main title ---
            title_div = soup.find(id="page_header")
            title_text = title_div.text.strip()
            return title_text

        @self._try_except_na
        @self._logger
        def get_alt_titles():
            #       --- alternative titles ---
            alt_titles_parent_div = soup.find(id="infotype-2")
            alt_titles_child_divs = alt_titles_parent_div.find_all("div")
            all_alt_titles_list = []
            for div in alt_titles_child_divs:
                all_alt_titles_list.append(div.text)

            return all_alt_titles_list

        @self._try_except_na
        @self._logger
        def get_related_media():
            #         --- related media ---
            related_parent_div = soup.find(id="infotype-related")
            related_child_divs = related_parent_div.find_all("a")
            all_related_media_list = []
            for anchor in related_child_divs:
                all_related_media_list.append(
                    {
                        "title": anchor.text,
                        "ann-id": str(anchor.get("href")).split("?id=")[1]
                    }
                )
            return all_related_media_list

        @self._try_except_na
        @self._logger
        def get_media_genre():
            #         --- media genre ---
            genres_parent_div = soup.find(id="infotype-30")
            genres_child_divs = genres_parent_div.find_all("a")
            media_genre_list = []
            for anchor in genres_child_divs:
                media_genre_list.append(anchor.text)

            return media_genre_list

        @self._try_except_na
        @self._logger
        def get_media_theme():
            #         --- media themes ---
            themes_parent_div = soup.find(id="infotype-31")
            themes_child_divs = themes_parent_div.find_all("a")
            media_theme_list = []
            for anchor in themes_child_divs:
                media_theme_list.append(anchor.text)

            return media_theme_list

        @self._try_except_na
        @self._logger
        def get_plot_sum():
            #        --- media plot summary ---
            plot_sum_parent_div = soup.find(id="infotype-12")
            plot_sum = plot_sum_parent_div.find("span").text

            return plot_sum

        @self._try_except_na
        @self._logger
        def get_cover_url():
            #        --- cover image ---
            cover_image_parent_div = soup.find(class_="fright")
            if cover_image_parent_div is not None:
                proper_image = cover_image_parent_div.find('img').get('src').replace('fit200x200', 'max500x600')
            else:
                proper_image = soup.find(id="vid-art").get("src")

            cover_image_url = f"https:{proper_image}"
            return cover_image_url

        @self._try_except_na
        @logger.catch
        def get_all_releases():
            def format_date(table_row):
                try:
                    date_released_list = table_row.find("td").find("div").text.split("-")
                except AttributeError:
                    return "n/a"

                date_released_list.reverse()
                return "-".join(date_released_list)

            if self._is_anime():
                params_ = {
                    "id": ann_id,
                    "page": 25
                }
            else:
                params_ = {
                    "id": ann_id,
                    "page": 34
                }

            releases_html_page, _ = self._get_request(endpoint, params=params_)
            soup = BeautifulSoup(releases_html_page, "html.parser")
            releases_table = soup.find("table", class_="episode-list")
            all_trs = releases_table.find_all("tr")
            episode_list = []
            for tr in all_trs:
                date_released = format_date(tr)
                all_tds = tr.find_all("td")
                episode_number = all_tds[1].text.strip().replace(".", "")
                episode_name = all_tds[3].find("div").text

                alt_releases_name = []
                # Get all divs in the tr except the first one
                alt_episode_name_div_list = all_tds[3].find_all("div")[1:]
                if len(alt_episode_name_div_list) != 0:
                    for div in alt_episode_name_div_list:
                        for alt_div in div:
                            stripped_text = alt_div.text.strip()
                            if stripped_text != "":
                                alt_releases_name.append(stripped_text)

                data_json = {
                    "date_released": date_released,
                    "episode_number": episode_number,
                    "episode_name": {
                        "main": episode_name,
                        "alt": alt_releases_name
                    }
                }
                episode_list.append(data_json)
            return episode_list

        # =============================================================== #
        endpoint = f"{self._ann_details_endpoint}/anime.php"
        params = {
            "id": ann_id,
        }
        # Initially sends a get request to the site as an anime, if the name contains (manga),
        # the request is resent to get the correct information
        html_site, request_status = self._get_request(endpoint, params=params)
        soup = BeautifulSoup(html_site, "html.parser")

        main_title = get_main_title()

        self._type = "manga" if "(manga)" in main_title else "anime"
        logger.info(f"Media type is {self._type}")

        if not self._is_anime():
            endpoint = f"{self._ann_details_endpoint}/manga.php"
            params = {
                "id": ann_id,
            }

            html_site, request_status = self._get_request(endpoint, params=params)
            soup = BeautifulSoup(html_site, "html.parser")

            main_title = get_main_title()

        alt_titles = get_alt_titles()
        related_media = get_related_media()
        media_genre = get_media_genre()
        media_theme = get_media_theme()
        plot_summary = get_plot_sum()
        cover_url = get_cover_url()
        all_releases = get_all_releases()

        final_data = {
            "media_type": self._type,
            "cover_url": cover_url,
            "title": {
                "main": main_title,
                "alt": alt_titles,
            },
            "related": related_media,
            "genre": media_genre,
            "theme": media_theme,
            "plot_sum": plot_summary,
            "releases": all_releases
        }

        if not self._is_anime():
            final_data["manga_id"] = self._return_manga_id(main_title)

        return self._format_to_return(request_status, final_data)
