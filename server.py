from ANN_api import ANNApi

annapi = ANNApi()
# anime_id = annapi.search_anime_by_name("dr. stone")
# print(anime_id)
details = annapi.get_anime_details_by_id(14445)
print(details)
