BASE_URL = "https://animixplay.to/v1/"


def _get_anime_video(title: str, episode_number):
    """
    title parameter should be in japanese,
    else, it should be in english
    :param title:
    :param episode_number:
    :return video_link:
    """
    anime_title = title.title().replace(" ", "-")
    endpoint = f"{BASE_URL}{anime_title}/ep{episode_number}/"
    return endpoint
