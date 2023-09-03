import json

import jmespath
import requests

API_KEY = ""
SECRET_KEY = ""


def get_access_token():
    url = f"https://aip.baidubce.com/oauth/2.0/token?client_id={API_KEY}&client_secret={SECRET_KEY}&grant_type=client_credentials"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json().get("access_token")


def chat(question):
    url = ("https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token="
           + get_access_token())
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": f"你现在扮演一个“饶庆龙”，饶庆龙是一个有趣的人，常常会用非常幽默风趣的语气回复别人的对话。回复内容要符合人的口气哟，只用模仿“饶庆龙”语气回复消息即可，以下是好友的提问：{question}"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    return jmespath.search("result", response_json)
