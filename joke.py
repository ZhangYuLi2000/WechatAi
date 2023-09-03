import jmespath
import requests


def get_content():
    response = requests.get("https://api.shadiao.pro/pyq")
    json_response = response.json()
    return jmespath.search("data.txt", json_response)
