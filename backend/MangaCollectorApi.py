from backend.ApiBase import ApiBase
from bs4 import BeautifulSoup


class MangaCollectorApi(ApiBase):
    def __init__(self):
        super().__init__()
        self._base_endpoint = "https://readmanganato.com/"

    def search_for_manga_by_name(self, manga_name: str):
        # Format the manga_name to replace spaces with _
        formatted_manga_name = manga_name.replace(" ", "_")
        endpoint = f"{self._base_endpoint}search/story/{formatted_manga_name}"
        html_site, status_code = self._get_request(endpoint)
        soup = BeautifulSoup(html_site, "html.parser")
        manga_details_div = soup.find_all("div", class_="search-story-item")
        data_json = []
        for manga_search_item in manga_details_div:
            item_manga_name = manga_search_item.find("a", class_="item-title").text
            item_manga_id = manga_search_item.find("a", class_="item-title").get("href").split("-")[1]
            item_manga_latest_chapters = [i.text for i in manga_search_item.find_all("a", class_="item-chapter")]
            item_manga_authors = manga_search_item.find("span", class_="item-author").text.split(",")
            data_json.append(
                {
                    "id": item_manga_id,
                    "title": item_manga_name,
                    "latest_releases": item_manga_latest_chapters,
                    "authors": item_manga_authors,
                }
            )
        return data_json
