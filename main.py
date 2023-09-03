import sys

import ntchat

from Wenxin import chat
from joke import get_content
from sparkAI import send_request

USE_AI = 1  # 1 科大讯飞；2 百度文心一眼


def main():
    """
    主程序：调用微信，监听消息（排除群消息）
    :return:
    """
    wechat = ntchat.WeChat()
    wechat.open(smart=True)
    wechat.wait_login()

    @wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
    def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
        """
        监听微信消息，如果不是自己的或者群的消息，调用 AI 服务
        根据 USE_AI 决定使用的 AI 服务，其他都调用段子回复接口
        :param wechat_instance:
        :param message:
        :return:
        """
        data = message["data"]
        from_wxid = data["from_wxid"]
        self_wxid = wechat_instance.get_login_info()["wxid"]
        if from_wxid != self_wxid and not data.get("room_wxid"):
            question = data['msg']
            answer = ""
            try:
                if USE_AI == 1:
                    answer = send_request(question) if question else "你为什么发空消息？"
                elif USE_AI == 2:
                    answer = chat(question)
                else:
                    answer = get_content()
            except Exception as e:
                print(e)
            finally:
                wechat_instance.send_text(to_wxid=from_wxid, content=answer)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        ntchat.exit_()
        sys.exit()


if __name__ == '__main__':
    main()
