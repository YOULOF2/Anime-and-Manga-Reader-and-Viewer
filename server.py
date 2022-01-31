from backend import search_anime_by_name, get_anime_or_manga_by_ams_id
import langid

anime_details = get_anime_or_manga_by_ams_id(10216)
payload = anime_details.get("payload")
titles = payload.get("title")
alt_titles = titles.get("alt")
for alt in alt_titles:
    if "(Japanese)" in alt:
        text = alt.split("(Japanese)")[0]
        lang_detection = langid.classify(text)[0]
        if not lang_detection == "ja":
            print(text)

