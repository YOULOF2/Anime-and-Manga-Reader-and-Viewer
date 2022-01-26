import requests
from bs4 import BeautifulSoup
from datetime import datetime


class ANNApi:
    def __init__(self):
        self._search_endpoint = "https://www.animenewsnetwork.com/encyclopedia/search/name"
        self._details_endpoint = "https://www.animenewsnetwork.com/encyclopedia"
        self._base_endpoint = "https://www.animenewsnetwork.com"

    @staticmethod
    def _try_except_na(function):
        def inner():
            try:
                return function()
            except AttributeError:
                return "n/a"

        return inner

    @staticmethod
    def _format_to_return(status: int, payload):
        return {
            "status": status,
            "payload": payload
        }

    @staticmethod
    def _get_request(endpoint, params):
        request = requests.get(endpoint, params)
        return request.text, request.status_code

    def search_anime_by_name(self, name):
        params = {
            "only": "anime",
            "q": name
        }
        html_site, status_code = self._get_request(self._search_endpoint, params)
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
        html_site, request_status = self._get_request(self._search_endpoint, params)
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

    def get_anime_details_by_id(self, ann_id):

        @self._try_except_na
        def get_main_title():
            #       --- main title ---
            title_div = soup.find(id="page_header")
            title_text = title_div.text.strip()
            return title_text

        @self._try_except_na
        def get_alt_titles():
            #       --- alternative titles ---
            alt_titles_parent_div = soup.find(id="infotype-2")
            alt_titles_child_divs = alt_titles_parent_div.find_all("div")
            all_alt_titles_list = []
            for div in alt_titles_child_divs:
                all_alt_titles_list.append(div.text)

            return all_alt_titles_list

        @self._try_except_na
        def get_related_anime():
            #         --- related anime ---
            related_parent_div = soup.find(id="infotype-related")
            related_child_divs = related_parent_div.find_all("a")
            all_related_anime_list = []
            for anchor in related_child_divs:
                all_related_anime_list.append(
                    {
                        "title": anchor.text,
                        "ann-id": str(anchor.get("href")).split("?id=")[1]
                    }
                )
            return all_related_anime_list

        @self._try_except_na
        def get_anime_genre():
            #         --- anime genre ---
            genres_parent_div = soup.find(id="infotype-30")
            genres_child_divs = genres_parent_div.find_all("a")
            anime_genre_list = []
            for anchor in genres_child_divs:
                anime_genre_list.append(anchor.text)

            return anime_genre_list

        @self._try_except_na
        def get_anime_theme():
            #         --- anime themes ---
            themes_parent_div = soup.find(id="infotype-31")
            themes_child_divs = themes_parent_div.find_all("a")
            anime_theme_list = []
            for anchor in themes_child_divs:
                anime_theme_list.append(anchor.text)

            return anime_theme_list

        @self._try_except_na
        def get_plot_sum():
            #        --- anime plot summary ---
            plot_sum_parent_div = soup.find(id="infotype-12")
            plot_sum = plot_sum_parent_div.find("span").text

            return plot_sum

        @self._try_except_na
        def get_cover_url():
            #        --- cover image ---
            cover_image_parent_div = soup.find(class_="fright")
            proper_image = cover_image_parent_div.find('img').get('src').replace('fit200x200', 'max500x600')
            cover_image_url = f"https:{proper_image}"

            return cover_image_url

        @self._try_except_na
        def get_all_episodes():
            def format_date(table_row):
                date_released_list = table_row.find("td").find("div").text.split("-")
                date_released_list.reverse()
                return "-".join(date_released_list)

            params_ = {
                "id": ann_id,
                "page": 25
            }
            episodes_html_page, _ = self._get_request(endpoint, params_)
            soup_ = BeautifulSoup(episodes_html_page, "html.parser")
            episodes_table = soup_.find(class_="episode-list")
            all_trs = episodes_table.find_all("tr")
            episode_list = []
            for tr in all_trs:
                date_released = format_date(tr)
                episode_number = tr.find_all("td")[1].text.strip().replace(".", "")
                # TODO: GET EPISODE NAME
                # TODO: PLACE ALL DATA IN JSON THE APPEND TO 'episode_list'

        # ============================================================================================================ #
        # ============================================================================================================ #

        endpoint = f"{self._details_endpoint}/anime.php"
        params = {
            "id": ann_id,
        }

        html_site, request_status = self._get_request(endpoint, params)
        soup = BeautifulSoup(html_site, "html.parser")

        main_title = get_main_title()
        alt_titles = get_alt_titles()
        related_anime = get_related_anime()
        anime_genre = get_anime_genre()
        anime_theme = get_anime_theme()
        plot_summary = get_plot_sum()
        cover_url = get_cover_url()
        all_episodes = get_all_episodes()

        final_data = {
            "title": {
                "main": main_title,
                "alt": alt_titles,
            },
            "related": related_anime,
            "genre": anime_genre,
            "theme": anime_theme,
            "plot_sum": plot_summary,
            "cover_url": cover_url,
        }
        return self._format_to_return(request_status, final_data)

    # def get_manga_details_by_id(self, ann_id):
    #
    #     @self._try_except_na
    #     def get_main_title():
    #         #       --- main title ---
    #         title_div = soup.find(id="page_header")
    #         title_text = title_div.text.strip()
    #         return title_text
    #
    #     @self._try_except_na
    #     def get_alt_titles():
    #         #       --- alternative titles ---
    #         alt_titles_parent_div = soup.find(id="infotype-2")
    #         alt_titles_child_divs = alt_titles_parent_div.find_all("div")
    #         all_alt_titles_list = []
    #         for div in alt_titles_child_divs:
    #             all_alt_titles_list.append(div.text)
    #
    #         return all_alt_titles_list
    #
    #     @self._try_except_na
    #     def get_related_manga():
    #         #         --- related anime ---
    #         related_parent_div = soup.find(id="infotype-related")
    #         related_child_divs = related_parent_div.find_all("a")
    #         all_related_manga_list = []
    #         for anchor in related_child_divs:
    #             all_related_manga_list.append(
    #                 {
    #                     "title": anchor.text,
    #                     "ann-id": str(anchor.get("href")).split("?id=")[1]
    #                 }
    #             )
    #         return all_related_manga_list
    #
    #     @self._try_except_na
    #     def get_manga_genre():
    #         #         --- anime genre ---
    #         genres_parent_div = soup.find(id="infotype-30")
    #         genres_child_divs = genres_parent_div.find_all("a")
    #         manga_genre_list = []
    #         for anchor in genres_child_divs:
    #             manga_genre_list.append(anchor.text)
    #
    #         return manga_genre_list
    #
    #     @self._try_except_na
    #     def get_manga_theme():
    #         #         --- anime themes ---
    #         themes_parent_div = soup.find(id="infotype-31")
    #         themes_child_divs = themes_parent_div.find_all("a")
    #         manga_theme_list = []
    #         for anchor in themes_child_divs:
    #             manga_theme_list.append(anchor.text)
    #
    #         return manga_theme_list
    #
    #     @self._try_except_na
    #     def get_description():
    #         #        --- anime plot summary ---
    #         plot_sum_parent_div = soup.find(id="infotype-12")
    #         plot_sum = plot_sum_parent_div.find("span").text
    #
    #         return plot_sum
    #
    #     @self._try_except_na
    #     def get_cover_url():
    #         #        --- cover image ---
    #         cover_image_parent_div = soup.find(class_="fright")
    #         proper_image = cover_image_parent_div.find('img').get('src').replace('fit200x200', 'max500x600')
    #         cover_image_url = f"https:{proper_image}"
    #
    #         return cover_image_url
    #
    #     endpoint = f"{self._details_endpoint}/manga.php"
    #     params = {
    #         "id": ann_id,
    #     }
    #
    #     html_site, request_status = self._get_request(endpoint, params)
    #     soup = BeautifulSoup(html_site, "html.parser")
    #
    #     main_title = get_main_title()
    #     alt_titles = get_alt_titles()
    #     related_manga = get_related_manga()
    #     manga_genre = get_manga_genre()
    #     manga_theme = get_manga_theme()
    #     plot_summary = get_description()
    #     cover_url = get_cover_url()
    #
    #     final_data = {
    #         "title": {
    #             "main": main_title,
    #             "alt": alt_titles,
    #         },
    #         "related": related_manga,
    #         "genre": manga_genre,
    #         "theme": manga_theme,
    #         "plot_sum": plot_summary,
    #         "cover_url": cover_url,
    #     }
    #     return self._format_to_return(request_status, final_data)
