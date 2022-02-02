import re
from backend._ApiBase import ApiBase
from backend.utilities import *


class _AnimeMangaSearch(ApiBase):
    def __init__(self):
        super().__init__()
        self._ann_search_endpoint = "https://www.animenewsnetwork.com/encyclopedia/search/name"
        self._ann_details_endpoint = "https://www.animenewsnetwork.com/encyclopedia"
        self._ann_base_endpoint = "https://www.animenewsnetwork.com"
        self._type = None

    # ===== Private methods ==== #
    def _is_anime(self):
        if self._type == "anime":
            return True
        return False

    # ===== Public methods ===== #
    def search_anime_by_name(self, name):
        params = {
            "only": "anime",
            "q": name
        }
        html_site, status_code = get_request(self._ann_search_endpoint, params=params)
        soup = soupify(html_site)
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
        html_site, request_status = get_request(self._ann_search_endpoint, params=params)
        soup = soupify(html_site)
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
        @logger.catch
        def get_main_title():
            #       --- main title ---
            title_div = soup.find(id="page_header")
            title_text = title_div.text.strip()
            return title_text

        @self._try_except_na
        @logger.catch
        def get_alt_titles():
            #       --- alternative titles ---
            alt_titles_parent_div = soup.find(id="infotype-2")
            alt_titles_child_divs = alt_titles_parent_div.find_all("div")
            all_alt_titles_list = []
            for div in alt_titles_child_divs:
                all_alt_titles_list.append(div.text)

            return all_alt_titles_list

        @self._try_except_na
        @logger.catch
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
        @logger.catch
        def get_media_genre():
            #         --- media genre ---
            genres_parent_div = soup.find(id="infotype-30")
            genres_child_divs = genres_parent_div.find_all("a")
            media_genre_list = []
            for anchor in genres_child_divs:
                media_genre_list.append(anchor.text)

            return media_genre_list

        @self._try_except_na
        @logger.catch
        def get_media_theme():
            #         --- media themes ---
            themes_parent_div = soup.find(id="infotype-31")
            themes_child_divs = themes_parent_div.find_all("a")
            media_theme_list = []
            for anchor in themes_child_divs:
                media_theme_list.append(anchor.text)

            return media_theme_list

        @self._try_except_na
        @logger.catch
        def get_plot_sum():
            #        --- media plot summary ---
            plot_sum_parent_div = soup.find(id="infotype-12")
            plot_sum = plot_sum_parent_div.find("span").text

            return plot_sum

        @self._try_except_na
        @logger.catch
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

            releases_html_page, _ = get_request(endpoint, params=params_)
            soup = soupify(releases_html_page)
            releases_table = soup.find("table", class_="episode-list")
            try:
                all_trs = releases_table.find_all("tr")
            except AttributeError:
                main_html, _ = get_request(endpoint, params={"id": ann_id})
                soup = soupify(main_html)
                volumes_table = soup.find(id="infotype-20")
                if volumes_table is not None:
                    volume_divs = volumes_table.find_all("div")
                    all_releases = []
                    for release in volume_divs:
                        release_text = release.text
                        splited_text = release_text.split(". ")
                        data_json = {
                            "date_released": "n/a",
                            "release_number": splited_text[0].replace("#", ""),
                            "release_name": {
                                "main": splited_text[1],
                                "alt": "n/a"
                            }
                        }
                        all_releases.append(data_json)
                    return all_releases
                else:
                    params = {
                        "id": ann_id,
                        "page": 28,
                    }
                    date_released_html, _ = get_request(endpoint, params=params)
                    soup = soupify(date_released_html)
                    dates_table = soup.find(id="infotype-28")
                    all_releases = dates_table.find_all("div")
                    volume_lists = []
                    for volume in all_releases:
                        volume_lists.append(volume.text.split(" (")[1].replace(")", ""))

                    final_all_volumes = []
                    result = [e for e in re.split("[^0-9]", " ".join(volume_lists)) if e != '']
                    max_vol_number = max(map(int, result))
                    main_region = volume_lists[0].split(" ")[0]
                    for volume_title in volume_lists:
                        if main_region in volume_title:
                            for volume_num in range(max_vol_number + 1):
                                if str(volume_num) in volume_title:
                                    final_all_volumes.append(volume_title)
                    return final_all_volumes
            else:
                release_list = []
                for tr in all_trs:
                    date_released = format_date(tr)
                    all_tds = tr.find_all("td")
                    release_number = all_tds[1].text.strip().replace(".", "")
                    release_name = all_tds[3].find("div").text

                    alt_releases_name = []
                    # Get all divs in the tr except the first one
                    alt_release_name_div_list = all_tds[3].find_all("div")[1:]
                    if len(alt_release_name_div_list) != 0:
                        for div in alt_release_name_div_list:
                            for alt_div in div:
                                stripped_text = alt_div.text.strip()
                                if stripped_text != "":
                                    alt_releases_name.append(stripped_text)

                    data_json = {
                        "date_released": date_released,
                        "release_number": release_number,
                        "release_name": {
                            "main": release_name,
                            "alt": alt_releases_name
                        }
                    }
                    release_list.append(data_json)
                return release_list

        # =============================================================== #
        endpoint = f"{self._ann_details_endpoint}/anime.php"
        params = {
            "id": ann_id,
        }
        # Initially sends a get request to the site as an anime, if the name contains (manga),
        # the request is resent to get the correct information
        html_site, request_status = get_request(endpoint, params=params)
        soup = soupify(html_site)

        main_title = get_main_title()

        self._type = "manga" if "(manga)" in main_title else "anime"
        logger.info(f"Media type is {self._type}")

        if not self._is_anime():
            endpoint = f"{self._ann_details_endpoint}/manga.php"
            params = {
                "id": ann_id,
            }

            html_site, request_status = get_request(endpoint, params=params)
            soup = soupify(html_site)

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

        return self._format_to_return(request_status, final_data)
