import _thread as thread
import base64
import hashlib
import hmac
import json
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlparse, urlencode
from wsgiref.handlers import format_date_time
import websocket  # 使用websocket_client

answer = ""
# 以下密钥信息从控制台获取
APP_ID = ""
API_SECRET = ""
API_KEY = ""


class SparkAI:

    def __init__(self, version=None):
        self.app_id = APP_ID
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.spark_url = "ws://spark-api.xf-yun.com/v2.1/chat" if version == 2 else ("ws://spark-api.xf-yun.com/v1.1"
                                                                                     "/chat")
        self.domain = "generalv2" if version == 2 else "general"
        self.host = urlparse(self.spark_url).netloc
        self.path = urlparse(self.spark_url).path

    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = (f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", '
                                f'signature="{signature_sha_base64}"')
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.spark_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws, one, two):
    print(" ")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, domain=ws.domain, question=ws.question))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        print(data)
        global answer
        answer += content
        if status == 2:
            ws.close()


def gen_params(appid, domain, question):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "random_threshold": 0.5,
                "max_tokens": 2048,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data


def send_request(question):
    global answer
    answer = ""
    question = [{"role": "user", "content": question}]
    ai = SparkAI()
    ai_url = ai.create_url()
    ws = websocket.WebSocketApp(ai_url, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = ai.app_id
    ws.question = question
    ws.domain = ai.domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    return answer
