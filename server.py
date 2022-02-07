from flask import Flask, request, jsonify, send_file
import backend

app = Flask(__name__)


@app.route("/search/manga/", methods=["GET"])
def search_manga_by_name():
    manga_name = request.args.get("name")
    return jsonify(backend.search_manga_by_name(manga_name))


@app.route("/search/anime/", methods=["GET"])
def search_anime_by_name():
    anime_name = request.args.get("name")
    return jsonify(backend.search_anime_by_name(anime_name))


@app.route("/fetch/details/", methods=["GET"])
def fetch_media_details():
    ann_id = request.args.get("ann_id")
    return jsonify(backend.search_anime_by_name(ann_id))


@app.route("/fetch/manga_file/")
def return_manga_file():
    manga_name = request.args.get("name")
    chapter_number = request.args.get("ch")

    with open(backend.get_manga(manga_name, chapter_number), "rb") as static_file:
        return send_file(static_file)


@app.route("/fetch/anime_link")
def return_video_link():
    anime_title = request.args.get("name")
    episode_number = request.args.get("num")
    return jsonify(backend.get_anime_video_link(anime_title, episode_number))


if __name__ == "__main__":
    app.run()
