from backend._ApiBase import ApiBase
import requests
import zipfile
import os
from pathlib import Path
from backend.utilities import *


class _MangaCollector(ApiBase):
    def __init__(self):
        super().__init__()
        self._base_endpoint = "https://mangakomi.com/"

    def get_manga_pdf_by_id_and_chapter(self, manga_name: str, chapter_num):
        clean_manga_name = manga_name.casefold().replace(" ", "-")
        clean_chapter_name = f"chapter-{chapter_num}"
        endpoint = f"{self._base_endpoint}manga/{clean_manga_name}/{clean_chapter_name}/"
        html_site, status_code = get_request(endpoint)
        soup = soupify(html_site)
        all_images_element = soup.find_all("img", class_="wp-manga-chapter-img")
        all_images_src = [str(img.get("data-src")).replace("\t", "").replace("\n", "") for img in all_images_element]
        all_image_ids = [img.get("id") for img in all_images_element]

        image_filenames = []
        zip_file_name = f"backend/output/{manga_name.title()}-ch{chapter_num}.zip"
        zip_file = zipfile.ZipFile(zip_file_name, "w")

        for image_src, image_id in zip(all_images_src, all_image_ids):
            filename = f"{image_id}.jpg"
            with open(filename, "wb") as image:
                response = requests.get(image_src)
                image.write(response.content)
            image_filenames.append(filename)

            zip_file.write(filename)
        zip_file.close()

        # Remove all files in backend/output directory except the zip_file_name
        all_files_in_output = [f"backend/output/{file}" for file in os.listdir("backend/output/")]
        all_files_in_output.remove(zip_file_name)
        for file in all_files_in_output:
            os.remove(file)

        zip_file_path = Path(zip_file_name)
        zip_file_path.rename(zip_file_path.with_suffix(".cbz"))

        for file in image_filenames:
            os.remove(file)

        return zip_file_path
